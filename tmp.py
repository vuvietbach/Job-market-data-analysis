from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("NlpHUST/vi-word-segmentation")
model = AutoModelForTokenClassification.from_pretrained("NlpHUST/vi-word-segmentation")

nlp = pipeline("token-classification", model=model, tokenizer=tokenizer)
example = "Phát biểu tại phiên thảo luận về tình hình kinh tế xã hội của Quốc hội sáng 28/10 , Bộ trưởng Bộ LĐ-TB&XH Đào Ngọc Dung khái quát , tại phiên khai mạc kỳ họp , lãnh đạo chính phủ đã báo cáo , đề cập tương đối rõ ràng về việc thực hiện các chính sách an sinh xã hội"

ner_results = nlp(example)
example_tok = ""
import pdb; pdb.set_trace()
for e in ner_results:
    if "##" in e["word"]:
        example_tok = example_tok + e["word"].replace("##","")
    elif e["entity"] =="I":
        example_tok = example_tok + "_" + e["word"]
    else:
        example_tok = example_tok + " " + e["word"]
print(example_tok)

