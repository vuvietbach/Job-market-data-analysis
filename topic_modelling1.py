
from bertopic import BERTopic
import utils
from collections import Counter
import time
start_time = time.time()

# In[114]:


jobs = utils.read_jsonl("normalized_data/it_jobs.jsonl")
reqs, req_post_id = utils.get_requirements(jobs, return_post_id=True)


# In[115]:


topic_model = BERTopic.load("large_files/requirment_topic_model")
topics, _ = topic_model.transform(reqs)
doc_topic = topics


# In[ ]:


topic_info = utils.read_jsonl("test.jsonl")


# In[ ]:


post_docs = {}
for i, post_id in enumerate(req_post_id):
    if post_id not in post_docs:
        post_docs[post_id] = []
    post_docs[post_id].append(i)
    


# In[ ]:


job_types = utils.read_it_jobs_txt('normalized_data/it_jobs.txt')


# In[ ]:


job_posts = {}
for i in range(len(job_types)):
    _, id = utils.get_jobs_by_positions(jobs, job_types[i], return_id=True)
    job_posts[i] = id


# In[ ]:


def get_topics_by_job_type(id, job_posts, post_docs, doc_topic, return_count=False):
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
    res = topics[:10] + topics[-10:]
    return res


# In[ ]:


# type_id = 8
# print(job_types[type_id])
# topic_ids = get_topics_by_job_type(type_id, job_posts, post_docs, doc_topic)
# topic_ids = filter_topics(topic_ids)


# In[ ]:


res = []
id = 0
for post in job_posts[id]:
    for doc in post_docs[post]:
        res.append({"category": jobs[post].get('category'), "requirement": reqs[doc], "topic": topic_info[doc_topic[doc]]['keybert']})
utils.write_jsonl("test1.jsonl", res)


print("Compute topic takes --- %s seconds ---" % (time.time() - start_time))