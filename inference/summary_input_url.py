import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import sys 
sys.path.append('../')
from utils_gpt import get_article_details, save_article_details
from utils_gpt import get_text
import os
from serpapi import GoogleSearch
from rouge_score import rouge_scorer
import torch


# device = "cuda" if torch.cuda.is_available() else "cpu"
# device = "cpu"
# tokenizer = AutoTokenizer.from_pretrained("minhtoan/t5-small-vietnamese-news")
# model = AutoModelForSeq2SeqLM.from_pretrained("minhtoan/t5-small-vietnamese-news")
# model.to(device)

# Cấu hình trang
st.set_page_config(
    page_title="Vietnamese News Summarization",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=":newspaper:",
)

col1, col2 = st.sidebar.columns(2)
url = col2.text_input("URL bài viết")

if url:
    try:

        if not os.path.exists('../vnexpress_data_summarization/inference'):
            os.makedirs('../vnexpress_data_summarization/inference')
        count = len(os.listdir('../vnexpress_data_summarization/inference'))
        soup = get_text(url)['Soup']

        title, source, published_date, author, content, tags, summary = get_article_details(soup)

        with st.container():
            st.title(title)
            st.markdown(f"**Nguồn:** {source}")
            st.markdown(f"**Thẻ tags:** {tags}")
            st.markdown(f"**URL:** {url}")
            st.markdown(f"**Ngày xuất bản:** {published_date}")
            st.markdown(f"**Tác giả:** {author}")

        with st.expander("Liên kết liên quan"):
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

        with st.expander("Nội dung bài viết"):
            st.markdown(content)

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Tóm tắt thủ công")
                st.markdown(summary)
            with col2:
                st.subheader("Tóm tắt tự động")
                src = content
                # tokenized_text = tokenizer.encode(src, return_tensors="pt").to(device)
                # model.eval()
                # summary_ids = model.generate(tokenized_text, max_length=150)
                output = "Tóm tắt tự động"
                # output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                st.markdown(output)

        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL', 'rougeLsum'], use_stemmer=True)
        scores = scorer.score(summary, output)
        with st.expander("Điểm Rouge"):
            st.markdown(f"**Rouge1:** {scores['rouge1'].fmeasure}")
            st.markdown(f"**Rouge2:** {scores['rouge2'].fmeasure}")
            st.markdown(f"**RougeL:** {scores['rougeL'].fmeasure}")

        file_path = f"../vnexpress_data_summarization/inference/Cluster_{(count+1):03}/original/{(count+1):03}.txt"
        if not os.path.exists(f"../vnexpress_data_summarization/inference/Cluster_{(count+1):03}/original"):
            os.makedirs(f"../vnexpress_data_summarization/inference/Cluster_{(count+1):03}/original")
        save_article_details(file_path, title, source, url, published_date, author, tags, summary, content)
        st.success("Lưu trữ thông tin bài viết thành công!")

    except:
        st.error("Lỗi! Vui lòng nhập URL hợp lệ.")


