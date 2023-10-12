#import urllib.request
import requests
from bs4 import BeautifulSoup
import string
from collections import defaultdict


# get content from website
#content= urllib.request.urlopen('https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/')
#print(content.read())
content = requests.get("https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/")


# clear the html contents 
soup=BeautifulSoup(content.text,'html.parser')
# get the text from website and transfor to lower letters
web_text=soup.get_text().lower()

# split the words and move punctuation
move_punctuation = str.maketrans('','',string.punctuation)
words = web_text.translate(move_punctuation).split()

# count each word's frequency
word_frequency = defaultdict(int)
for word in words:
    word_frequency[word] += 1

# count how many words for total
total_words = len(words)
print(f"The course website has :{total_words} words\n")

# print the frequency of each item
sorted_word_frequency = sorted(word_frequency.items())
for word, frequency in sorted_word_frequency:
    print(f'{word} occur:{frequency} times')

    