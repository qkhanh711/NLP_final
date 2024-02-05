from bs4 import BeautifulSoup as bs
import requests as req

def get_text(url):
    Web = req.get(url)

    S = bs(Web.text, 'lxml')
    def get_href(S):
        # results = S.find_all('article', {'data-offset': True})
        # if [result.find_all('a')[0].get('href') for result in results] == []:
        results = S.find_all('article')
        # elif [result.find_all('a')[0].get('href') for result in results] == [] and index == 15:
        #     results = S.find_all('article', {'data-publishtime': True})
        # elif [result.find_all('a')[0].get('href') for result in results] == [] and index == 18:
        #     results = S.find_all('article', {'data-campaign': True})
        return results
    hrefs = get_href(S)
    return {"HTML code": S.prettify(),
            "List articles' links": hrefs}

def crawler(list_to_crawl, clusID=0):
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
        with open(f'vnexpress_data_classification/original/Cluster_{clusID+1:03}/original/{i+1}.txt ', 'a') as f:
            f.write(f"Title: {title}\n")
            f.write(f"Source: {source}\n")
            f.write(f"Link: {url}\n")
            f.write(f"Published Date: {published_date}\n")
            f.write(f"Author: {author}\n")
            f.write(f"Tags: {tags}\n")
            f.write(f"Summary: {summary}\n")
            f.write(f"Content: {content}\n\n")