from bs4 import BeautifulSoup as bs
import requests as req
from serpapi import GoogleSearch
from tqdm import tqdm
import os

def get_text(url):
    response = req.get(url)
    soup = bs(response.text, 'lxml')
    articles = soup.find_all('article')
    return {"Soup": soup, "HTML code": soup.prettify(), "List articles' links": articles}

def get_article_details(soup):
    title = soup.find('title').text
    source = soup.find('meta', {'name': 'author'})['content']
    try:
        published_date = soup.find('span', class_='date').text
    except:
        published_date = "N/A"    
    author = ''
    content = ''
    for p in soup.find_all('p'):
        if p.get('style') == 'text-align:right;':
            author = p.text
        else:
            content += p.text.replace('\n', ' ').strip() + ' '
    tags = soup.find('meta', {'name': 'keywords'})['content']
    summary = soup.find('meta', {'property': 'og:description'})['content']
    return title, source, published_date, author, content, tags, summary

def save_article_details(file_path, title, source, url, published_date, author, tags, summary, content):
    with open(file_path, 'w') as f:
        f.write(f"Title: {title}\n")
        f.write(f"Source: {source}\n")
        f.write(f"Link: {url}\n")
        f.write(f"Published Date: {published_date}\n")
        f.write(f"Author: {author}\n")
        f.write(f"Tags: {tags}\n")
        f.write(f"Summary: {summary}\n")
        f.write(f"Content: {content}\n\n")

def crawler_Classification(list_to_crawl, clusID=0):
    for i, url in enumerate(tqdm(list_to_crawl)):
        response = req.get(url)
        soup = bs(response.text, 'lxml')
        title, source, published_date, author, content, tags, summary = get_article_details(soup)
        folder_path = f'vnexpress_data_classification/original/Cluster_{clusID+1:03}/original'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = f'{folder_path}/{i+1}.txt'
        save_article_details(file_path, title, source, url, published_date, author, tags, summary, content)

def crawler_Summary(list_class_to_crawl, clusID=0):
    for i, url in enumerate(tqdm(list_class_to_crawl)):
        response = req.get(url)
        soup = bs(response.text, 'lxml')
        title, source, published_date, author, content, tags, summary = get_article_details(soup)
        folder_path = f'vnexpress_data_summarization/original/Cluster_{clusID+1:03}/original'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = f'{folder_path}/{i+1}.txt'
        save_article_details(file_path, title, source, url, published_date, author, tags, summary, content)

def sniper(path):
    with open(path, 'r') as f:
        title = f.readline().strip()
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
        return results['organic_results']
    
def saveClusSummary(organic_results, ClusID=1):
    print("\nCrawling...")
    for i, result in enumerate(tqdm(organic_results)):
        file_path = f'vnexpress_data_summarization/original/Cluster_{ClusID:03}/original/{i+2}.txt'
        try:
            response = req.get(result["link"])
            soup = bs(response.text, 'lxml')
            title, source, published_date, author, content, tags, summary = get_article_details(soup)
            save_article_details(file_path, title, source, result["link"], published_date, author, tags, result["snippet"], content)
        except Exception as e:
            print(f"Error occurred while processing {result['link']}: {e}")
    print("Crawling finished!")
