import json
def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
def read_jsonl(file_path):
    with open(file_path, 'r') as f:
        data = [json.loads(line) for line in f]
    return data
def write_jsonl(file_path, data):
    with open(file_path, 'w', encoding='utf8') as f:
        for line in data:
            json.dump(line, f, ensure_ascii=False)
            f.write('\n')

def normalize_location():
    lines = read_jsonl("data/full.jsonl")
    with open("tinhthanh.txt", 'r') as f:
        locations = f.readlines()
    locations = [l.strip() for l in locations]
    other_name = {"Bà Rịa Vũng Tàu": "Bà Rịa - Vũng Tàu", "TP.HCM": "Hồ Chí Minh"}
    errors = []
    for line in lines:
        location = []
        try:
            for loc in locations:
                if(loc in line['location']):
                    location.append(loc)
            for k, v in other_name.items():
                if(k in line['location']):
                    location.append(v)
            if len(location) == 0:
                errors.append(line['location'])
            else:
                location = list(set(location))
                line['location'] = location
        except:
            errors.append(line['location'])
    write_jsonl("normalized_data/full.jsonl", lines)

def write_list_to_file(file_path, data):
    with open(file_path, 'w', encoding='utf8') as f:
        for line in data:
            f.write(line)
            f.write('\n')

def get_category(categories):
    categories = list(set(categories))

def preprocess(df):
    l = df['requirements'].tolist()
    tmp = []
    for i in l:
        try:
            if isinstance(i, str):
                l1 = i.split('\n')
            else:
                l1 = i
            tmp += l1
        except:
            continue
    docs = tmp
    return docs