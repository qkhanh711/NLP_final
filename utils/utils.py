from bs4 import BeautifulSoup as bs
import requests as req
from serpapi import GoogleSearch
from tqdm import tqdm
import os
from dotenv import load_dotenv
load_dotenv()


serpapi_key = os.environ.get('GOOGLE_SEARCH_API_KEY')
openai_key = os.environ.get('OPENAP_KEY')

def get_text(url):
    Web = req.get(url)

    S = bs(Web.text, 'lxml')
    hrefs = S.find_all('article')
    return {"HTML code": S.prettify(),
            "List articles' links": hrefs}

def crawler_Clasification(list_to_crawl, clusID=0):
    for i in range(len(list_to_crawl)):
        url = list_to_crawl[i]
        soup = bs(req.get(url).text, 'lxml')
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
                content += p.text
        tags = soup.find('meta', {'name': 'keywords'})['content']
        summary = soup.find('meta', {'property': 'og:description'})['content']
        if not os.path.exists(f'vnexpress_data_classification/original/Cluster_{clusID+1:03}/original'):
            os.makedirs(f'vnexpress_data_classification/original/Cluster_{clusID+1:03}/original')
        with open(f'vnexpress_data_classification/original/Cluster_{clusID+1:03}/original/{i+1}.txt ', 'w') as f:
            f.write(f"Title: {title}\n")
            f.write(f"Source: {source}\n")
            f.write(f"Link: {url}\n")
            f.write(f"Published Date: {published_date}\n")
            f.write(f"Author: {author}\n")
            f.write(f"Tags: {tags}\n")
            f.write(f"Summary: {summary}\n")
            f.write(f"Content: {content}\n\n")

def crawler_Summary(list_class_to_crawl, clusID =0, save_info = True):
    for i in range(len(list_class_to_crawl)):
        url = list_class_to_crawl[i]
        soup = bs(req.get(url).text, 'lxml')
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
                content += p.text.replace('\n', ' ').strip()
        tags = soup.find('meta', {'name': 'keywords'})['content']
        summary = soup.find('meta', {'property': 'og:description'})['content']
        if not os.path.exists(f'vnexpress_data_summarization/original/Cluster_{clusID+1:03}/original'):
            os.makedirs(f'vnexpress_data_summarization/original/Cluster_{clusID+1:03}/original')
        if save_info:
            with open(f'vnexpress_data_summarization/original/Cluster_{clusID+1:03}/original/1.txt', 'w') as f:
                f.write(f"Title: {title}\n")
                f.write(f"Source: {source}\n")
                f.write(f"Link: {url}\n")
                f.write(f"Published Date: {published_date}\n")
                f.write(f"Author: {author}\n")
                f.write(f"Tags: {tags}\n")
                f.write(f"Summary: {summary}\n")
                f.write(f"Content: {content}\n\n")

def sniper(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        title = lines[0]
        print(title[6:])
        params = {
            "q": f"{title[6:]}",
            "location": "Vietnam",
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "api_key": serpapi_key,
            }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results['organic_results']
    
def saveClusSummary(organic_results, ClusID = 1):
    print("\nCrawling...")
    for i in tqdm(range(len(organic_results))):
        path = f'vnexpress_data_summarization/original/Cluster_{ClusID:03}/original/{i+2}.txt'
        with open(path, 'w') as f:
            f.write(f'Title: {organic_results[i]["title"]}\n')
            f.write(f'Source: {organic_results[i]["source"]}\n')
            f.write(f'Link: {organic_results[i]["link"]}\n')
            try:
                soup = bs(req.get(organic_results[i]["link"]).text, 'lxml')
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
                f.write(f"Published Date: {published_date}\n")
                f.write(f'Author: {author}\n')
                try:
                    tags_string = ', '.join(organic_results[i]["snippet_highlighted_words"])
                except:
                    tags_string = None
                f.write(f'Tags: {tags_string}\n')            
                f.write(f'Summary: {organic_results[i]["snippet"]}\n')
                f.write(f'Content: {content}\n')
            except:
                f.write(f"Published Date: N/A\n")
                f.write(f'Author: N/A\n')
                f.write(f'Tags: N/A\n')            
                f.write(f'Summary: N/A\n')
                f.write(f'Content: N/A\n')
            f.write('\n')
    print("Crawling finished!")

class Labeler():
    def __init__(self, path_origin, path_summary, threshold=20):
        self.path_origin = path_origin
        self.path_summary = path_summary
        self.labels = []
        self.news = []
        self.summary = ""
        self.threshold = threshold
    
    def get_news(self):
        with open(self.path_origin, 'r') as f:
            self.news = f.readlines()
            self.news = self.news[7][9:].split('.')
            self.news = [sentence.lower() for sentence in self.news]
        return self.news
    
    def get_summary(self):
        with open(self.path_summary, 'r') as f:
            self.summary = f.readlines()
        return self.summary[0].lower()
    
    def Labeling(self):
        counter = 0
        for sentence in self.news:
            words = sentence.split(' ')
            for word in words:
                if word in self.summary:
                    counter += 1
            if counter > self.threshold:
                self.labels.append(1)
            else:
                self.labels.append(0)
            counter = 0
        return self.labels
     
    def get_all(self):
        self.news = self.get_news()
        self.summary = self.get_summary()
        self.labels =  self.Labeling()
        return {"news": self.news, "summary": self.summary, "labels": self.labels}
