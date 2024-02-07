from bs4 import BeautifulSoup as bs
import requests as req
from serpapi import GoogleSearch
from tqdm import tqdm

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
        import os
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

def crawler_Summary(list_class_to_crawl, clusID =0):
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
        import os
        if not os.path.exists(f'vnexpress_data_summarization/original/Cluster_{clusID+1:03}/original'):
            os.makedirs(f'vnexpress_data_summarization/original/Cluster_{clusID+1:03}/original')
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
            "api_key": "d229d82c7ffb85675c13b46b7e28d5b2707a64a3a374f5a535a2f83d85ac3c58"
            }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results['organic_results']
    
def saveClusSummary(organic_results, ClusID = 1):
    print("\nCrawling...")
    for i in tqdm(range(len(organic_results))):
        path = f'vnexpress_data_summarization/original/Cluster_{ClusID:03}/original/{i+2}.txt'
        # print(path)
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
            