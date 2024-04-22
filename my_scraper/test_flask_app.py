import unittest
import requests
import json

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:5000/process_query"

    def test_valid_query(self):
        response = requests.post(
            self.base_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"query": "search term"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("results" in response.json())

    def test_empty_query(self):
        response = requests.post(
            self.base_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"query": ""})
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in response.json())

    def test_query_no_results(self):
        """Test a valid query that has no matching results in the index."""
        response = requests.post(
            self.base_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"query": "Aa"})
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue("results" in data)
        self.assertEqual(len(data["results"]), 0)  # Assuming no results should be empty
        
    def test_unexpected_data_type(self):
        """Test sending unexpected data types as a query."""
        response = requests.post(
            self.base_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"query": 12345})  # sending numbers instead of a string
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in response.json())
    
    def test_method_not_allowed(self):
        """Test using an HTTP method not allowed by the route."""
        response = requests.get(self.base_url)  # Using GET instead of POST
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
    
    def test_missing_query_field(self):
        """Test sending a JSON without the 'query' field."""
        response = requests.post(
            self.base_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({})
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in response.json())

    def test_non_json_submission(self):
        """Test sending a form data instead of JSON."""
        response = requests.post(
            self.base_url,
            data="query=search term"
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in response.json())

    def test_no_data_submission(self):
        """Test sending no data with the POST request."""
        response = requests.post(
            self.base_url,
            headers={"Content-Type": "application/json"}
            # No 'data' argument provided
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in response.json())

    def test_query_validation(self):
        """Test query validation with illegal characters."""
        illegal_query = "DROP TABLE users;--"
        response = requests.post(
            self.base_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"query": illegal_query})
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in response.json())
if __name__ == '__main__':
    with open('test_results.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner)

