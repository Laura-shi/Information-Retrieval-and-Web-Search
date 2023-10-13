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

from collections import defaultdict



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

    # create a dictionary to store term indices
    word_index=defaultdict(list)
    
    #split the content into terms and store their indices
    
    for i, word in enumerate(words):
        word_index[word].append(i)

    return preprocessed_text,word_index


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
def crawl_text_from_txt(url):
    response = requests.get(url)
    return response.text




# input articles 
url_dict = {
    'https://news.yahoo.com/louisiana-officials-efforts-combat-saltwater-234431982.html': 'html',
    'https://news.yahoo.com/webb-image-reveals-mysterious-planet-193350030.html': 'html',
    'https://news.yahoo.com/summer-2023-hottest-record-yes-122910650.html': 'html',
    'https://news.yahoo.com/africa-first-carbon-removal-plant-205258930.html': 'html',
    'https://news.yahoo.com/trump-considering-visiting-capitol-amid-224523933.html':'html',
    'https://news.yahoo.com/lifestyle/being-vegetarian-might-dna-210214800.html':'html',
    'https://www.yahoo.com/news/chiefs-half-districts-where-moms-101500871.html':'html',
    'https://news.yahoo.com/the-uaw-strike-and-electric-cars-does-trump-have-a-new-wedge-issue-183658881.html':'html',
    'https://finance.yahoo.com/news/amazon-spacex-duel-heats-tardy-223837713.html':'html',
    'https://news.yahoo.com/gma/white-house-trump-allegedly-discussed-203359022.html':'html'

}


# Function to convert URL to a valid filename
def url_to_filename(url):
    # Remove special characters from the URL to create a valid filename
    return "".join(c if c.isalnum() else "_" for c in url)





def main():
    output_directory = r'C:\Users\Laura\Documents\Data Science\UoM\Inform Retrieval and web search\homework\assignment 5'

    # Dictionary to store word frequency for each document
    document_word_frequency = defaultdict(lambda: defaultdict(int))

    # Document frequency for each word
    word_df = defaultdict(int)

    # Set of all URLs
    all_urls = set(url_dict.values())

    # Iterate through the URLs and file types in the url_dict
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
            # Preprocess the text
            preprocessed_text, word_index = preprocess_text(text)

            # Calculate word frequency for this document
            word_frequency = defaultdict(int)
            for word in preprocessed_text.split():
                word_frequency[word] += 1

            # Update document_word_frequency and word_df
            for word, freq in word_frequency.items():
                document_word_frequency[word][url] = freq
                word_df[word] += 1

            # Print word frequency for this document
            print(f'URL: {url}')
            print("Word Frequency:")
            for word, freq in word_frequency.items():
                print(f"Word: {word}, Frequency in {url}: {freq}")

            # Save the preprocessed text to a file (similar to your original code)
            filename = url_to_filename(url) + '.txt'
            file_path = os.path.join(output_directory, filename)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f"URL: {url}\n")
                file.write(f'Text: {preprocessed_text}\n')
                file.write('Word Frequency:\n')
                for word in word_index:
                    freq = word_frequency.get(word, 0)
                    file.write(f'Word: {word}, Frequency in {url}: {freq}\n')

                # Count how many words in total
                total_words = len(preprocessed_text.split())
                print(f'Total words: {total_words}\n')

            print(f"Preprocessed text for URL {url} saved to {filename}")

    # Save the inverted index to a file
    inverted_index_file = os.path.join(output_directory, 'inverted_index.txt')
    with open(inverted_index_file, 'w', encoding='utf-8') as file:
        file.write("Inverted Index (word -> (document, tf, df)):\n")
        for word, doc_data in document_word_frequency.items():
            file.write(f"{word} -> {doc_data} (df={word_df[word]})\n")

            

    print("Inverted index saved to 'inverted_index.txt'.")

if __name__ == "__main__":
    main()
