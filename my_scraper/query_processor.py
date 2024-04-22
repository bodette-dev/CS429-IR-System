import pickle
from flask import Flask, request, jsonify
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from werkzeug.exceptions import HTTPException, MethodNotAllowed


# Ensure required NLTK downloads are present
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

TOP_K = 5  # Number of top results to return

# Function to load inverted index from .pkl file
def load_idx(path):
    try:
        with open(path, 'rb') as idx_file:
            # Load inverted index
            return pickle.load(idx_file)
    except FileNotFoundError:
        print("Inverted index file not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the index: {e}")
        return None

# Function to validate query
def validate_query(query):
    # Check if the query is not None or empty string and does not contain illegal characters
    # Adjust the regular expression as needed to match your validation requirements
    pattern = re.compile("^[a-zA-Z0-9 ]+$")  # Example pattern: allows only alphanumeric characters and space
    return query is not None and query.strip() != "" and pattern.match(query)


# Preprocess text function
def preprocess_text(txt):
    txt = txt.lower()
    txt = re.sub(r'[^\w\s]', '', txt)
    toks = word_tokenize(txt)
    stop_words = set(stopwords.words('english'))
    filtered_toks = [word for word in toks if not word in stop_words]
    return filtered_toks

# Transform query function
def transform_query(query, vectorizer):
    query_toks = preprocess_text(query)
    query_str = " ".join(query_toks)
    query_vect = vectorizer.transform([query_str])
    return query_vect

# Calculate cosine similarity function
def calculate_cosine_similarity(query_vector, tfidf_matrix):
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)
    return cosine_similarities.flatten()

@app.route('/process_query', methods=['POST'])
def process_query():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    try:
        query_data = request.get_json()
        
        # Ensure 'query' key exists and is of type 'str'
        if 'query' not in query_data or not isinstance(query_data['query'], str):
            return jsonify({"error": "Empty or missing query in request"}), 400

        query_text = query_data['query']
        if not validate_query(query_text):
            return jsonify({"error": "Invalid query"}), 400

        query_vector = transform_query(query_text, vectorizer)
        similarity_scores = calculate_cosine_similarity(query_vector, tfidf_matrix)
        

        # Rank results and construct response
        # Get indices of non-zero scores and sort them by score in descending order
        nonzero_indices = np.nonzero(similarity_scores)[0]
        top_indices = np.argsort(-similarity_scores[nonzero_indices])[:TOP_K]
        top_scores = similarity_scores[nonzero_indices][top_indices]

        # Generate results ensuring only non-zero scores are included
        results = [{"doc_id": int(nonzero_indices[idx]), "score": float(score)} for idx, score in enumerate(top_scores) if score > 0]
    
        response = {
            "success": True,
            "query": query_text,
            "results": results
        }
    except Exception as e:
        # Log the error here if you want
        return jsonify({"error": "Bad request, invalid input"}), 400
    
    return jsonify(response), 200

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    return jsonify(error="Method not allowed."), 405

# Path to the serialized objects
IDX_FILE = 'inverted_index.pkl'
VECTORIZER_FILE = 'vectorizer.pkl'
TFIDF_MATRIX_FILE = 'tfidf_matrix.pkl'

# Load the serialized objects at startup
inverted_idx = load_idx(IDX_FILE)
vectorizer = load_idx(VECTORIZER_FILE)
tfidf_matrix = load_idx(TFIDF_MATRIX_FILE)

# Ensure the serialized objects are loaded correctly
if inverted_idx is None or vectorizer is None or tfidf_matrix is None:
    raise Exception("Failed to load serialized objects.")

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify(error="The resource could not be found."), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error="Bad request."), 400

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="Internal server error."), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    return jsonify(error="An unexpected error occurred."), 500

if __name__ == '__main__':
    app.run(debug=True)
