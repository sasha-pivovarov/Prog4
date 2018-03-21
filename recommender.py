from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import LatentDirichletAllocation, NMF, TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
import pickle
import re
from itertools import combinations
import numpy as np
from pathlib import Path
from sklearn.metrics import pairwise
from sklearn.neighbors import NearestNeighbors
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer("english")
stem_list = lambda x: [stemmer.stem(y) for y in x]
class NewsRecommender:
    """
    обучить систему на корпусе текстов  с помощью тематической модели и метрики, выбранных в результате исследования
    """

    def __init__(self):
        self.model = None
        self.vectorizer = TfidfVectorizer(min_df=0.1, max_df=0.5)
        self.w2v = None
        self.texts = None
        self.textmatrix = None
        self.neighbors = NearestNeighbors(metric=pairwise.cosine_distances)

    def train(self, texts):
        self.texts = texts.data
        w2v_path = Path("w2v-model.bin")
        stemmed_texts = [" ".join(stem_list(x.split())) for x in self.texts]
        topic_range = range(4, 25)
        tfidfs = self.vectorizer.fit_transform(stemmed_texts)
        fnames = self.vectorizer.get_feature_names()
        if not w2v_path.is_file():
            docgen = TokenGenerator(stemmed_texts, [])
            w2v_model = Word2Vec(docgen, size=500, min_count=20, sg=1)
        else:
            w2v_model = Word2Vec.load("w2v-model.bin")

        self.w2v = w2v_model
        print("Model has %d terms" % len(w2v_model.wv.vocab))
        w2v_model.save("w2v-model.bin")
        # texts = fetch_20newsgroups()
        best_model = None
        best_score = 0
        best_matrix = None

        for i in topic_range:
            lda_name = Path("lda_%d.pkl" % i)
            nmf_name = Path("nmf_%d.pkl" % i)
            if not lda_name.is_file():
                lda = LatentDirichletAllocation(n_components=i, learning_method="batch")
                W_lda = lda.fit_transform(tfidfs)
                with open(lda_name, "wb") as io:
                    pickle.dump(lda, io)
            else:
                with open(lda_name, "rb") as io:
                    lda = pickle.load(io)
                    W_lda = lda.transform(tfidfs)

            H_lda = lda.components_
            if not nmf_name.is_file():
                nmf = NMF(n_components=i, init="nndsvda")
                W_nmf = nmf.fit_transform(tfidfs)
                with open(nmf_name, "wb") as io:
                    pickle.dump(nmf, io)
            else:
                with open(nmf_name, "rb") as io:
                    nmf = pickle.load(io)
                    W_nmf = nmf.transform(tfidfs)


            H_nmf = nmf.components_
            term_rankings_lda = [get_descriptor(fnames, H_lda, x, 10) for x in range(0, i)]
            term_rankings_nmf = [get_descriptor(fnames, H_nmf, x, 10) for x in range(0, i)]
            lda_score = tcw2c(self.w2v, term_rankings_lda)
            nmf_score = tcw2c(self.w2v, term_rankings_nmf)

            if lda_score > nmf_score and lda_score > best_score:
                best_score = lda_score
                best_model = lda
                best_matrix = W_lda
            elif nmf_score > lda_score and nmf_score > best_score:
                best_score = nmf_score
                best_model = nmf
                best_matrix = W_nmf
            print("Evaluated model with i="+str(i))
        print("Found best model:")
        self.model = best_model
        self.textmatrix = best_matrix
        print(type(best_model))
        #print(best_model.n_components_)
        print(best_score)

    """
    выдать k самых пожих новостей для заданного заголовка по функции расстояния, выбранной в результате исследования
    обратите внимание, что text_sample может содержать слова не из обучающего корпуса
    """

    def recommend(self, text_sample, k):
        print("Recommending...")
        sample_vecspace = self.vectorizer.transform([" ".join(stem_list(text_sample.split()))])
        reduced_vecspace = self.model.transform(sample_vecspace)
        distances = pairwise.cosine_distances(reduced_vecspace, self.textmatrix)
        dist_list = []
        for i in range(len(distances[0])):
            dist_list.append((i , distances[0][i]))
        dist_list = sorted(dist_list, key=lambda x: x[1])
        

        return [(x[0], self.texts[x[0]]) for x in dist_list[:k]]


def tcw2c(w2v_model, term_rankings):
    overall_coherence = 0.0
    for topic_index in range(len(term_rankings)):
        pair_scores = []
        for pair in combinations(term_rankings[topic_index], 2):
            try:
                pair_scores.append( w2v_model.similarity(pair[0], pair[1]) )
            except KeyError:
                continue
        topic_score = sum(pair_scores) / len(pair_scores)
        overall_coherence += topic_score
    return overall_coherence / len(term_rankings)


def get_descriptor(terms, H, topic_index, top):
    top_indices = np.argsort(H[topic_index, :])#[::-1]
    top_terms = []
    for term_index in top_indices[0:top]:
        top_terms.append(terms[term_index])
    return top_terms


class TokenGenerator:
    def __init__(self, documents, stopwords):
        self.documents = documents
        self.stopwords = stopwords
        self.tokenizer = re.compile(r"(?u)\b\w\w+\b")

    def __iter__(self):
        for doc in self.documents:
            tokens = []
            for tok in self.tokenizer.findall(doc):
                if tok in self.stopwords:
                    tokens.append("<stopword>")
                elif len(tok) >= 2:
                    tokens.append(tok)
            yield tokens


rec = NewsRecommender()
texts = fetch_20newsgroups()
rec.train(texts)
recs = rec.recommend("""
Nelson was born and raised in Salt Lake City, Utah. He attended the University of Utah for his undergraduate and medical school education, then did further surgical training and earned a Ph.D. at the University of Minnesota. He served for two years in the U.S. Army Medical Corps during the Korean War, then did additional surgical training at Harvard Medical School via Massachusetts General Hospital. In 1955, Nelson returned to Salt Lake City and accepted a professorship at the University of Utah School of Medicine. Nelson spent the next 29 years at Utah working in the field of cardiothoracic surgery and serving in a variety of LDS Church leadership positions, beginning locally and then as the LDS Church's Sunday School General President from 1971 to 1979.[5] Nelson became a renowned heart surgeon, and served as president of the Society for Vascular Surgery and the Utah Medical Association.[6]"""
                     , 5)

