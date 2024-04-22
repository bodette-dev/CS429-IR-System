import subprocess
import os
import sys

PROJECT_NAME = 'my_scraper'
SPIDER_NAME = 'my_spider'
TEXT_PROCESSING_SCRIPT = 'text_processing.py'
QUERY_PROCESSOR_SCRIPT = 'query_processor.py'

def run_spider():
    # Ensure current working directory is project root
    project_path = os.path.join(os.getcwd(), PROJECT_NAME)
    os.chdir(project_path)
    
    # Define path to output JSON file
    output_json_path = os.path.join(project_path, "scraped_data.json")
    
    # Check if JSON file exists and remove it if it does
    if os.path.exists(output_json_path):
        os.remove(output_json_path)
        print(f"Existing JSON file removed: {output_json_path}")

    # Run spider
    subprocess.run(["scrapy", "crawl", SPIDER_NAME, "-o", "scraped_data.json", "-t", "json"])
    
    # Run text processing
    subprocess.run([sys.executable, TEXT_PROCESSING_SCRIPT])

    # Run query processor
    subprocess.run([sys.executable, QUERY_PROCESSOR_SCRIPT])

if __name__ == "__main__":
    run_spider()

