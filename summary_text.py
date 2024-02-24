from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import os
from tqdm import tqdm

def summarize_text(path , max_lenght=256, models: list = [0,1,2,3]):
    with open(path, 'r', encoding='utf-8') as f:
        src = f.readlines()
        summary = src[6]
        summary = summary[9:]
        src = src[7]
        src = src[9:]
    OUTPUT = []
    if 0 in models:
        ouput0 = summary
        OUTPUT.append(ouput0)
    if 1 in models:
        tokenizer = AutoTokenizer.from_pretrained("minhtoan/t5-small-vietnamese-news")
        model = AutoModelForSeq2SeqLM.from_pretrained("minhtoan/t5-small-vietnamese-news")
        model.cuda()
        tokenized_text = tokenizer.encode(src, return_tensors="pt").cuda()
        model.eval()
        summary_ids = model.generate(tokenized_text, max_length=max_lenght)
        output1 = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        OUTPUT.append(output1)
    if 2 in models:
        if len(src) > 1024:
            src = src[:1024]
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(src, max_length=max_lenght, min_length=30, do_sample=False)
        output2 = summary[0]['summary_text']  
        OUTPUT.append(output2)
    if 3 in models:
        tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base-vietnews-summarization")  
        model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base-vietnews-summarization")
        model.cuda()

        sentence = src + "<s>"
        encoding = tokenizer(sentence, return_tensors="pt")
        input_ids, attention_masks = encoding["input_ids"].to("cuda"), encoding["attention_mask"].to("cuda")
        outputs = model.generate(
            input_ids=input_ids, attention_mask=attention_masks,
            max_length=max_lenght,
            early_stopping=True
        )
        for output in outputs:
            output3 = tokenizer.decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        OUTPUT.append(output3)
    if 4 in models:
        tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-large-vietnews-summarization")  
        model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-large-vietnews-summarization")
        model.cuda()
        sentence = src
        text =  "vietnews: " + sentence + " </s>"
        encoding = tokenizer(text, return_tensors="pt")
        input_ids, attention_masks = encoding["input_ids"].to("cuda"), encoding["attention_mask"].to("cuda")
        outputs = model.generate(
            input_ids=input_ids, attention_mask=attention_masks,
            max_length=256,
            early_stopping=True
        )
        for output in outputs:
            line = tokenizer.decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        OUTPUT.append(line)

    return OUTPUT

num_clasters = os.listdir("vnexpress_data_summarization/original")
print(len(num_clasters)) 

for i in tqdm(range(1, len(num_clasters)+1)):
    path = f"vnexpress_data_summarization/original/Cluster_{i:03}/original/1.txt"
    summaried_texts = summarize_text(path, models=[0,1])
    for j in range(len(summaried_texts)):
        summaried_text = summaried_texts[j]
        if not os.path.exists(f"vnexpress_data_summarization/summary/Cluster_{i:03}"):
            os.makedirs(f"vnexpress_data_summarization/summary/Cluster_{i:03}")
        with open(f"vnexpress_data_summarization/summary/Cluster_{i:03}/{j}.gold.txt", "w", encoding="utf-8") as f:
            f.write(summaried_text)