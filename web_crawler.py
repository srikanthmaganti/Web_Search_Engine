import pickle
import requests
import urllib.request
import os
from bs4 import BeautifulSoup
from collections import deque
def web_crawler():
    main_url="https://www.cs.uic.edu/"
    que,list_of_urls,domain,page_num,url_dict,outlinks=deque(),[],'uic.edu',0,{},{}
    que.append(main_url)
    list_of_urls.append(domain)
    exclude_content = ['.avi','.ppt','.gz','.zip','.tar','.tgz','.docx','.ico', '.css', '.js','.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.JPG', '.mp4', '.svg']

    while (len(que)!=0):
        try:
            link=que.popleft()
            req=requests.get(link)
            if (req.status_code==200):
                url_dict[page_num]=link
                file="./Crawled_data/"+str(page_num)
                os.makedirs(os.path.dirname(file), exist_ok=True)
                with open(file,"w",encoding="utf-8") as f:

                    f.write(req.text)
                soup=BeautifulSoup(req.text,'lxml')
                find_tags=soup.find_all('a')
                for tag in find_tags:
                    l=tag.get('href')
                    if l is not None and l.startswith("http") and l not in list_of_urls and domain in l and not any(word in l for word in exclude_content):
                        list_of_urls.append(l)
                        if outlinks.get(page_num):
                        	outlinks[page_num].append(l)
                        else:
                        	outlinks[page_num]=[l]
                        que.append(l)
                	
                if (len(url_dict) > 3000):
                	break
                page_num=page_num+1
        except Exception as e:
        	print(e)
        	print("connection failed",link)
        	continue
    with open('url_dict.pickle','wb') as f:
    	pickle.dump(url_dict,f)
    with open('outlinks.pickle','wb') as f:
    	pickle.dump(outlinks,f)
web_crawler()

