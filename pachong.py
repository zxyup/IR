from bs4 import BeautifulSoup
import os,sys
import re,requests
from fake_useragent import UserAgent
from urllib.parse import urlparse, urljoin, quote,unquote
from collections import deque
import certifi
os.chdir(sys.path[0])

visited_urls = set()
link_counter = 0
def normalize_url(url):
    # 将URL的协议标准化为HTTPS
    parsed_url = urlparse(url)
    if parsed_url.scheme == 'http':
        url = url.replace('http://', 'https://', 1)
    return url

def save_content(content,url):
    global link_counter
    link_counter+=1
    encoded_link = str(link_counter) + '_'+ quote(url)
    encoded_link = encoded_link.replace('/', '_')
    path = os.path.join('web_doc',encoded_link)
    with open(f"{path}.txt",'w',encoding='utf-8-sig') as f:
        f.write(str(content))
    print(link_counter,end='\t')

def spider(url):
    queue = deque([url])
    
    while queue:
        current_url = queue.popleft()
        if 'lecture.xmu.edu.cn/system/files/ppts/' in current_url:
            continue
        if '_upload/article/files/' in current_url:
            continue
        if 'system/_content/download.jsp?urltype=news.DownloadAttachUrl' in current_url:
            continue
        if 'page.jsp?urltype=tree.TreeTempUrl' in current_url:
            continue
        if current_url.endswith('null'):
            continue
        try:
            headers = {'User-Agent': UserAgent().random} 
            response = requests.get(current_url,verify=certifi.where(),headers=headers)
        except Exception as e:
            print(f'\n{e}')
            print(current_url)
            continue
        if response.status_code == 200:
            # content = response.content
            response.encoding = response.apparent_encoding
            save_content(response.text,current_url)
            if current_url == 'https://hr.xmu.edu.cn/':
                soup = BeautifulSoup(response.content,'xml')
            else:
                soup = BeautifulSoup(response.content,'html.parser')
            
            links = soup.find_all('a',href=True)
            for link in links:
                href = link['href']
                if href != '#' and not href.startswith('javascript:') and not href.endswith('pdf') and not href.endswith('jpg') and not href.endswith('doc') and not href.endswith('xls') and not href.endswith('xlsx') and not href.endswith('jpg'):
                    if len(href)>100:
                        continue
                    next_url = urljoin(current_url,href)
                    next_url = normalize_url(next_url)  # 标准化URL
                    if 'xmu.edu.cn' in next_url and next_url not in visited_urls:
                        visited_urls.add(next_url)
                        queue.append(next_url)
                            
                        
def main():
    start_url = "http://www.xmu.edu.cn"
    visited_urls.add(start_url)
    spider(start_url)

if __name__ == "__main__":
    main()