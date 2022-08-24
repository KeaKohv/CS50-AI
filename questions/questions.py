import nltk
import sys
import os
import string
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
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    # Create a dictionary to map filenames to their contents as strings
    filename_mapping_txt = dict()

    # Read in each txt file in the directory and save to the dictionary
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), "r", encoding='utf8') as f:
            contents = f.read()
            filename_mapping_txt[file] = contents
        
    return filename_mapping_txt


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    # Create a list for the words in the document
    list_of_words = []

    # Convert the document string into lowercase
    document = document.lower()

    # Tokenize, i.e. convert the string into words in a list
    words = nltk.tokenize.word_tokenize(document)

    # Go through each word in the document
    for word in words:

        # If the word is a stopword, it is not added to the words list
        if word in nltk.corpus.stopwords.words('english'):
            continue

        # Also, if the word consist only of punctuation characters, it is not added to the words list
        else:
            punctuation = True
            for character in word:
                if character not in string.punctuation:
                    punctuation = False
                    break

            if not punctuation:
                list_of_words.append(word)

    return list_of_words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # Create a dict to map words to IDF values
    words_IDF = dict()

    # Go through the content of each document and count in how many files each word appears
    for filename in documents:

        # Create a helper set for keeping track of the unique words in each of the document
        unique_words = set()

        for word in documents[filename]:

            # Add the word into the unique words set if it is not there already
            if word not in unique_words:
                unique_words.add(word)

                # Increase the count of the word in the dictionary by one, marking that it appeared in
                # the document
                if word not in words_IDF:
                    words_IDF[word] = 1
                else:
                    words_IDF[word] += 1

    # Update the IDF values in the dictionary
    # The inverse document frequency (IDF) of a word is defined by taking the natural logarithm
    # of the number of documents divided by the number of documents in which the word appears.
    nr_of_documents = len(documents)
    for word in words_IDF.keys():
        how_many_docs = words_IDF[word]
        words_IDF[word] = math.log(nr_of_documents/how_many_docs)

    return words_IDF


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the `n` top
    files that match the query, ranked according to tf-idf.
    """

    # Create a dictionary to keep track of the file scores
    file_scores = dict()

    # Go through each file list of words to get the combined tf-idf for the query
    for file in files:

        # Initalize the combined tf_idf for the query (for each file) as 0
        tf_idf = 0

        # Tf-idf for a term is computed by multiplying the number of times the term appears
        # in the document by the IDF value for that term. Here the tf-idf is combined for the whole query.
        for word in query:
            tf_idf += files[file].count(word) * idfs[word]

        # Save the file score to the file_scores dictionary
        file_scores[file] = tf_idf

    # Create a new dictionary for sorted files according to the tf-idf of each file
    top_files = sorted(file_scores.items(), key=lambda item: item[1], reverse=True)

    # Return the first n filenames, tf-idf values are not returned
    return [x[0] for x in top_files[:n]]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    # Initialize an empty list to store sentences and their respective idfs and query term density values
    sentences_ratings = []

    # Go through all sentences, calculate their idfs and query term density values
    for sentence, sentence_words in sentences.items():
        idf = 0
        query_words_in_sentence = 0

        for word in query:
            if word in sentence_words:
                idf += idfs[word]
                query_words_in_sentence += 1

        # Query term density is the proportion of words in the sentence that are also words in the query. 
        query_term_density = float(query_words_in_sentence)/len(sentence_words)

        sentences_ratings.append((sentence, idf, query_term_density))
    
    # Sort the sentences
    sentences_ratings.sort(key=lambda item: (item[1], item[2]), reverse=True)

    # Return a list of the n top sentences. The ratings themselves are excluded.
    return [item[0] for item in sentences_ratings[:n]]


if __name__ == "__main__":
    main()
