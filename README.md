# CS 429 - Individual Project 
# Blake Odette

## Abstract
The goal of this project was to develop an information retrieval-based system capable of efficiently finding and retrieving information from websites, organizing it for searching, and managing user queries. I used Python tools to develop a web crawler with Scrapy to collect web pages, an indexing system using Scikit-Learn to sort the information, and finally, a Flask application for managing and responding to searches with a list of best matches. 

The crawler is initialized with a seed URL which I have provided, www.iit.edu, as well as values for the max pages (*page_limit* in *my_spider.py*) and max depth (*page_depth* in *my_spider.py*). The indexer uses measurements of cosine similarity to ensure that the most relevant documents are matched with user queries and returned. Finally, the Flask-based processor is used to apply query validation to the user input and return the top-K ranked results. 

The next steps for the project aim to improve the system's accuracy and scalability as well as enhance the experience of the user. These steps include implementing additional features such as concurrent and distributed crawling, vector embedding representations for indexing, and natural language processing enhancements for query processing. These developments will work to further optimize the system's performance as well as expand its capabilities to handle more complex user queries. 

## Overview

The system consists of three primary components: a web crawler, an indexer, and a query processor. 

 - Web Crawler: Built using Scrapy, it browses the Internet starting from the provided URL (www.iit.edu), and collects web documents up to a provided number of pages and depth. These configurations can be easily adjusted, allowing for flexibility depending on the scope and scale of the information need. 
 - Indexer: After collecting documents, control is passed to the indexer. The indexer searches through the content of the web documents and organizes it into a single inverted index. The TF-IDF scores were used to weigh the importance of words in each document. This allows the system to ultimately determine how relevant a document is to a search query. 
 - Query Processor: This Flask-based application accepts input from the user and processes it to match the terms against the previously-created inverted index. This application uses cosine similarity to rank the documents in order of relevance. 

Together, these components come together to create an information retrieval system capable of handling complex user queries and returning relevant results efficiently and accurately. 

## Design

**Capabilities:** My system is able to effectively and efficiently navigate, collect, and process html document data from the web. My query processor is capable of interpreting user queries, validating their input, and then using the previously created TF-IDF inverted index to fetch and rank the results. Through a series of comprehensive unit tests, my system has proven to be capable of handling complex user queries with ease. 

**Interactions:** Each module in my system is designed for a specific task and interacts with one another. The crawler fetches the data and passes it to the indexer, which proceeds to then generate an inverted index that the query processor will proceed to search and make use of in ranking documents based on relevance. This creates a flow of interaction that aims to achieve accurate results in an efficient and timely manor. 

**Integration:** Due to the interactability of our components, the components come together to create a single, cohesive search mechanism. Having these components connected in a Python environment allows for the system to be easily updatable. The potential for development of new features or improvements on previous components is great due to its easily modifiable individual components. 

## Architecture

The architecture of our system was designed with cohesive interaction between the three components in mind. The interface between the crawler and indexer is a structured JSON file, which is populated with web data by the crawler. This data is then used by the indexer for creating the inverted index. The query processor utilizes this inverted index so that it can match user queries with documents based on their cosine similarity scores. This sequential process of translating raw web data into a readible format for the query processor to utilize demonsrates the integrated nature of the system. 

The system's front end is represented by the query processing Flask application. This front end communicates with the indexer to fetch and display the search results. The architecture of my solution ensures that each module functions independently, yet integrates smoothly into a unified operation. This modular architecture also allows for simplified maintenance and updatability. 

## Operation

In order to build, run, and test the system, these simple instructions should be followed:
 - From the root directory, you will notice two directories: *my_scraper* and *new_build*. *my_scraper* contains all of the files used to create my system. This is the end result of building the system. Every time the system is built, a new *my_scraper* directory will be created, containing all system components. *new_build* contains a zip file, two python modules, and a shell script.
 - Navigate to the *new_build* directory. 
 - To build the system and do nothing else, run this command from the *new_build* directory: python3 build_crawler.py
 - To run the built system and do nothing else, run this command from the *new_build* directory: python3 run_scraper.py
 - In order to build, run, and test the system in one single command, run this command from the *new_build* directory: ./*run_tests.sh*. This command will generate a file, *test_results.txt* in the same directory where the shell script is run. If the tests in *my_scraper/test_flak_app.py* are run on their own, this text file will be generated and placed in the outer */my_scraper* directory instead. **Note: You may need to run the following command prior to executing the shell script 'chmod +x run_tests.sh'** 
 - When running the *run_tests.sh* script, users don't need to input anything manually, the script handles everything. The sample query supplied to the system is the word, "Elevate". When running the *run_scraper.py* module instead, the user can provide a custom query of their own. 
 - If you wish to modify the supplied values for max pages and max depth, you can manually modify the values of *page_limit* and *depth_limit* in *my_scraper/my_scraper/spiders/my_spider.py*
 - If you wish to modify the amount of wait time between the execution of the *run_scraper.py* module and the execution of the *test_flask_app.py* in the shell script, you can manually change the wait time on line 10 of *run_tests.sh*

Installation of all necessary libraries and dependencies is straightforward and handled in the build_crawler.py module. 

The system is designed to do all of the heavy lifting, allowing users to enjoy an easy-to-use and effective information retrieval system. 

It is important to note that I utilized ChatGPT 3.5 in order to help create my *build_crawler.py* and *run_scraper.py* modules. The language model was able to generate a general structure, which I further modified to be compatible with my existing code and file structure. Code for some of the tests was modified based off of further suggestions by ChatGPT 3.5, but most of the test themselves and all of the content of *run_tests.sh* were written by me without assistance. 

## Conclusion

To conclude, my code successfully creates an effective and efficient information retrieval system. Using Python libraries, the system retrieves, indexes, and processes web documents. The Scrapy crawler, indexer, and query processor work together to provide consistently accurate results. 

While the system has proven successful through rigourous testing, it is important to acknowledge the limitations of this system. For example, the scope of the web pages crawled is not as great as it could potentially be. There is also potential for varying degrees of accuracy in our results depending on the data available and the search terms provided by the user. 

Future efforts could focus on expanding the reach of the crawler, optimizing the search algorithm to improve speed and performance, and implement a more sophisticated approach to handling queries. Thankfully, the flexibility of the system allows for these changes to be fairly easy to implement. 

## Data Sources

All data sources for this project are web pages accessed via hyperlinks that the Scrapy crawler has followed. The crawler begins with the seed URL, "www.iit.edu", and recursively follows links found within these pages in accordance with the constraints such as total number of pages and max depth. 

Each page is downloaded and processed so that meaningful text can be extracted. This allows redundant and irrelevant content to be ignored in favor of relevant results. 

There are no issues with information access when it comes to my system. This is because my scraper is compliant with the robots.txt files on the downloaded web pages, and does not violate the terms of service for the pages. 

## Test Cases

The testing framework for my project is included as a robust suite of tests that can be found in *my_scraper/test_flask_app.py*. The nine tests present in this python module perform comprehensive coverage of the Flask application. Included in the suite are tests for:
 - Validating queries.
 - Handling empty user queries.
 - Handling queries that return no results.
 - Handling queries that contain unexpected datatypes. 
 - Handling an unallowed GET request.
 - Handling a JSON submission without a query field.
 - Handling a non-JSON submission.
 - Handling a POST request with no data argument provided.
 - Validating queries with illegal characters.

The coverage of my tests range from simple unit tests to much more complex integration and functional tests. These more complex tests validate the application's interactions with the underlying components. 

## References

Croft, W. Bruce, Donald Metzler, and Trevor Strohman. Search engines: Information retrieval in practice. Boston, 
    MA: Addison-Wesley, 2015.

“Scikit-Learn User Guide.” Scikit-Learn, n.d. https://scikit-learn.org/stable/user_guide.html. 
    
“Requests: HTTP for HumansTM.” Read the Docs, n.d. https://requests.readthedocs.io/en/latest/. 
    
"Scrapy 2.11 Documentation." Scrapy, n.d. https://docs.scrapy.org/en/latest/. 

“NumPy Documentation.” NumPy, n.d. https://numpy.org/doc/stable/.

“Web Scraping with Beautiful Soup.” Pluralsight, January 8, 2019. 
    https://www.pluralsight.com/resources/blog/guides/web-scraping-with-beautiful-soup.

“Documentation: Natural Language Toolkit.” NLTK, January 2, 2023. https://www.nltk.org/. 

“Pickle - Python Object Serialization.” Python Documentation, n.d. https://docs.python.org/3/library/pickle.html. 

“JSON - JSON Encoder and Decoder.” Python Documentation, n.d. https://docs.python.org/3/library/json.html. 

“Unittest - Unit Testing Framework.” Python Documentation, n.d. https://docs.python.org/3/library/unittest.html. 

“Welcome to Flask - User’s Guide.” Flask Documentation (3.0.x), n.d. https://flask.palletsprojects.com/en/3.0.x/. 

