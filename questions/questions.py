import nltk
from nltk.tokenize import word_tokenize
import string
import sys
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):

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
            if word in documents[document]:
                word_appearances += 1

        idf = math.log(len(documents) / word_appearances)
        idfs[word] = idf

    return idfs


def top_files(query, files, idfs, n):

    tf_idf_scores = dict()

    for file in files:
        score = 0

        for word in query:
            if word in files[file]:

                idf = idfs[word]
                appearances_in_doc = files[file].count(word)
                score += idf * appearances_in_doc

        tf_idf_scores[file] = score

    # Sort the key-value pairs by the value of the item; reverse=True achieves descending order
    top_scores = dict(sorted(tf_idf_scores.items(),
                      key=lambda item: item[1], reverse=True))

    # Return the top n document names
    return list(top_scores.keys())[:n]


def top_sentences(query, sentences, idfs, n):

    scores = []

    for sentence in sentences:
        matching_word_score = sum(
            idfs[word] for word in query if word in sentences[sentence])
        query_term_density = sum(
            1 for word in query if word in sentences[sentence]) / len(sentences[sentence])
        scores.append((sentence, matching_word_score, query_term_density))

    # The sort() function's default behavior is to sort the list in natural ascending order. When you provide a key, it temporarily applies that function to each value you specify and THEN applies the natural ascending order sort.
    # x[1] and x[2] are the matching_word_score and query_term_density for each sentence. Our goal is to get the resulting list in descending order. Consider that the highest score in a list of scores will become the LOWEST score if we negate the score. This produces the descending order.
    # If two sentences have the same value for -x[1], the sort() function then looks as the second value in the tuple -- the query_term_density.

    scores.sort(key=lambda x: (-x[1], -x[2]))
    top_n_sentences = [score[0] for score in scores[:n]]

    return top_n_sentences


if __name__ == "__main__":
    main()
