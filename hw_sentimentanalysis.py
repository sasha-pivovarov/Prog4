from sklearn.svm import SVC, LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import NMF
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
import numpy as np

SEED = 1337

df = pd.read_csv("Tweets.csv")

df.loc[df.airline_sentiment == 'negative', 'airline_sentiment'] = 0
df.loc[df.airline_sentiment == 'neutral', 'airline_sentiment'] = 1
df.loc[df.airline_sentiment == 'positive', 'airline_sentiment'] = 2
airline_le = LabelEncoder()
df['airline'] = airline_le.fit_transform(df.airline)
stemmer = SnowballStemmer("english")
df["text"] = df["text"].apply(lambda x: " ".join([stemmer.stem(y) for y in x.split()]))
print(df.head())

pipe = make_pipeline(TfidfVectorizer(), NMF(), LinearSVC())
params = {
          "tfidfvectorizer__min_df": [0.01, 0.1],
          "tfidfvectorizer__max_df": [0.6, 0.8],
          "tfidfvectorizer__sublinear_tf": [True, False],
          "tfidfvectorizer__use_idf": [True],
          "tfidfvectorizer__analyzer": ["word", "char"],
          "nmf__random_state": [SEED],
          "nmf__n_components": [1000, None],
          "linearsvc__random_state":[SEED],
          "linearsvc__C": [0.5, 1.0, 5.0]
          }
model = GridSearchCV(pipe, param_grid=params, verbose=True)

y = df.airline_sentiment.values
df_train, df_test, y_train, y_test = train_test_split(df, y, test_size=0.25, stratify=y, random_state=SEED, shuffle=True)

print("Fitting model...")
model.fit(df_train.text, y_train.astype(int))
print(model.best_params_)
y_pred = model.predict(df_test.text)
print(classification_report(y_test, y_pred))


