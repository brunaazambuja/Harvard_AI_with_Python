import nltk
import sys
import os
import string
import math

nltk.download('punkt')


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

    while(True):
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
    files = dict()


    for file in os.listdir(directory):
        with open(os.path.abspath(os.path.join(directory, file))) as f:
            files[file] = f.read()
    
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(document)
    stopwords = nltk.corpus.stopwords.words('english')

    lower = []

    for word in words:
        lower.append(word.lower())


    for word in lower.copy():
        if (word in string.punctuation or word in stopwords):
            lower.remove(word)


    return lower



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    wordCounter = dict()

    for file in documents:
        for word in documents[file]:
            if (word not in wordCounter):
                wordCounter[word] = 0
    
    for word in wordCounter:
        for file in documents:
            if (word in documents[file]):
                wordCounter[word] += 1

        wordCounter[word] = math.log(len(documents)/wordCounter[word])

    return wordCounter


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the `n` top
    files that match the query, ranked according to tf-idf.
    """
    filenames = dict()

    for file in files:
        filenames[file] = 0

    for word in query:
        for file in files:
            for word2 in files[file]:
                if (word == word2):
                    filenames[file] += idfs[word]
    
    sortedDict = dict()
    for key, value in sorted(filenames.items(), key=lambda item: item[1], reverse=True):
        sortedDict[key] = value

    result = []
    count = 0

    for key in sortedDict.keys():
        result.append(key)
        count += 1
        if (n == count):
            return result



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    def calculate_term_dens(sentence, query):
        counter = 0
        for word in sentence:
            if (word in query):
                counter += 1
        counter /= len(sentence)
        return counter


    

    topSentences = dict()

    for sentence in sentences:
        topSentences[sentence] = 0

    for word in query:
        for sentence in sentences:
            if (word in sentences[sentence]):
                topSentences[sentence] += idfs[word]

    sortedDict = dict()
    for key, value in sorted(topSentences.items(), key=lambda item: item[1], reverse=True):
        sortedDict[key] = value

    for i in range(n - 1):
        if (sortedDict[i][1] == sortedDict[i+1][1]):
            first = calculate_term_dens(sortedDict[i][0], query)
            second = calculate_term_dens(sortedDict[i+1][0], query)
            if (second > first):
                sortedDict[i], sortedDict[i+1] = sortedDict[i+1], sortedDict[i]    

    result = []
    count = 0

    for key in sortedDict.keys():
        result.append(key)
        count += 1
        if (n == count):
            return result



if __name__ == "__main__":
    main()
