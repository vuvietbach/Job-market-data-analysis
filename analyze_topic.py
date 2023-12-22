from collections import Counter
import utils
import json
import os


    
def sort_dict_by_value(d):
    return dict(sorted(d.items(), key=lambda x: x[1]))

class TopicModel:
    
    def __init__(self, cfg):
        self.data = utils.Data()
        self.col_name = cfg['col_name']
        
        # job keywords
        self.job_kws = utils.read_json("normalized_data/job_keywords.json")
        self.job_names = list(self.job_kws.keys())
        
        # job_posts
        self.get_type_posts()
        
        # post_docs
        self.get_post_docs()
        
        # doc_topic
        input_path = cfg['topic_prediction_path']
        with open(input_path, 'r') as f:
            self.doc_topic = json.load(f)
        
        # topics
        input_path = cfg['topic_info_path']
        with open(input_path, 'r') as f:
            self.topics = json.load(f)
        
        
    def get_topic_by_type(self, job_id):
        assert isinstance(job_id, int) or isinstance(job_id, str)
        
        if isinstance(job_id, int):
            job_id = self.job_names[job_id]
            topics = []
        for post in self.type_posts[job_id]:
            if post not in self.post_docs:
                continue
            for doc in self.post_docs[post]:
                topics.append(self.doc_topic[doc])

        freq = dict(Counter(topics))
        return freq
    
    def get_topic_info(self, topic_ids):
        return [self.topics[i+1]['gpt'] for i in topic_ids]
    
    def filter_topic_by_freq(self, freq, ntop=10):
        res = dict(sorted(freq.items(), key=lambda x: x[1]))
        topic_ids = list(res.keys())[-ntop:]
        topic_infos = [self.topic_info[i]['gpt'] for i in topic_ids]
        return topic_infos
    
    def get_type_posts(self):
        self.type_posts = {}
        for job_type in self.job_names:
            self.type_posts[job_type] = self.data.get_post_by_type(job_type)
    
    def get_post_docs(self):
        post_docs = {}
        _, post_ids = self.data.get_col_values(self.col_name)
        for i, id in enumerate(post_ids):
            if id not in post_docs:
                post_docs[id] = []
            post_docs[id].append(i)
        self.post_docs = post_docs
        # utils.write_json('tesxt.json', post_ids)

from argparse import ArgumentParser
def main():
    parser = ArgumentParser()
    parser.add_argument('--col_name', type=str)
    parser.add_argument('--topic_prediction_path', type=str)
    parser.add_argument('--topic_info_path', type=str)
    args = parser.parse_args()
    cfg = {
        'col_name': args.col_name,
        'topic_prediction_path': args.topic_prediction_path,
        'topic_info_path': args.topic_info_path
    }
    # parser.add_argument('--config', type=str, default='config.json')
    model = TopicModel(cfg)
    
    job_kws = utils.read_json("normalized_data/job_keywords.json")
    job_names = list(job_kws.keys())

    save_dir = 'test'
    topk = 20
    os.makedirs(save_dir, exist_ok=True)
    for i in range(len(job_names)):
        topic_cnt = model.get_topic_by_type(i)
        topic_cnt = sort_dict_by_value(topic_cnt)
        topic_cnt = dict(list(topic_cnt.items())[-topk:])
        topic_info = model.get_topic_info(list(topic_cnt.keys()))
        save_path = os.path.join(save_dir, job_names[i]+'.json')
        utils.write_json(save_path, topic_info)

if __name__ == '__main__':
    main()
    

