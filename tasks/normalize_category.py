import utils
import re
posts = utils.read_jsonl("normalized_data/it_jobs.jsonl")
kws = ['manager', 'dev', 'qa', 'embedded', 'backend', 'leader', 'web', 'react', 'support', 'qc', 'python', 'lead', 'java', 'owner', 'ui', 'full']
kws = {
    0: ['cloud', 'devops', 'system'],
    1: ['ui', 'ux', 'designer'],
    2: ['hardware', 'embedded', ],
    3: ['web developer', 'software', 'phần mềm', 'developer', 'frontend', 'backend', 'react', 'java', 'python', 'full', 'lập trình viên', 'flutter', 'android', 'ios'],
    4: ['data', 'ai', 'machine learning', 'analyst'],
    5: ['owner', 'master', 'lead', 'leader', 'manager', 'giám đốc'],
    8: ['security'],
    11: ['test', 'qa', 'qc'],
}
kws_pattern = {}
for k in kws:
    kws_pattern[k] = [f"({i})" for i in kws[k]]
    kws_pattern[k] = '|'.join(kws_pattern[k])
jobs = utils.read_it_jobs_txt("normalized_data/it_jobs.txt")
jobs_str = ["_".join(job) for job in jobs]
jobs_pattern = []
for job in jobs:
    job = [f"({i})" for i in job]
    job = '|'.join(job)
    jobs_pattern.append(job)

new_posts = []
def get_category_for_nan(job):
    for i in kws_pattern:
        category = []
        pattern = kws_pattern[i]
        if re.search(pattern, job, re.IGNORECASE):
            category.append(jobs_str[i])
    if len(category) > 0:
        return category
    return ["other"]

def get_category_for_normal(category):
    try:
        new_category = []
        if isinstance(category, list):
            category = " ".join(category)
        for i, pattern in enumerate(jobs_pattern):
            if re.search(pattern, category, re.IGNORECASE):
                new_category.append(jobs_str[i])
        if len(new_category) > 0:
            return new_category
        return ["other"]
    except:
        return ["other"]

for post in posts:
    if 'category' not in post or utils.is_nan(post['category']):
        post['normalized_category'] = get_category_for_nan(post['job'])
    else:
        post['normalized_category'] = get_category_for_normal(post['category'])
utils.write_jsonl("normalized_data/it_jobs.jsonl", posts)
# nan_posts = []
# for post in posts:
#     if 'category' not in post or utils.is_nan(post['category']):
#         nan_posts.append(post)
# posts1 = []
# for post in nan_posts:
#     ok = False
#     for kw in kws:
#         if re.search(kw, post['job'], re.IGNORECASE):
#             ok=True
#             break
#     if not ok:
#         posts1.append(post)
# with open("nan_jobs.txt", 'w') as f:
#     pass
# for post in posts1:
#     with open("nan_jobs.txt", 'a') as f:
#         f.write(post['job'] + "\n")