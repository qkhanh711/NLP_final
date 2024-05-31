from bs4 import BeautifulSoup as bs
import requests as req
import sys
sys.path.append('..')
from utils.utils import get_text
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description='Crawl news from VnExpress')
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
print(len(articles))