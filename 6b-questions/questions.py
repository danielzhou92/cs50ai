import operator
import math
import string
import os
import sys
import nltk

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
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_dict = dict()

    for item in os.scandir(directory):
        if item.is_file():
            file = open(item.path, 'r')
            file_content = file.read()
            file_dict[item.name] = file_content
            file.close()

    return file_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # stratigy here is to first take out all the punctuations
    trans_table = str.maketrans('', '', string.punctuation)
    document_no_punkt = document.translate(trans_table)

    # then tokenize the lowercased string
    # technically this also filters out the punktuations,
    # but will let periods through if they are directly followed by another word, like "123.txt"
    tokens = nltk.word_tokenize(document_no_punkt.lower())

    # then remove any token that is a stopword
    stop_words = nltk.corpus.stopwords.words("english")
    filtered_tokens = [w for w in tokens if w not in stop_words]

    return filtered_tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_freq_count_dict = dict()
    idf_dict = dict()
    total_docs_count = len(documents.keys())

    # first convert the list of words for each document into a set to make the words unique
    # check if the word is in the idf_dict (means it had shown up in a previous document),
    # if it is, then add one to the count, if not then set the count to 1
    for words_list in documents.values():
        words_set = set(words_list)
        for word in words_set:
            if word in word_freq_count_dict.keys():
                word_freq_count_dict[word] += 1
            else:
                word_freq_count_dict[word] = 1

    # calculate the idf values
    for word, docs_with_word_count in word_freq_count_dict.items():
        idf_dict[word] = math.log(total_docs_count / docs_with_word_count)

    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf_dict = dict()

    for file_name, file_words in files.items():
        tf_idf_dict[file_name] = 0
        for query_word in query:
            tf_idf = file_words.count(query_word) * idfs[query_word]
            tf_idf_dict[file_name] += tf_idf

    sorted_files = sorted(tf_idf_dict.items(),
                          key=operator.itemgetter(1), reverse=True)

    return [item[0] for item in sorted_files[:n]]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentences_tuples = list()

    for sent_name, sent_words in sentences.items():
        sent_idf = 0
        words_found = 0
        for query_word in query:
            if query_word in sent_words:
                sent_idf += idfs[query_word]
                words_found += 1

        query_density = words_found / len(sent_words)
        sentences_tuples.append((sent_name, sent_idf, query_density))

    sentences_tuples.sort(key=operator.itemgetter(1, 2), reverse=True)

    return [item[0] for item in sentences_tuples[:n]]


if __name__ == "__main__":
    main()
