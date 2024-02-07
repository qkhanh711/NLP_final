from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import os
from tqdm import tqdm

def summarize_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        src = f.readlines()
        src = src[7]
        src = src[9:]

    tokenizer = AutoTokenizer.from_pretrained("minhtoan/t5-small-vietnamese-news")
    model = AutoModelForSeq2SeqLM.from_pretrained("minhtoan/t5-small-vietnamese-news")
    model.cuda()
    tokenized_text = tokenizer.encode(src, return_tensors="pt").cuda()
    model.eval()
    summary_ids = model.generate(tokenized_text, max_length=150)
    output1 = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    if len(src) > 1024:
        src = src[:1024]
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(src, max_length=150, min_length=30, do_sample=False)
    output2 = summary[0]['summary_text']    
    return [output1, output2]

num_clasters = os.listdir("vnexpress_data_summarization/original")
print(len(num_clasters)) 

for i in tqdm(range(1, len(num_clasters)+1)):
    path = f"vnexpress_data_summarization/original/Cluster_{i:03}/original/1.txt"
    summaried_texts = summarize_text(path)
    for j in range(len(summaried_texts)):
        summaried_text = summaried_texts[j]
        if not os.path.exists(f"vnexpress_data_summarization/summary/Cluster_{i:03}/summary"):
            os.makedirs(f"vnexpress_data_summarization/summary/Cluster_{i:03}/summary")
        with open(f"vnexpress_data_summarization/summary/Cluster_{i:03}/summary/{j}.gold.txt", "w", encoding="utf-8") as f:
            f.write(summaried_text)