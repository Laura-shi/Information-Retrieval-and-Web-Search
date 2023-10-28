import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin
from nltk.tokenize import word_tokenize
from collections import deque
import re

# Define the base directory for saving files and links
base_dir = 'C:/Users/Laura/Documents/Data Science/UoM/Inform Retrieval and web search/homework/assignment6/text_moved_html_tags'
os.makedirs(base_dir, exist_ok=True)

# Control variables
total_files_to_save = 10000
total_saved_files = 0

# Create a BFS queue to manage URLs to visit
url_queue = deque(["https://www.memphis.edu/"])  # Start with the root URL

# Function to save text content to a file
def save_text_content(text_content, file_path):
    with open(file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text_content)

while url_queue and total_saved_files < total_files_to_save:
    # Dequeue the next URL to visit
    current_url = url_queue.popleft()

    # Make an HTTP request to the current URL
    try:
        response = requests.get(current_url)
        response.raise_for_status()  # Check for HTTP request errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text content from HTML using Beautiful Soup
        text_content = soup.get_text()

        # Tokenize text
        tokens = word_tokenize(text_content)
        if len(tokens) >= 50:
            # Save the plain text content in a single folder
            file_name = f"file_{total_saved_files}.txt"
            file_path = os.path.join(base_dir, file_name)
            save_text_content(text_content, file_path)

            # Save the original link (current URL) in the same folder
            link_file_path = os.path.join(base_dir, f"{file_name}.link.txt")
            with open(link_file_path, 'w', encoding='utf-8') as link_file:
                link_file.write(current_url)

            # Update the count of saved files
            total_saved_files += 1

        # Limit the number of saved files
        if total_saved_files >= total_files_to_save:
            break

        # Find and enqueue new URLs to visit (BFS) with the current URL as the original link
        new_links = [urljoin(current_url, link['href']) for link in soup.find_all('a', href=True)]
        url_queue.extend(new_links)

    except requests.RequestException as e:
        print(f"Failed to access the URL: {current_url}, Error: {e}")

print(f"Total files saved: {total_saved_files}")
