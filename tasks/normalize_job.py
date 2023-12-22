import utils
import json
posts = utils.read_jsonl("normalized_data/it_jobs.jsonl")
with open("job_keywords.json", 'r') as f:
    job_kws = json.load(f)
    
for post in posts:
    job = post['job'].lower()
    for kw in job_kws:
        for k in job_kws[kw]:
            if k in job:
                post['normalized_job'] = kw
                break
    if 'normalized_job' not in post:
        post['normalized_job'] = 'other'
        
utils.write_jsonl("normalized_data/it_jobs_normalized.jsonl", posts)