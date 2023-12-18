from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import time
from bertopic import BERTopic
import os
import json
import numpy as np
from underthesea import word_tokenize
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance, OpenAI
import openai
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from underthesea import word_tokenize
def plot_wordcloud(word_list, save_path=None, return_counter=False):
    counter = dict(Counter(word_list))
    wc = WordCloud(background_color="white").generate_from_frequencies(counter)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
    if return_counter:
        return counter


def get_jobs_by_type(jobs, positions, return_id=False):
    """
    jobs: list of jobs postings
    positions: list of  query job positions
    """
    categories = get_category_str(jobs)
    positions = [f"({p})" for p in positions]
    pattern = "|".join(positions)
    jobs_id = [
        i
        for i, category in enumerate(categories)
        if re.search(pattern, category, re.IGNORECASE)
    ]
    jobs = [jobs[i] for i in jobs_id]
    if return_id:
        return jobs, jobs_id
    else:
        return jobs


def plot_skills_wordcloud(data, save_path=None):
    def process_skill(tmp, skill):
        if skill == "nan" or skill is None or not isinstance(skill, str):
            return
        skill = list(skill.split(","))
        skill = [s.strip() for s in skill]
        skill = [s.lower() for s in skill]
        tmp.extend(skill)

    # get skills
    skills = [j.get("skills", None) for j in data]
    tmp = []
    for skill in skills:
        process_skill(tmp, skill)
    skills = tmp

    plot_wordcloud(skills, save_path)


def read_it_jobs_txt(path):
    with open(path, "r") as f:
        data = f.readlines()
    data = [row.strip() for row in data]
    data = [row.split(">") for row in data]
    data = [[i.strip() for i in row] for row in data]
    return data


def train_topic_model(docs, save_model_dir=None, **kwargs):
    start_time = time.time()
    topic_model = BERTopic(
        **kwargs, language="multilingual", calculate_probabilities=True, verbose=True
    )
    topics, probs = topic_model.fit_transform(docs)
    if save_model_dir is not None:
        os.makedirs(save_model_dir, exist_ok=True)
        topic_model.save(save_model_dir, serialization="safetensors", save_ctfidf=True)
    print("Compute topic takes --- %s seconds ---" % (time.time() - start_time))
    return {"model": topic_model, "topics": topics, "probs": probs}


def get_it_job_types(path):
    # path: path to txt file where each line hold a type of it job
    with open(path, "r") as f:
        jobs = f.readlines()
        jobs = [job.strip().split(">") for job in jobs]
        jobs = [[i.strip() for i in job] for job in jobs]
        positions = jobs
    return positions


def write_jsonl(file_path, data):
    with open(file_path, "w", encoding="utf8") as f:
        for line in data:
            json.dump(line, f, ensure_ascii=False)
            f.write("\n")


class BertTopic:
    def load_model(path):
        return BERTopic.load(path, serialization="safetensors")


def read_jsonl(file_path):
    with open(file_path, "r") as f:
        data = [json.loads(line) for line in f]
    return data


def df_to_jsonl(df, file_path):
    data = df.to_dict(orient="records")
    write_jsonl(file_path, data)


def load_embeddings(file_path):
    with open(file_path, "rb") as f:
        embeddings = np.load(f)
    return embeddings

def remove_multiple_spaces(text):
    return re.sub(r"\s+", " ", text)

def remove_punctuation(text, replace_with_space=False):
    if replace_with_space:
        return re.sub(r"[^\w\s-]", " ", text)
    else:
        return re.sub(r"[^\w\s-]", "", text)

def filter_by_length(text, min_len=4):
    return len(text.split(" ")) >= min_len

def process_string(text):
    text = text.lower()
    text = remove_punctuation(text, replace_with_space=True)
    text = remove_multiple_spaces(text)
    text = text.strip()
    return text

def get_requirements(data, return_post_id=False):
    # separate by new line
    # separate by --
    # remove punctuation
    # filte by length, minimum length 4
    def process_req(req):
        req = req.lower()
        req = remove_punctuation(req)
        req = remove_multiple_spaces(req)
        req = req.strip()
        if filter_by_length(req):
            return req
        else:
            return None
    
    def process(req_str):
        res = []
        reqs = req_str.split("\n")
        for req in reqs:
            req = req.split("--")
            req = [process_req(i) for i in req]
            req = [i for i in req if i is not None]
            res += req
        return res
    
    res = []
    req_post_id = []
    for i, row in enumerate(data):
        if "requirements" in row:
            req = process(row["requirements"])
            res += req
            req_post_id += [i] * len(req)
    if return_post_id:
        return res, req_post_id
    else:
        return res

def get_category_str(jobs):
    categories = []
    for job in jobs:
        if('category' not in job):
            categories.append("")
        else:
            if(isinstance(job['category'], str)):
                categories.append(job['category'])
            elif(isinstance(job['category'], list)):
                categories.append(" ".join(job['category']))
            else:
                categories.append("")
    return categories

def get_representation_model(types):
    res = {}
    for i in types:
        if isinstance(i, str):
            model_type = i
            args = {}
        elif isinstance(i, dict):
            model_type = i['type']
            args = i['args']
        
        assert isinstance(args, dict)
        
        if(model_type == "keybert"):
            res[model_type] = KeyBERTInspired(**args)
        elif(model_type == "mrm"):
            res[model_type] = MaximalMarginalRelevance(**args)
        elif(model_type == 'gpt'):
            client = openai.OpenAI(api_key="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")
            prompt = """
            I have a topic that contains the following documents:
            [DOCUMENTS]
            The topic is described by the following keywords: [KEYWORDS]

            Based on the information above, extract a short but highly descriptive topic label of at most 5 words. Make sure it is in the following format:
            topic: <topic label>
            """
            client = openai.OpenAI(api_key="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")
            openai_model = OpenAI(client, model="gpt-3.5-turbo", exponential_backoff=True, chat=True, prompt=prompt)
            res[model_type] = openai_model
    return res

def save_embeddings(embeddings, path):
    with open(path, 'wb') as f:
        np.save(f, embeddings)

def save_topic_info(topic_info, path):
    df_to_jsonl(topic_info, path)

def debug_req(reqs):
    jobs = read_jsonl("normalized_data/it_jobs.jsonl")
    reqs = get_requirements(jobs)
    reqs1 = [(i, len(i)) for i in reqs]
    reqs1 = sorted(reqs1, key=lambda x : x[1])
    reqs = [i[0] for i in reqs1]
    reqs = "\n############\n".join(reqs)
    with open("req.txt", 'w') as f:
        f.write(reqs)

def get_topics_by_job_type(id, job_posts, post_docs, doc_topic):
    '''
    return: topics dict where key: id of topic, value: count of the topic
    '''
    topics = []
    for post in job_posts[id]:
        for doc in post_docs[post]:
            topics.append(doc_topic[doc])

    freq = dict(Counter(topics))
    freq = [{'id': k, 'count': v} for k, v in freq.items()]
    return freq

def filter_topics(topics):
    '''
    get top 10 topics by frequency
    '''
    res = sorted(topics, key=lambda x : x['count'])
    res = [i for i in res if i['id']!=-1]
    res = res[-30:]
    return res

def get_topics(docs, save_model_dir=None, use_gpt=False, **kwargs):
    start_time = time.time()

    vectorizer = CountVectorizer(ngram_range=(1, 2), tokenizer=word_tokenize)
    
    rep_models = ["keybert", {"type": "mrm", "args": {"diversity": 0.6}}]
    if use_gpt:
        rep_models.append("gpt")

    rep_model = get_representation_model(rep_models)  

    embedding_model_name = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    embedding_model = SentenceTransformer(embedding_model_name)


    topic_model = BERTopic(
            embedding_model=embedding_model,
            vectorizer_model=vectorizer,
            representation_model=rep_model,
            verbose=True
    )
    
    topics, _ = topic_model.fit_transform(docs)
    if save_model_dir is not None:
        os.makedirs(save_model_dir, exist_ok=True)
    else:
        save_model_dir = "large_files/topic_model"
    topic_model.save(save_model_dir, serialization="safetensors", save_ctfidf=True)
   
    with open("topics.json", 'w') as f:
        json.dump(topics, f)
    print("Compute topic takes --- %s seconds ---" % (time.time() - start_time))

import math
def is_nan(value):
    try:
        if value is None:
            return True
        return math.isnan(float(value))
    except:
        return False