from bertopic import BERTopic
from argparse import ArgumentParser
import utils
import os
class Data:
    def __init__(self):
        self.data = utils.read_jsonl("normalized_data/it_jobs.jsonl")
    
    def get_col_values(self, col_name):
        row_ids = []
        res = []
        for i, row in enumerate(self.data):
            res += row[col_name]
            row_ids += [i] * len(row[col_name])
        return res, row_ids

def main():
    parser = ArgumentParser()
    parser.add_argument('--model_dir', type=str)
    parser.add_argument('--output_dir', type=str)
    parser.add_argument('--col_name', type=str)
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    model = BERTopic.load(args.model_dir, embedding_model='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    data = Data()
    docs, row_ids = data.get_col_values(args.col_name)
    
    topics, _ = model.transform(docs)
    topics = [i.item() for i in topics]
    save_path = os.path.join(args.output_dir, 'topic_prediction.json')
    utils.write_json(save_path, topics)
    
    topic_info = model.get_topic_info()
    topic_info = topic_info.to_dict(orient='records')
    save_path = os.path.join(args.output_dir, 'topic_info.json')
    utils.write_json(save_path, topic_info)

if __name__ == '__main__':
    main()