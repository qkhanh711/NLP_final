import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import sys 
sys.path.append('../')
from utils_gpt import get_article_details, save_article_details
from utils_gpt import get_text
import os
from serpapi import GoogleSearch
from rouge_score import rouge_scorer

tokenizer = AutoTokenizer.from_pretrained("minhtoan/t5-small-vietnamese-news")  
model = AutoModelForSeq2SeqLM.from_pretrained("minhtoan/t5-small-vietnamese-news")
model.cuda()


st.title('Vietnamese News Summarization')

st.write("Please input your link to get the summary")
url = st.text_input("URL Link: ")
if st.button('Submit'):
    try:
        if not os.path.exists('../vnexpress_data_summarization/inference'):
            os.makedirs('../vnexpress_data_summarization/inference')
        count = len(os.listdir('../vnexpress_data_summarization/inference'))
        soup = get_text(url)['Soup']
        title, source, published_date, author, content, tags, summary = get_article_details(soup)
        st.write("List of information: ")
        st.write(f"Title: {title}")
        with st.expander("Show the related url"):
            params = {
                "q": title,
                "location": "Vietnam",
                "hl": "en",
                "gl": "us",
                "google_domain": "google.com",
                "api_key": "d229d82c7ffb85675c13b46b7e28d5b2707a64a3a374f5a535a2f83d85ac3c58"
                }
            search = GoogleSearch(params)
            results = search.get_dict()
            st.write([result['link'] for result in results['organic_results']])


        with st.expander("Show more details"):
            st.write(f"Source: {source}")
            st.write(f"Published Date: {published_date}")
            st.write(f"Author: {author}")
            st.write(f"Tags: {tags}")
            st.write(f"Content: {content}")

        with st.expander("Human summarize"):
            st.write(f"Summary: {summary}")

        with st.expander("Machine summarize"):
            src = content
            tokenized_text = tokenizer.encode(src, return_tensors="pt").cuda()
            model.eval()
            summary_ids = model.generate(tokenized_text, max_length=150)
            output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            st.write(f"Summary: {output}")

        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL', 'rougeLsum'], use_stemmer=True)
        scores = scorer.score(summary, output)
        st.write(f"""Calculating the Rouge score...""")
        with st.expander("Show the Rouge score"):
            st.write(f"Rouge1: {scores['rouge1'].fmeasure}")
            st.write(f"Rouge2: {scores['rouge2'].fmeasure}")
            st.write(f"RougeL: {scores['rougeL'].fmeasure}")

        file_path = f"../vnexpress_data_summarization/inference/Cluster_{(count+1):03}/original/{(count+1):03}.txt"
        if not os.path.exists(f"../vnexpress_data_summarization/inference/Cluster_{(count+1):03}/original"):
            os.makedirs(f"../vnexpress_data_summarization/inference/Cluster_{(count+1):03}/original")
        save_article_details(file_path, title, source, url, published_date, author, tags, summary, content)
        st.write("Susscessfully saved the article details to the database")
    except:
        st.write("Please input a valid link!!")

