# This is a mess, because it is a converted jupyter notebook
import json
import pickle
from random import random

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

# Reading the tables and concatenating them
print("Reading tables")
pol = pd.read_csv("data/Political_tweets.csv")
gen = pd.read_csv(
    "data/training.1600000.processed.noemoticon.csv", encoding="ISO-8859-1", header=None
)
gen.columns = ["target", "id", "date", "flag", "user", "text"]
pol["class"] = 1
gen["class"] = 0
p_clean = (
    lambda x: x.replace("#politics", "").replace("#POLITICS", "")
    if random() < 0.8
    else x
)
pol.text = pol.text.apply(p_clean)
tables_dataset = (
    pol[["text", "class"]].iloc[:160_000],
    gen[["text", "class"]].iloc[:200_000],
)
tables_generation = (
    pol[["text", "class"]].iloc[160_000:],
    gen[["text", "class"]].iloc[200_000:400_000],
)

print("Preparing the data")
dataset_df = pd.concat(tables_dataset)
generation_df = pd.concat(tables_generation)
print("Dumping random static")
texts = list(generation_df.text)
users = list(gen.user)
json.dump({"texts": texts, "users": users}, open("static/static.json", "w"))


# making static for generation


# Making the dataset
print("Shuffling the datasets")
positions = np.arange(0, len(dataset_df))
np.random.shuffle(positions)

l = len(dataset_df)
train_idx = positions[0 : int(l * 0.6)]
val_idx = positions[int(l * 0.6) : int(l * 0.8)]
test_idx = positions[int(l * 0.8) :]
train_df = dataset_df.iloc[train_idx]
val_df = dataset_df.iloc[val_idx]
test_df = dataset_df.iloc[test_idx]


print("Training the model")
vectorizer = CountVectorizer()
tfidf = TfidfTransformer()
clf = LogisticRegression(max_iter=10000)

pipeline = Pipeline(
    [
        ("vec", vectorizer),  # strings to token integer counts
        ("tfidf", tfidf),  # integer counts to weighted TF-IDF scores
        ("classifier", clf),  # train on TF-IDF vectors
    ]
)

pipeline.fit(train_df["text"], train_df["class"])
pred = pipeline.predict(test_df["text"])
print(classification_report(test_df["class"], pred))
print("Dumping the model")
pickle.dump(pipeline, open("classifier/classifier.pkl", "wb"))

print("Most important tokens in our linear model")
id2word = {v: k for k, v in vectorizer.vocabulary_.items()}
s = list(reversed(clf.coef_.argsort().tolist()[0]))
for i in range(100):
    print(id2word[s[i]], end=", ")
