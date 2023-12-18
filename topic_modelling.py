import utils
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from underthesea import word_tokenize
from bertopic import BERTopic
import json
import time
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

def main():
    data = utils.read_jsonl("normalized_data/it_jobs.jsonl")
    reqs = utils.get_requirements(data)
    # step 1: get embeddings
    
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    
    # # save embeddings
    # with open('large_files/requirement_embeddings/embeddings.npy', 'wb') as f:
    #     np.save(f, embeddings)
    # step 2: get topics
        
    # step 3: transform documents
    pass

if __name__ == "__main__":
    get_topics()