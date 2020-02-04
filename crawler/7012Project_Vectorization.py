import pandas as pd
import numpy as np
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

corpus = ['The sky is blue and beautiful.',
          'Love this blue and beautiful sky!',
          'The quick brown fox jumps over the lazy dog.',
          "A king's breakfast has sausages, ham, bacon, eggs, toast and beans",
          'I love green eggs, ham, sausages and bacon!',
          'The brown fox is quick and the blue dog is lazy!',
          'The sky is very blue and the sky is very beautiful today',
          'The dog is lazy but the brown fox is quick!']
corpus = np.array(corpus)

# -------------------------text normalization-----------------------
wpt = nltk.WordPunctTokenizer()
stop_words = nltk.corpus.stopwords.words('english')


def normalize_document(doc):
    doc = re.sub(r'[^a-zA-Z\s]', '', doc)
    doc = doc.lower()
    doc = doc.strip()
    tokens = wpt.tokenize(doc)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    doc = ' '.join(filtered_tokens)
    return doc


# -------------------------bag of words-------------------------


# -------------------------tf-idf-------------------------
def tf_idf(cv, cv_matrix):
    tt = TfidfTransformer(norm='l2', use_idf=True)
    tt_matrix = tt.fit_transform(cv_matrix)
    tt_matrix = tt_matrix.toarray()
    vocab = cv.get_feature_names()
    return pd.DataFrame(np.round(tt_matrix, 2), columns=vocab)


def Vectorization(corpus, method="tfidf"):
    if method not in ["tfidf", "count", "binary"]:
        return "Error input of parameter"
    # Normalize Corpus
    normalize_corpus = np.vectorize(normalize_document)
    norm_corpus = normalize_corpus(corpus)

    # Bag of Words
    cv = CountVectorizer(min_df=0., max_df=1.)
    cv_matrix = cv.fit_transform(norm_corpus)
    cv_matrix = cv_matrix.toarray()
    vocab = cv.get_feature_names()
    cv_matrix = pd.DataFrame(cv_matrix, columns=vocab)

    # Feature Engineering Models
    if method == "tfidf":
        result = tf_idf(cv, cv_matrix)
    elif method == "count":
        result = cv_matrix
    elif method == "binary":
        result = np.logical_or(np.zeros(np.shape(cv_matrix)), cv_matrix) + 0
    return result

print(Vectorization(corpus, "tfidf"))
# Vectorization(corpus, "count")
# Vectorization(corpus, "binary")
# Vectorization(corpus, "test")

