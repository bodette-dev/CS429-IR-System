#!/bin/bash

# Run build_crawler.py
python3 build_crawler.py

# Run run_scraper.py
echo "Elevate" | python3 run_scraper.py &

# Wait for 200 seconds
sleep 200

# Run test_flask_app.py in a new terminal window
gnome-terminal -- python3 my_scraper/test_flask_app.py 

