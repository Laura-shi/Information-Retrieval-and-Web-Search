import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize the Porter Stemmer for stemming
porter_stemmer = PorterStemmer()

# Load the stopwords and create a set
stopwords_set = set(stopwords.words('english'))


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

    if not words:
        #print("Warning: Document content is empty after preprocessing.")
        return ""

    # Convert to lowercase and join the words back into a single string
    preprocessed_text = ' '.join([word.lower() for word in words])

    # Tokenize the text into words and apply lemmatization
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(preprocessed_text)
    words = [lemmatizer.lemmatize(word) for word in words]

    return preprocessed_text


def calculate_document_vectors(result_set, invertedIndex, documents, links):
    vectorizer = TfidfVectorizer()
    documents_content = [" ".join(documents[filename]) for filename in result_set if documents[filename] is not None]

    if not documents_content:
        #print("Error: No valid documents to calculate vectors.")
        return None

    document_vectors = vectorizer.fit_transform(documents_content)
    return document_vectors, vectorizer


def calculate_query_vector(query, vectorizer):
    query_vector = vectorizer.transform([query])
    return query_vector


def rank_documents(document_vectors, query_vector, result_set):
    # Calculate cosine similarity between query vector and document vectors
    similarities = cosine_similarity(query_vector, document_vectors).flatten()

    # Rank documents based on cosine similarity
    ranked_results = [(filename, similarity) for filename, similarity in zip(result_set, similarities)]
    ranked_results.sort(key=lambda x: x[1], reverse=True)
    if document_vectors is None:
        #print("Error: Unable to rank documents due to missing vectors.")
        return []

    return ranked_results


def get_document_url(filename, links):
    return links.get(filename, "Link not available")


def phrase_query(query, invertedIndex, documents, links):
    pattern = re.compile('[\W_]+')
    query = pattern.sub(' ', query)
    listOfLists = [one_word_query(word, invertedIndex) for word in query.split()]

    setted = set(listOfLists[0]).intersection(*listOfLists)

    if not setted:
        print("No documents found.")
        return []

    # Calculate document vectors
    document_vectors, vectorizer = calculate_document_vectors(setted, invertedIndex, documents, links)

    # Calculate query vector using the same fitted vectorizer
    query_vector = calculate_query_vector(query, vectorizer)

    # Rank documents based on cosine similarity
    ranked_documents = rank_documents(document_vectors, query_vector, setted)

    # Retrieve filenames and links for the top-ranking documents
    results = []
    for doc_id, similarity in ranked_documents:
        filename = os.path.basename(doc_id)
        link = get_document_url(doc_id, links)
        results.append({'filename': filename, 'similarity': similarity, 'link': link})

    return results


def one_word_query(word, invertedIndex):
    pattern = re.compile('[\W_]+')
    word = pattern.sub(' ', word)
    if word in invertedIndex.keys():
        return [filename for filename in invertedIndex[word].keys()]
    else:
        return []


def index_one_file(termlist):
    fileIndex = defaultdict(list)
    for index, word in enumerate(termlist):
        fileIndex[word].append(index)
    return fileIndex


def create_inverted_index(documents):
    invertedIndex = defaultdict(dict)
    for filename, terms in documents.items():
        fileIndex = index_one_file(terms)
        for term, positions in fileIndex.items():
            invertedIndex[term][filename] = positions

    return invertedIndex


def process_files(filenames):
    file_to_terms = {}
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            content = ' '.join(lines).lower()
            pattern = re.compile('[\W_]+')
            content = pattern.sub(' ', content)
            file_to_terms[filename] = content.split()

    return file_to_terms

# read the local folder
def read_local_files(directory):
    filenames = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith(".txt")]
    return process_files(filenames)





# distinguish the content files and links file.
def get_content_and_links(directory):
    content_files = []
    link_files = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            base_filename, extension = os.path.splitext(filename)

            if extension == '.txt':
                content_files.append(file_path)
                #print("Content file:", file_path)

                # Update the link file extension to ".link.txt"
                link_filename = f'{base_filename}.link.txt'
                #print("Expected link file:", link_filename)
                link_files.append(os.path.join(directory, link_filename))

    return content_files, link_files

# read the original link from the link files
def read_links(directory, content_files):
    links = {}

    for content_file in content_files:
        # Form the expected link file name by adding ".link.txt" to the content file name
        link_file = content_file + ".link.txt"

        try:
            with open(content_file, 'r', encoding='utf-8', errors='ignore') as content_f, \
                 open(link_file, 'r', encoding='utf-8', errors='ignore') as link_f:

                content = content_f.read()
                link_content = link_f.read()

                #print("Content File:", content_file)
                #print("Link Content:", link_content)

                links[content_file] = link_content
        except Exception as e:
            #print(f"Error reading files {content_file} and {link_file}: {e}")
            pass
    return links



# read the 10000 files[crawling from hw6] from local path
def get_directory_path():
    #directory = input("Enter the directory path containing text files: ").strip()
    directory = r"C:\Users\Laura\Documents\Data Science\UoM\Inform Retrieval and web search\homework\assignment 6\text_moved_html_tags"
    if not directory or not os.path.isdir(directory):
        print("Error: Please enter a valid directory path.")
        return get_directory_path()
    return directory

# get the input value from user
def get_user_query():
    query = input("Enter your query: ").strip()
    if not query:
        print("Error: Please enter a valid query.")
        return get_user_query()
    return query


def main():
    directory = get_directory_path()
    user_query = get_user_query()

    content_files, link_files = get_content_and_links(directory)
    links = read_links(directory, content_files)

    if content_files and link_files:
        documents = read_local_files(directory)
        invertedIndex = create_inverted_index(documents)

        # Process the user's query
        query_results = phrase_query(user_query, invertedIndex, documents, links)

        if query_results:
            print("\nTop Results:")
            for result in query_results:
                print(f"\nFilename: {result['filename']}")
                print(f"Similarity Score: {result['similarity']}")
                print(f"Link: {result['link']}")
        else:
            print("No matching documents found.")
    else:
        print("No content or link files found.")

if __name__ == "__main__":
    main()
