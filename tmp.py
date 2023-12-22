import utils

col_name = 'requirements'
posts = utils.read_jsonl("normalized_data/it_jobs.jsonl")
# vals1, post_id = utils.get_requirements(posts, return_post_id=True)

def split_string(text):
    text = text.replace('--', '\n')
    text = text.split('\n')
    return text
        
def normalize_data_by_col(data, col_name):
    tmp = []
    for post in data:
        if col_name not in post:
            post[col_name] = []
        elif isinstance(post[col_name], str):
            post[col_name] = split_string(post[col_name])
            post[col_name] = [utils.process_string(b) for b in post[col_name]]
        elif isinstance(post[col_name], list):
            post[col_name] = [utils.process_string(b) for b in post[col_name]]
    return data
            
def filter_col_value_by_len(data, col_name):
    for post in data:
        tmp = []
        for val in post[col_name]:
            if utils.filter_by_length(val):
                tmp.append(val)
        post[col_name] = tmp 
    return data
# # tmp = [doc for post in posts for doc in post[col_name]]
# # utils.write_json('test.json', tmp)
# utils.write_jsonl("normalized_data/it_jobs.jsonl", posts)
posts = normalize_data_by_col(posts, col_name)
posts = filter_col_value_by_len(posts, col_name)

# id = []
# for i, post in enumerate(posts):
#     id += [i] * len(post[col_name])

# print(len(id))
# print(len(post_id))

# vals = [doc for post in posts for doc in post[col_name]]
# # utils.write_json('test.json', vals)

# for i in range(len(id)):
#     if id[i] != post_id[i]:
#         import pdb; pdb.set_trace()
utils.write_jsonl("normalized_data/it_jobs.jsonl", posts)