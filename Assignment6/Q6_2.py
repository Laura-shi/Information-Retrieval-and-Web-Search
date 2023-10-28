# Import necessary libraries
import os
import re
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF for PDF parsing
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
# Download the stopwords and wordnet corpus (needed for lemmatization) using nltk
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')



# Initialize the Porter Stemmer for stemming
porter_stemmer = PorterStemmer()

# Load the stopwords and create a set
stopwords_set = set(stopwords.words('english'))


# define a preprocess_text function to remove 
# digits,
# punctuation,
# stop words (use the generic list available at ...ir-websearch/papers/english.stopwords.txt)
# urls and other html-like strings,
# uppercases 
# morphological variations
def preprocess_text(text):
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)

    # Remove HTML-like strings
    text = re.sub(r'<.*?>', '', text)

    # Remove digits and punctuation
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize the text into words and apply stemming
    words = word_tokenize(text)
    words = [porter_stemmer.stem(word) for word in words if word.lower() not in stopwords_set]
    
    # Remove stopwords
    words = [word for word in words if word.lower() not in stopwords_set]
    
    # Convert to lowercase and join the words back into a single string
    preprocessed_text = ' '.join([word.lower() for word in words])

    # Tokenize the text into words and apply lemmatization
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word) for word in words]

    return preprocessed_text


# crawl content from webpages
def crawl_text_from_web(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    web_text = soup.get_text().lower()
    return web_text


# crawl contents from pdf file
def crawl_text_from_pdf(url):
    try:
        pdf_document = fitz.open(url)
        pdf_text = ''
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            pdf_text += page.get_text()
        return pdf_text
    except Exception as e:
        print(f'Error extracting text from PDF at {url}')
        return ' '


# crawl contents from txt file
def crawl_text_from_txt(folder_path):
    #response = requests.get(url)
    with open(folder_path,'r', encoding='utf-8') as file:
        return file.read()


# input local saved files
folder_path = "C:/Users/Laura/Documents/Data Science/UoM/Inform Retrieval and web search/homework/assignment6/text_moved_html_tags"

# cretae a dictionary to map files path to their type
url_dict={}

# List files in the specified directory
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)

        # Determine the file type based on the file extension
        if file_path.endswith(".pdf"):
            file_type = "pdf"
        elif file_path.endswith(".txt"):
            file_type = "txt"
        elif file_path.endswith(".html"):
            file_type = "html"
        else:
            # Handle other file types if needed
            file_type = "other"

        # Add the file path and type to the dictionary
        url_dict[file_path] = file_type


def main():
# Iterate the dictionary to check if the file format is "pdf","text" or "html",
# and then use the specific method to crawl text from them.

    gathered_texts = {}

    for url, file_type in url_dict.items():
        if file_type == 'pdf':
            text = crawl_text_from_pdf(url)
        elif file_type == 'txt':
            text = crawl_text_from_txt(url)
        elif file_type == 'html':
            text = crawl_text_from_web(url)
        else:
            print(f"Unsupported file type: {file_type}")
            continue

        if text:
            gathered_texts[url] = text


    # Preprocess the gathered text
    preprocessed_texts = {url: preprocess_text(text) for url, text in gathered_texts.items()}

    for url, preprocessed_text in preprocessed_texts.items():
        print(f"URL:{url}\n")

        # count each word's frequency
        word_frequency = defaultdict(int)
        for word in preprocessed_text.split():
            word_frequency[word] += 1

        sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
        
        for word, frequency in sorted_word_frequency:
            print(f'Word: {word}, Frequency: {frequency}')

    # Count how many words in total
        total_words = len(preprocessed_text.split())
        print(f'Total words: {total_words}\n')


    # store the output in my local computer
    output_directory = r'C:\Users\Laura\Documents\Data Science\UoM\Inform Retrieval and web search\homework\assignment6\text_Q2'
    # check the directory is exist or not
    if not os.path.exists(output_directory):
            os.makedirs(output_directory)   


    with open(os.path.join(output_directory, 'HW_6_output.txt'), 'w', encoding='utf-8') as f:
        # Iterate through the preprocessed texts and write to the file
        for url, preprocessed_text in preprocessed_texts.items():
            f.write(f"URL: {url}\n")
            f.write(f'Text: {preprocessed_text}\n')
            f.write('\n')  # Add a separator between entries

    print("Results written to HW_6_output_files.txt in the local computer .")

if __name__ == "__main__":

    main()
