import json
import re
import nltk
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('punkt')

def load_html(file_path):
    # Load HTML content from JSON file
    with open(file_path, 'r') as file:
        html = json.load(file)
    return html

def parse_html(content):
    # Assuming 'content' is a dictionary and the actual HTML is under the key 'main_content'
    soup = BeautifulSoup(content['main_content'], 'html.parser')
    return soup.get_text()


def preprocess_text(txt):
    # Make text case-insensitive and remove punctuation
    txt = txt.lower()
    txt = re.sub(r'[^\w\s]', '', txt)
    
    # Tokenize and remove stopwords
    toks = word_tokenize(txt)
    stop_words = set(stopwords.words('english'))
    filtered_toks = [word for word in toks if not word in stop_words]
    return filtered_toks
    
def compute_tfidf(docs):
    # Compute TF-IDF matrix for preprocessed docs
    txts = [" ".join(doc) for doc in docs]
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(txts)
    return tfidf, vectorizer

def build_inverted_index(tfidf, vectorizer):
    # Build inverted index from TF-IDF matrix
    features = vectorizer.get_feature_names_out()
    inverted_idx = {}

    # Iterate over all features
    for n, term in enumerate(features):
        # Retrieve column
        col = tfidf.getcol(n)
        
        # Convert column to list of tuples
        ids_and_scores = [(doc_id, tfidf_score) for doc_id, tfidf_score in zip(col.indices, col.data)]
        
        # Store mappings in the index
        inverted_idx[term] = ids_and_scores

    return inverted_idx

def transform_query(query, vectorizer):
    # Transform user query into same TF-IDF vector space as docs
    query_toks = preprocess_text(query)
    query_str = " ".join(query_toks)
    query_vect = vectorizer.transform([query_str])
    return query_vect

def calculate_cosine_similarity(query_vector, tfidf_matrix):
    # Calculate cosine similarity between query and document vectors
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)
    return cosine_similarities.flatten()

def save_inverted_index(inverted_index, file_path):
    """Serialize the inverted index and save it to a file."""
    with open(file_path, 'wb') as file:
        pickle.dump(inverted_index, file)

# Serialize the inverted index, vectorizer, and TF-IDF matrix
def save_objects(objects, file_names):
    for obj, file_name in zip(objects, file_names):
        with open(file_name, 'wb') as file:
            pickle.dump(obj, file)

json_path = 'scraped_data.json'
html_docs = load_html(json_path)

preprocessed = []
for content in html_docs:
    # Parse HTML and extract text
    txt = parse_html(content)
    # Preprocess text
    preprocessed.append(preprocess_text(txt))

# Compute TF-IDF matrix and build the inverted index
tfidf_matrix, vectorizer = compute_tfidf(preprocessed)
inverted_index = build_inverted_index(tfidf_matrix, vectorizer)

# Serialize the inverted index and vectorizer
save_objects(
    [inverted_index, vectorizer, tfidf_matrix], 
    ['inverted_index.pkl', 'vectorizer.pkl', 'tfidf_matrix.pkl']
)
print("Inverted index, vectorizer, and TF-IDF matrix serialized and saved.")
    
# Ask user for a query
query = input("Enter your query: ")
    
# Transform query into TF-IDF vector space
query_vect = transform_query(query, vectorizer)
    
# Calculate cosine similarities
# Here we need to use tfidf_matrix, which is the correct variable name
similarities = calculate_cosine_similarity(query_vect, tfidf_matrix)
    
# Print similarity scores
print(similarities)
