import requests
import os.path
from bs4 import BeautifulSoup
import time

host_url='https://tmi.yokogawa.com/cn/library/search/#/t=5'
save_folder = 'E:\\py_downloads\\'
keywords = '.pdf'
exclude_web = set()

f = open(save_folder + "finish_url",'r')
finish_url = f.readlines()
f.close()
def real_time_update_finish_url(want_url):
    exclude_web.add(want_url)
    #做完的網頁加入已完成url 並且存檔
    # 網頁完成的條件為 1.回應為200 或是 2.無效url 或是 3.原本就排除的網頁finish_url
    with open(save_folder + "finish_url", 'w') as f:
        for item in exclude_web:
            f.write("%s\n" % item)

def try_web_connect (url ) :
    tries = 5
    while (tries):
        try:
            page = requests.get(url,headers={'Connection':'close'})
            if(page.status_code == 200):
                return page
            else :
                raise 'error'
        except:
            print("Connection refused by the server..,sleep for 5 seconds")
            time.sleep(3)
            tries -=1
            continue
    return None

def download(url):
    filename = url[url.rfind("/")+1:]
    full_path = save_folder + filename
    if os.path.isfile(full_path):
        print ("File exist :" + full_path )
        return

    r = try_web_connect(url)
    if r is None :
        return
    if(r.status_code == 200):
        print(full_path)
        return open(full_path, 'wb').write(r.content)
    else:
        return -1

def enter_download_page(url):
    r = try_web_connect(url)  # https://tmi.yokogawa.com/industries/motors-drives/
    if r is None :
        return

    print(r.status_code)
    # print(type(r))
    # print(type(html_str))
    s = set()
    if(r.status_code == 200):
        html_str = r.text
        soup = BeautifulSoup(html_str, 'html.parser')
        a_tags = soup.find_all('a')
        for tag in a_tags:
            url = str(tag.get('href'))
            if url.find(keywords) != -1:
                s.add(url)
        real_time_update_finish_url(want_url)
    else:
        print('enter_download_page http request error!')

    for ss in s:
        print('downloading:' + ss)
        if ss.find('http') == 0:
            print('invalid address!')
            return
        else :
            download('https:' + ss)

# https://tmi.yokogawa.com/industries/motors-drives/
r = try_web_connect(host_url)
if(r.status_code == 200):
    url_sets = set()
    html_str = r.text
    print(r.status_code)
    soup = BeautifulSoup(html_str, 'html.parser')
    a_tags = soup.find_all('a')

    # 加入網頁中所有超連結元素到 url_sets
    for tag in a_tags:
        url = str(tag.get('href'))
        # 原本想過濾超連結
        #if url.find('industries') != -1:
        url_sets.add(url)

    for item in url_sets:
        want_url = 'https://tmi.yokogawa.com' + item
        print(want_url)
        if any(want_url in y for y in finish_url):
            print('had finished download!')
            real_time_update_finish_url(want_url)
        else :
            if item.find('http') != -1:
                print('invalid address!')
                real_time_update_finish_url(want_url)
            else :
                enter_download_page(want_url)
else:
    print('http request error!')
