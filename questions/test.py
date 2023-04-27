
import nltk
from nltk.tokenize import word_tokenize
import string
import sys
import math
import os


def main():
    files = load_files("corpus")
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    compute_idfs(file_words)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    files = os.listdir(directory)
    file_dict = {}

    for file in files:
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            content = str(f.read())
            file_dict[file] = content

    return file_dict


def tokenize(document):

    document = document.lower()
    tokenized_document = word_tokenize(document)
    tokenized_document = [
        word for word in tokenized_document if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english")]

    return tokenized_document


def compute_idfs(documents):

    words = {}
    idfs = {}

    # Populate words dict with number of times each word occurs in corpus
    for document in documents:
        for word in documents[document]:

            if word not in words:
                words[word] = 1
            else:
                words[word] += 1

    # Calculate IDF
    for word in words:
        word_appearances = 0
        for document in documents:
            if word in document:
                word_appearances += 1

        idf = math.log(len(documents) / word_appearances)
        idfs[word] = idf
        print(idf)

    return idfs


main()
