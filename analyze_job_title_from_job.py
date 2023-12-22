import utils 
import json
# stage 1
posts = utils.read_jsonl("normalized_data/it_jobs.jsonl")
jobs = [i['job'].lower().strip() for i in posts]
jobs = [i for i in jobs if i != ""]
jobs = list(set(jobs))
with open("jobs.json", "w", encoding='utf-8') as f:
    json.dump(jobs, f, ensure_ascii=False, indent=4)
# stage 2
kws = [
    ["giám đốc", "director", "executive"],
    [
        "quản lý",
        "quản trị",
        "phó",
        "trưởng",
        "lead",
        "head",
        "manager",
        "supervisor",
        "owner",
        "product owner",
        "master",
        "scrum master",
    ],
    ["consultant", "tư vấn"],
    ["chuyên gia", "specialist", "expert"],
    ["giáo viên", "giảng viên", "teacher", "lecturer"],
    ["thực tập", "intern", "sinh viên"],
    [
        "nhân viên",
        "chuyên viên",
        "kỹ thuật",
        "analyst",
        "admin",
        "engineer",
        "kỹ sư",
        "kĩ sư",
        "lập trình",
        "dev",
        "tester",
        "test",
        "it",
        "designer",
        "support",
    ],
]
with open("jobs.json", 'r') as f:
    jobs = json.load(f)
num_jobs = {i:0 for i in range(8)}
for job in jobs:
    ok1 = False
    for i in range(7):
        ok = False
        for job_pos in kws[i]:
            if(job_pos in job):
                ok = True
                break
        if ok:
            ok1 = True
            num_jobs[i] += 1
            break
    if not ok1:
        num_jobs[7] += 1 
    
job_pos_name = ['lãnh đạo', 'quản lý', 'tư vấn', 'chuyên gia', 'giáo viên', 'thực tập sinh', 'nhân viên', 'khác']
utils.plot_bar(job_pos_name, num_jobs.values(), 'số lượng công việc trên vị trí', 'vị trí', 'số lượng công việc', save_file='job_position.png')
