import utils
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from underthesea import word_tokenize
from bertopic import BERTopic
import json
import time
import os
def get_topics():
    start_time = time.time()
    data = utils.read_jsonl("normalized_data/it_jobs.jsonl")
    docs = utils.get_requirements(data)

    vectorizer = CountVectorizer(ngram_range=(1, 2), tokenizer=word_tokenize)
    
    rep_models = ["keybert", {"type": "mrm", "args": {"diversity": 0.6}}, "gpt"]
    rep_model = utils.get_representation_model(rep_models)  

    embedding_model_name = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    embedding_model = SentenceTransformer(embedding_model_name)


    topic_model = BERTopic(
            embedding_model=embedding_model,
            vectorizer_model=vectorizer,
            representation_model=rep_model,
            verbose=True
    )
    
    topics, _ = topic_model.fit_transform(docs)
    model_save_dir = "large_files/topic_model"
    topic_model.save(model_save_dir, serialization="safetensors", save_ctfidf=True)
   
    with open("topics.json", 'w') as f:
        json.dump(topics, f)
    print("Compute topic takes --- %s seconds ---" % (time.time() - start_time))

from argparse import ArgumentParser
def main():
    parser = ArgumentParser()
    parser.add_argument("--col_name", type=str)
    parser.add_argument("--save_dir", type=str)
    parser.add_argument("--result_save_dir", type=str)
    args = parser.parse_args()
    col_name = args.col_name
    start_time = time.time()
    data = utils.read_jsonl("normalized_data/it_jobs.jsonl")
    docs = [doc for post in data for doc in post[col_name]]

    vectorizer = CountVectorizer(ngram_range=(1, 2), tokenizer=word_tokenize)
    
    rep_models = ["keybert", {"type": "mrm", "args": {"diversity": 0.6}}, "gpt"]
    rep_model = utils.get_representation_model(rep_models)  

    embedding_model_name = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    embedding_model = SentenceTransformer(embedding_model_name)


    topic_model = BERTopic(
            embedding_model=embedding_model,
            vectorizer_model=vectorizer,
            representation_model=rep_model,
            verbose=True
    )
    
    topics, _ = topic_model.fit_transform(docs)
    
    model_save_dir = args.save_dir
    os.makedirs(model_save_dir, exist_ok=True)
    topic_model.save(model_save_dir, serialization="safetensors", save_ctfidf=True)

    result_save_dir = args.result_save_dir
    os.makedirs(result_save_dir, exist_ok=True)
    # with open(result_save_dir + "/topics.json", 'w') as f:
        

    print("Compute topic takes --- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()