import utils
# this code can be use to normalize description field in it_jobs.jsonl
posts = utils.read_jsonl("normalized_data/it_jobs.jsonl")

tmp = []
sep = r"[\n]"
for post in posts:
    if "benefits" not in post:
        post["benefits"] = []
    elif isinstance(post["benefits"], str):
        post["benefits"] = post["benefits"].split("\n")
        post["benefits"] = [utils.process_string(b) for b in post["benefits"]]
    elif isinstance(post["benefits"], list):
        post["benefits"] = [utils.process_string(b) for b in post["benefits"]]

utils.write_jsonl("normalized_data/it_jobs.jsonl", posts)
