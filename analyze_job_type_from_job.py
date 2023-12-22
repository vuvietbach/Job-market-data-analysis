import utils 
import json
import matplotlib.pyplot as plt
import seaborn as sns

kws = []
kws.append(['architect'])
kws.append(['database'])
kws.append(['game', 'unity'])
kws.append(['cloud', 'devops'])
kws.append(['support', 'help', 'service'])
kws.append(['designer', 'thiết kế', 'animator'])
kws.append(['security', 'an ninh', 'bảo mật'])
kws.append(['test', 'quality', 'qa', 'qc', 'kiểm thử'])
kws.append(['embedded', 'phần cứng', 'hardware', 'firmware', 'fpga'])
kws.append(['network', 'system', 'admin', 'mạng', 'linux'])
kws.append(['data', 'business', 'dữ liệu', 'ai', 'computer vision', 'cv', 'phân tích', 'analyst', 'trí tuệ nhân tạo', 'machine learning'])
kws.append(['web', 'back', 'front', 'full', '.net', 'node', 'php', 'react'])
kws.append(['mobile', 'ios', 'android', 'flutter', 'react native'])
kws.append(['dev', 'soft', 'lập trình', 'phần mềm', 'python', 'java', 'c++'])

job_kws = {job[0]:job for job in kws}
with open("job_keywords.json", 'w', encoding='utf-8') as f:
    json.dump(job_kws, f, ensure_ascii=False, indent=4)
job_names = [job[0] for job in kws]
job_count = {name:0 for name in job_names}
def plot_bar(vals, title=None, xlabel=None, ylabel=None, save_path=None):
    plt.figure(figsize=(10, 6))
    x = vals.keys()
    y = vals.values()
    barplot = sns.barplot(x=x, y=y, palette="viridis")
    for idx, value in enumerate(y):
        barplot.text(idx, value + 0.1, str(value), ha='center', va='bottom', fontsize=8)

    plt.title(title, fontweight='bold', color = 'blue')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')

    # legend_labels = sns.color_palette("viridis", len(salary_counts))
    # legend_handles = [plt.Rectangle((0, 0), 1, 1, color=label) for label in legend_labels]
    # plt.legend(legend_handles, salary_counts.index, title="Mức lương")
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    else:
        plt.show()

with open("jobs.json", 'r') as f:
    jobs = json.load(f)

def check_if_contain_kw(text, kws):
    for kw in kws:
        if kw in text:
            return True
    return False
for job in jobs:
    for kw in kws:
        ok = check_if_contain_kw(job, kw)
        if ok:
            job_count[kw[0]] += 1
            break
plot_bar(job_count, 'số lượng công việc theo vị trí', 'vị trí', 'số lượng công việc', 'test.jpg')    