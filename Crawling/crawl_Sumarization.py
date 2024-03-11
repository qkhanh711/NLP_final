from bs4 import BeautifulSoup as bs
import requests as req
from utils.utils import *
from tqdm import tqdm
import argparse


parser = argparse.ArgumentParser(description='Crawl and Summarize news from VnExpress')
parser.add_argument('--num_clusters', type=int, default=10, help='Number of clusters to crawl')
args = parser.parse_args()

num_clusters = args.num_clusters


Web = req.get('https://vnexpress.net')
S = bs(Web.text, 'lxml')
navigator = S.find_all(class_='main-nav')
li_elements = navigator[0].find_all('li') 
classes = [li.get('class')[0] for li in li_elements][1:-1]
paths = [li.find_all('a')[0].get('href') for li in li_elements][1:-1]
classes.remove('video')
paths.remove('https://video.vnexpress.net')
urls = ['https://vnexpress.net' + content for content in paths]

print(urls)

articles = get_text(urls[18])["List articles' links"]
# print(len(articles))
articles[10].find_all('a')
list_to_crawl = [article.find_all('a')[0].get('href')  for article in articles if article.find_all('a') != []]
print()

pages = [get_text(url) for url in urls]

list_class_to_crawl = []
for i in range(len(pages)):
    articles = pages[i]["List articles' links"]
    list_to_crawl = [article.find('a')['href'] for article in articles if article.find_all('a') != []]
    list_class_to_crawl.extend(list_to_crawl)

for clusID in tqdm(range(len(list_class_to_crawl[:num_clusters]))):
    crawler_Summary([list_class_to_crawl[clusID]], clusID=clusID)
    organic_results  = sniper(f'vnexpress_data_summarization/original/Cluster_{clusID+1:03}/original/1.txt')
    saveClusSummary(organic_results, ClusID = clusID+1)
