import os
import sys
import zipfile
import subprocess
from shutil import copyfile, rmtree

PROJECT_NAME = 'my_scraper'
SPIDER_NAME = 'my_spider'
ZIP_FILE = 'my_scraper.zip'

def install_packages():
    # Install required packages
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'scrapy'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'nltk'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'scikit-learn'])

def unzip_project(zip_path, extract_to):
    # Unzip project contents
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Unzipped '{zip_path}' into '{extract_to}'.")

def create_scrapy_project(project_name):
    # Create new Scrapy project if it doesn't exist
    if not os.path.exists(project_name):
        subprocess.run(["scrapy", "startproject", project_name])
        print(f"Scrapy project '{project_name}' has been created.")
    else:
        print(f"Scrapy project '{project_name}' already exists.")

def copy_custom_code(src_file, dest_file):
    # Copy code from zip file into new project directory
    try:
        if os.path.isfile(src_file):
            copyfile(src_file, dest_file)
            print(f"Copied custom code from '{src_file}' to '{dest_file}'.")
        else:
            print(f"No custom code file found at '{src_file}' to copy.")
    except IOError as e:
        print(f"Failed to copy file from '{src_file}' to '{dest_file}'. Error: {e}")


def main():
    install_packages()

    # Directory where the zip will be extracted
    extract_dir = os.path.join(os.getcwd(), 'extracted')

    # Unzip project
    unzip_project(ZIP_FILE, extract_dir)

    # Create new Scrapy project
    create_scrapy_project(PROJECT_NAME)

    # Define source and destination files for other custom code
    src_items_file = os.path.join(extract_dir, PROJECT_NAME, PROJECT_NAME, 'items.py')
    dest_items_file = os.path.join(PROJECT_NAME, PROJECT_NAME, 'items.py')

    src_spider_file = os.path.join(extract_dir, PROJECT_NAME, PROJECT_NAME, 'spiders', f'{SPIDER_NAME}.py')
    dest_spider_file = os.path.join(PROJECT_NAME, PROJECT_NAME, 'spiders', f'{SPIDER_NAME}.py')

    src_settings_file = os.path.join(extract_dir, PROJECT_NAME, PROJECT_NAME, 'settings.py')
    dest_settings_file = os.path.join(PROJECT_NAME, PROJECT_NAME, 'settings.py')

    # Correct source and destination files for text_processing.py
    src_text_processing_file = os.path.join(extract_dir, PROJECT_NAME, 'text_processing.py')  # Updated path
    dest_text_processing_file = os.path.join(PROJECT_NAME, 'text_processing.py')
    
    # Correct source and destination files for query_processor.py
    src_query_processor_file = os.path.join(extract_dir, PROJECT_NAME, 'query_processor.py')
    dest_query_processor_file = os.path.join(PROJECT_NAME, 'query_processor.py')

    # Correct source and destination files for test_flask_app.py
    src_test_flask_app_file = os.path.join(extract_dir, PROJECT_NAME, 'test_flask_app.py')
    dest_test_flask_app_file = os.path.join(PROJECT_NAME, 'test_flask_app.py')


    # Copy the custom code files to their respective destinations
    copy_custom_code(src_items_file, dest_items_file)
    copy_custom_code(src_spider_file, dest_spider_file)
    copy_custom_code(src_settings_file, dest_settings_file)
    copy_custom_code(src_text_processing_file, dest_text_processing_file)  # Copy from correct source
    copy_custom_code(src_query_processor_file, dest_query_processor_file)
    copy_custom_code(src_test_flask_app_file, dest_test_flask_app_file)

    
    # Clean up extracted files
    rmtree(extract_dir)
    print(f"Removed temporary extraction directory '{extract_dir}'.")

if __name__ == "__main__":
    main()
