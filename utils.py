from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import time
from bertopic import BERTopic
import os
import json


def plot_wordcloud(word_list, save_path=None):
    counter = dict(Counter(word_list))
    wc = WordCloud(background_color="white").generate_from_frequencies(counter)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


def get_jobs_by_positions(jobs, categories, positions):
    """
    jobs: list of jobs postings
    categories: list of category for each job posting, type: string
    positions: list of  query job positions

    """
    positions = [f"({p})" for p in positions]
    pattern = "|".join(positions)
    jobs_id = [
        i
        for i, category in enumerate(categories)
        if re.search(pattern, category, re.IGNORECASE)
    ]
    jobs = [jobs[i] for i in jobs_id]
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


def train_topic_model(docs, save_model_dir=None):
    start_time = time.time()
    topic_model = BERTopic(
        language="multilingual", calculate_probabilities=True, verbose=True
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
