from bertopic import BERTopic
import utils
from sklearn.feature_extraction.text import CountVectorizer
from underthesea import word_tokenize
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance, OpenAI
import openai

def get_requirements(data):
    res = []
    for row in data:
        if("requirements" in row):
            res += list(row['requirements'].split("\n"))
    return res
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

def get_topics():
    data = utils.read_jsonl("normalized_data/it_jobs.jsonl")
    reqs = get_requirements(data)
    
    model = BERTopic.load("large_files/requirment_topic_model")
    
    vectorizer = CountVectorizer(ngram_range=(1, 2), tokenizer=word_tokenize)
    
    rep_type = ["keybert", {"type": "mrm", "args": {"diversity": 0.6}}, "gpt"]
    reps_model = get_representation_model(rep_type)

    model.update_topics(reqs, vectorizer_model = vectorizer, representation_model = reps_model)
    topics = model.get_topic_info()
    utils.df_to_jsonl(topics, "large_files/topics.jsonl")

import time
if __name__ == "__main__":
    start_time = time.time()
    get_topics()
    print("Compute topic takes --- %s seconds ---" % (time.time() - start_time))