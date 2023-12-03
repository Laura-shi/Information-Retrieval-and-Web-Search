# app.py

from flask import Flask, render_template, request
from homework7 import phrase_query, create_inverted_index, read_local_files, read_links,get_directory_path,get_content_and_links

app = Flask(__name__)

# ... (Other functions remain unchanged)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Get the user input query from the form data
    data_from_form = request.form['data']

    # Assuming you have these functions from your_program.py
    directory = get_directory_path()
    content_files, link_files = get_content_and_links(directory)
    links = read_links(directory, content_files)

    if content_files and link_files:
        documents = read_local_files(directory)
        invertedIndex = create_inverted_index(documents)

        # Call the phrase_query function from your_program.py
        search_results = phrase_query(data_from_form, invertedIndex, documents, links)

        return render_template('result.html', query=data_from_form, search_results=search_results)
    else:
        return render_template('result.html', query=data_from_form, search_results=[])

if __name__ == '__main__':
    app.run(debug=True)
