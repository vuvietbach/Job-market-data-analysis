from bertopic import BERTopic
import pandas as pd
import time
start_time = time.time()
df = pd.read_json('it_jobs.jsonl', lines=True)
reqs = df['requirements'].tolist()
tmp = []
for req in reqs:
    try:
        if isinstance(req, str):
            req = req.split('\n')
        tmp += req
    except:
        continue
docs = tmp
topic_model = BERTopic(language="multilingual", calculate_probabilities=True, verbose=True)
topics, probs = topic_model.fit_transform(docs)
topic_model.save("saved_model_all", serialization="safetensors", save_ctfidf=True)
print("--- %s seconds ---" % (time.time() - start_time))