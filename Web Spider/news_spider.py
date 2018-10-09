import re
import requests
from bs4 import BeautifulSoup
import translater.youdao as Youdao
import print_time.click_time as click
import urllib3
import ssl
from lxml import etree

def spider(n_url,n_header=0):
    if(n_header==0):
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)'
        }
    else:
        if(n_header==1):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }
        else:
            if(n_header==2):
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                    'Cookie': '__jsluid=7b7a496218ccf130103334d424693762; csrftoken=qq1qva6gB6teYCbVR98w9KYuznqHqTE9; Hm_lvt_6b15558d6e6f640af728f65c4a5bf687=1538237060,1538308814,1538656061,1538843155; Hm_lpvt_6b15558d6e6f640af728f65c4a5bf687=1538844173; __jsl_clearance=1538861279.44|0|eLjw89YCtKe2D9xL578po3ymXgY%3D'
                }
            else:
                if(n_header==3):
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                        'Cookie': 'acw_tc=65c86a0d15388642732773900e610ba37f5f4f22ae046d41404c2e97d444cf; acw_sc__v2=NWJiOTM0YjdiZjg2MjBjODMwNzdiYjJhOTVjYmJhNDUxNGE4OGJkYg==; acw_sc__v3=5bb934ba58914a637b2737590a1a91b7840d0445; Hm_lvt_cc53db168808048541c6735ce30421f5=1538864318; Hm_lpvt_cc53db168808048541c6735ce30421f5=1538864318; 3cb185a485c81b23211eb80b75a406fd=1538864318; PHPSESSID=pbogl3c78up26cfjd93fc97gd1'
                    }
    flag1 = 0
    flag2 = 0
    while ((flag1!=1)&(flag2!=3)):
        try:
            request = requests.get(n_url, headers=headers)
            flag1 = 1
        except (requests.exceptions.ConnectionError, requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
            flag2 = flag2 + 1
            print(n_url+"connect failed!")
            if(flag2==3):
                return None,flag2
    # request = requests.get(n_url, headers=headers)
    return request.text,flag2

def one(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://blogs.msdn.microsoft.com/"
    # st = str(tmp_x)
    # a = open(r'.\tmp'+st+'.html', str(how_write), encoding='utf-8')
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()

    # flag2 = 0
    html_text,flag2 = spider(n_url)
    # html_text = spider("https://blogs.msdn.microsoft.com/")
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    # a.write(html_text)
    # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    # n=0
    # soup = BeautifulSoup(html_text, 'html.parser')
    # get_news = soup.find_all('article')  #找有某属性的标签
    # print(get_news)
    ###############新闻信息分类
    #####时间
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    # ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # ####
    # print(n_time1[0])
    #####标题
    # n_title = get_news[0].img.attrs['alt']
    # print(n_title)
    #####内容
    # n_detail = get_news[0].find('div',{'class':'home-desc'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[0].a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    if(flag2 != 3):
        soup = BeautifulSoup(html_text, 'html.parser')
        get_news = soup.find_all('article')
        n=0

        while(n<9):
            n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
            ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            print('span:',span_time)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
            ########只显示how_day内的新闻
            # re.findall('(.*?)T', (get_news[n].time.attrs['datetime']))
            n_title = get_news[n].find('header').text
            n_detail = get_news[n].div.p.text
            n_url = get_news[n].header.h2.a.attrs['href']

            a.write(str(n_time).strip()+'\n')

            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')

            # a.write(str(n_detail).strip()+'\n')
            a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def two(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://thehackernews.com/?m=1"
    # st = str(tmp_x)
    # a = open(r'.\tmp'+st+'.html', str(how_write), encoding='utf-8')
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    # flag1 = 0
    # flag2 = 0
    # while ((flag1!=1)&(flag2!=3)):
    #     try:
    #         html_text = spider(n_url)
    #         flag1 = 1
    #     except (requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
    #         flag2 = flag2 + 1
    #         print(n_url+"connect failed!")
    # html_text = spider(n_url)
    # flag2 = 0
    (html_text,flag2) = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    # a.write(html_text)
    # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    # soup = BeautifulSoup(html_text, 'html.parser')
    # get_news = soup.find_all('div',{'class':'body-post clear'})  #找有某属性的标签
    # print(get_news[0])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[0].find('div',{'class':'item-label'})
    # print(n_time)
    # ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # ####
    # print(n_time1[0])
    #####标题
    # n_title = get_news[0].img.attrs['alt']
    # print(n_title)
    #####内容
    # n_detail = get_news[0].find('div',{'class':'home-desc'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[0].a.attrs['href']
    # print(n_url)
#############################################################
    # a = open(r'.\tmp'+st+'.txt', 'a',encoding='utf-8')
    a = open(way, 'a', encoding='utf-8')
    if(flag2 != 3):
        soup = BeautifulSoup(html_text, 'html.parser')
        get_news = soup.find_all('div', {'class': 'body-post clear'})
        n=0

        while(n<7):

            n_time = str(etree.HTML(str(get_news[n].find('div',{'class':'item-label'}))).xpath('//div[@class="item-label"]/text()')[0]).strip()
            ########只显示how_day内的新闻
            span_time = click.day_span(n_time,0,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
            ########只显示how_day内的新闻
            n_title = get_news[n].img.attrs['alt']
            n_detail = get_news[n].find('div',{'class':'home-desc'}).text
            n_url = get_news[n].a.attrs['href']

            a.write(n_time+'\n')

            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')

            # a.write(str(n_detail).strip()+'\n')
            a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def three(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://researchcenter.paloaltonetworks.com/"
    # st = str(tmp_x)
    # a = open(r'.\tmp'+st+'.txt', str(how_write),encoding='utf-8')
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()

    # flag1 = 0
    # flag2 = 0
    # while ((flag1!=1)&(flag2!=3)):
    #     try:
    #         html_text = spider(n_url)
    #         flag1 = 1
    #     except (requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
    #         flag2 = flag2 + 1
    #         print(n_url+"connect failed!")
    html_text,flag2 = spider(n_url)
    # html_text = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    # soup = BeautifulSoup(html_text, 'html.parser')
    # get_news = soup.find_all('article')  #找有某属性的标签
    # print(get_news[0])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].time.attrs['datetime']
    # print(n_time)
    # ##用模块re提取标准时间
    # n_time1 = re.findall('(.*?)T',get_news[n].time.attrs['datetime'])[0]
    # print(n_time1)
    # ##用模块xpath提取出不在某个具体标签中的元素
    # n_time2 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # ####
    # print(n_time1[0])
    #####标题
    # n_title = get_news[0].div.header.h2.a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[0].find('div',{'class':'entry-summary clearfix'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[0].div.header.h2.a.attrs['href']
    # print(n_url)
#############################################################
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    a = open(way, 'a', encoding='utf-8')
    if(flag2 != 3):
        soup = BeautifulSoup(html_text, 'html.parser')
        get_news = soup.find_all('article')
        n=0

        while(n<3):

            n_time = re.findall('(.*?)T',get_news[n].time.attrs['datetime'])[0]
            ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            print(span_time)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
            ########只显示how_day内的新闻
            n_title = get_news[n].div.header.h2.a.text
            n_detail = get_news[n].find('div',{'class':'entry-summary clearfix'}).text
            n_url = get_news[n].div.header.h2.a.attrs['href']

            a.write(str(n_time).strip()+'\n')

            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')

            # a.write(str(n_detail).strip()+'\n')
            a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def four(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "http://hackernews.cc/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    flag1 = 0
    flag2 = 0
    # while ((flag1!=1)&(flag2!=3)):
    #     try:
    #         html_text = spider(n_url)
    #         flag1 = 1
    #     except (requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
    #         flag2 = flag2 + 1
    #         print(n_url+"connect failed!")
    html_text,flag2 = spider(n_url)
    # html_text = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    # soup = BeautifulSoup(html_text, 'html.parser')
    # get_news = soup.find_all('article', {'id':'article'})  #找有某属性的标签
    # print(get_news[0])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[0].find('div',{'class':'light-post-meta'}).find_all('span')[1].a.text
    # print(n_time)
    # ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # ####
    # print(n_time1[0])
    #####标题
    # n_title = get_news[0].find('div',{'class':'classic-list-left'}).a.attrs["title"]
    # print(n_title)
    #####内容
    # n_detail = get_news[0].find('div',{'class':'m-post-excepert'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[0].find('div',{'class':'classic-list-left'}).a.attrs["href"]
    # print(n_url)
#############################################################
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    a = open(way, 'a', encoding='utf-8')
    if(flag2 != 3):
        soup = BeautifulSoup(html_text, 'html.parser')
        get_news = soup.find_all('article', {'id':'article'})
        n=0

        while(n<10):

            n_time = get_news[n].find('div',{'class':'light-post-meta'}).find_all('span')[1].a.text
            ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
            ########只显示how_day内的新闻
            n_title = get_news[n].find('div',{'class':'classic-list-left'}).a.attrs["title"]
            n_detail = get_news[n].find('div',{'class':'m-post-excepert'}).text
            n_url = get_news[n].find('div',{'class':'classic-list-left'}).a.attrs["href"]


            a.write(str(n_time).strip()+'\n')
################不用翻译组
            a.write(n_title.strip()+'\n')
            a.write(str(n_detail).strip()+'\n')
################翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(Youdao.go(n_title.strip())+'\n')
            #
            # a.write(str(n_detail).strip()+'\n')
            # a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def five(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://posts.specterops.io/"
    a = open(way, str(how_write), encoding='utf-8')
    # st = str(tmp_x)
    # a = open(r'.\tmp'+st+'.html', str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    flag1 = 0
    flag2 = 0
    # while ((flag1!=1)&(flag2!=3)):
    #     try:
    #         html_text = spider(n_url)
    #         flag1 = 1
    #     except (requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
    #         flag2 = flag2 + 1
    #         print(n_url+"connect failed!")
    html_text,flag2 = spider(n_url)
    # html_text = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    # n=0
    # soup = BeautifulSoup(html_text, 'html.parser')
    # get_news = soup.find_all('div', {'class':'postArticle postArticle--short is-withAccentColors'})  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = re.findall('(.*?)T',(get_news[n].time.attrs['datetime']))
    # print(n_time)
    # ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].h3.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].p.text
    # print(n_detail)
    #####链接
    # n_url = get_news[2].find_all('a')[3].attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        soup = BeautifulSoup(html_text, 'html.parser')
        get_news = soup.find_all('div', {'class':'postArticle postArticle--short is-withAccentColors'})
        n=0

        while(n<2):

            n_time = re.findall('(.*?)T',(get_news[n].time.attrs['datetime']))[0]
            ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
            ########只显示how_day内的新闻
            n_title = get_news[n].h3.text
            try:
                n_detail = get_news[n].p.text
            except(AttributeError):
                n_detail = "None detail.Maybe,it is a imag!"
            n_url = get_news[2].find_all('a')[3].attrs['href']


            a.write(str(n_time).strip()+'\n')
################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')

            # a.write(str(n_detail).strip()+'\n')
            a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def six(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://cofense.com/"
    a = open(way, str(how_write), encoding='utf-8')
    # st = str(tmp_x)
    # a = open(r'.\tmp'+st+'.html', str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    flag1 = 0
    flag2 = 0
    # while ((flag1!=1)&(flag2!=3)):
    #     try:
    #         html_text = spider(n_url)
    #         flag1 = 1
    #     except (requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
    #         flag2 = flag2 + 1
    #         print(n_url+"connect failed!")
    html_text,flag2 = spider(n_url)
    # html_text = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    # n=0
    # soup = BeautifulSoup(html_text, 'html.parser')
    # get_news = soup.find_all('div', {'class':'col-md-4'})  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].time.attrs['datetime']
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].h3.a.attrs['title']
    # print(n_title)
    #####内容
    # n_detail = get_news[n].p.text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].h3.a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        soup = BeautifulSoup(html_text, 'html.parser')
        get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<3):

            n_time = get_news[n].time.attrs['datetime']
            ########只显示how_day内的新闻
            span_time = click.day_span(n_time,0,0)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
            ########只显示how_day内的新闻
            n_title = get_news[n].h3.a.attrs['title']
            n_detail = get_news[n].p.text
            n_url = get_news[n].h3.a.attrs['href']


            a.write(str(n_time).strip()+'\n')
################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')

            # a.write(str(n_detail).strip()+'\n')
            a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def eight(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://www.hackread.com/hacking-news/"
    a = open(way, str(how_write), encoding='utf-8')
    # st = str(tmp_x)
    # a = open(r'.\tmp'+st+'.html', str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    flag1 = 0
    flag2 = 0
    # while ((flag1!=1)&(flag2!=3)):
    #     try:
    #         html_text = spider(n_url)
    #         flag1 = 1
    #     except (requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
    #         flag2 = flag2 + 1
    #         print(n_url+"connect failed!")
    html_text,flag2 = spider(n_url)
    # html_text = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('article')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].time.attrs['datetime']
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].h3.a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].h3.a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<6):
            n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
            ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
            ########只显示how_day内的新闻
            n_title = get_news[n].h3.a.text
            n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
            n_url = get_news[n].h3.a.attrs['href']


            a.write(str(n_time).strip()+'\n')
################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')

            # a.write(str(n_detail).strip()+'\n')
            a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def nine(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://motherboard.vice.com/en_us/topic/hacking"
    a = open(way, str(how_write), encoding='utf-8')
    # st = str(tmp_x)
    # a = open(r'.\tmp'+st+'.html', str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    flag1 = 0
    flag2 = 0
    # while ((flag1!=1)&(flag2!=3)):
    #     try:
    #         html_text = spider(n_url)
    #         flag1 = 1
    #     except (requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
    #         flag2 = flag2 + 1
    #         print(n_url+"connect failed!")
    html_text,flag2 = spider(n_url)
    # html_text = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=1
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('a',{'class':'grid__wrapper__card grd-col col-12-xs col-6-m col-3-hd dsp-block-xs p-t-3-xs col-4-xl'})  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].find('div',{'class':'dsp-inline-xs hed-xxs canonical__date hed-xxs'}).text
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('h2',{'class':'grid__wrapper__card__text__title hed-m m-b-2-xs'}).text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'grid__wrapper__card__text__summary bod-s m-b-2-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = 'https://motherboard.vice.com'+get_news[n].attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<1):
            n_time = get_news[n].find('div',{'class':'dsp-inline-xs hed-xxs canonical__date hed-xxs'}).text
            ########只显示how_day内的新闻
            # span_time = click.day_span(n_time)
            # if((n!=0)&(span_time>how_day)):
            #     break
            # if(span_time==-1):
            #     print(n_url+"时间格式有问题")
            #     break
            ########只显示how_day内的新闻
            n_title = get_news[n].find('h2',{'class':'grid__wrapper__card__text__title hed-m m-b-2-xs'}).text
            n_detail = get_news[n].find('div',{'class':'grid__wrapper__card__text__summary bod-s m-b-2-xs'}).text
            n_url = 'https://motherboard.vice.com'+get_news[n].attrs['href']


            a.write(str(n_time).strip()+'\n')
################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')

            # a.write(str(n_detail).strip()+'\n')
            a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def ten(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://www.cnbeta.com/topics/157.htm"
    a = open(way, str(how_write), encoding='utf-8')
    # st = str(tmp_x)
    # a = open(r'.\tmp'+st+'.html', str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    flag1 = 0
    flag2 = 0
    # while ((flag1!=1)&(flag2!=3)):
    #     try:
    #         html_text = spider(n_url)
    #         flag1 = 1
    #     except (requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
    #         flag2 = flag2 + 1
    #         print(n_url+"connect failed!")
    html_text,flag2 = spider(n_url)
    # html_text = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=3
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('div',{'class','item'})  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].find('ul').find('li').text
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('20(.*?) ', (get_news[n].find('ul').find('li').text))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('a',{'target':'_blank'}).text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('dd').text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].find('a',{'target':'_blank'}).attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<9):
            n_time = '20'+ (re.findall('20(.*?) ', (get_news[n].find('ul').find('li').text))[0])
            ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
            ########只显示how_day内的新闻
            n_title = get_news[n].find('a',{'target':'_blank'}).text
            n_detail = get_news[n].find('dd').text
            n_url = get_news[n].find('a',{'target':'_blank'}).attrs['href']


            a.write(str(n_time).strip()+'\n')
################不用翻译组
            a.write(n_title.strip()+'\n')
            a.write(str(n_detail).strip()+'\n')
################翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(Youdao.go(n_title.strip())+'\n')
            #
            # a.write(str(n_detail).strip()+'\n')
            # a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def ten_1(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://www.zdnet.com/topic/security/"
    a = open(way, str(how_write), encoding='utf-8')
    # st = str(tmp_x)
    # a = open(r'.\tmp'+st+'.html', str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    flag1 = 0
    flag2 = 0
    # while ((flag1!=1)&(flag2!=3)):
    #     try:
    #         html_text = spider(n_url)
    #         flag1 = 1
    #     except (requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
    #         flag2 = flag2 + 1
    #         print(n_url+"connect failed!")
    html_text,flag2 = spider(n_url)
    # html_text = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('div',{'class':'content'})  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].find('span').attrs['data-date']
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?) ', get_news[n].find('span').attrs['data-date'])[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('a').text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('p').text
    # print(n_detail)
    #####链接
    # n_url = 'https://www.zdnet.com'+get_news[n].a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<6):
            n_time = re.findall('(.*?) ', get_news[n].find('span').attrs['data-date'])[0]
            ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
            ########只显示how_day内的新闻
            n_title = get_news[n].find('a').text
            n_detail = get_news[n].find('p').text
            n_url = 'https://www.zdnet.com'+get_news[n].a.attrs['href']


            a.write(str(n_time).strip()+'\n')
################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')

            # a.write(str(n_detail).strip()+'\n')
            a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def ten_2(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "http://www.4hou.com/"
    a = open(way, str(how_write), encoding='utf-8')
    # st = str(tmp_x)
    # a = open(r'.\tmp'+st+'.html', str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    flag1 = 0
    flag2 = 0
    # while ((flag1!=1)&(flag2!=3)):
    #     try:
    #         html_text = spider(n_url)
    #         flag1 = 1
    #     except (requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
    #         flag2 = flag2 + 1
    #         print(n_url+"connect failed!")
    html_text,flag2 = spider(n_url)
    # html_text = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=1
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('div',{'class':'main-box'})  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].find('span',{'class':'stime'}).text
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('div',{'class':'new_con'}).a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'new_con'}).p.text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].find('div',{'class':'new_con'}).a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<3):
            n_time = get_news[n].find('span',{'class':'stime'}).text
            ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if((n!=0)&(span_time==-1)):
                print(n_url+"时间格式有问题")
                break
            ########只显示how_day内的新闻
            n_title = get_news[n].find('div',{'class':'new_con'}).a.text
            n_detail = get_news[n].find('div',{'class':'new_con'}).p.text
            n_url = get_news[n].find('div',{'class':'new_con'}).a.attrs['href']

            a.write(str(n_time).strip()+'\n')
################不用翻译组
            a.write(n_title.strip()+'\n')
            a.write(str(n_detail).strip()+'\n')
################翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(Youdao.go(n_title.strip())+'\n')
            #
            # a.write(str(n_detail).strip()+'\n')
            # a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def ten_3(how_write,how_day,way='.\tmp.txt'):
    n_url = "https://packetstormsecurity.com/"
    a = open(way, 'a', encoding='utf-8')
    # st = str(tmp_x)
    # a = open(r'.\tmp'+st+'.html', str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    flag1 = 0
    flag2 = 0
    # while ((flag1!=1)&(flag2!=3)):
    #     try:
    #         html_text = spider(n_url)
    #         flag1 = 1
    #     except (requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
    #         flag2 = flag2 + 1
    #         print(n_url+"connect failed!")
    html_text,flag2 = spider(n_url)
    # html_text = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=4
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('dl')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].dd.a.attrs['href']
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('date/(.*?)/', (get_news[n].dd.a.attrs['href']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].dt.a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('dd',{'class':'detail'}).text
    # print(n_detail)
    #####链接
    # n_url = 'https://packetstormsecurity.com'+get_news[n].dt.a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=4

        while(n<15):
            n_time = re.findall('date/(.*?)/', (get_news[n].dd.a.attrs['href']))[0]
            ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
            ########只显示how_day内的新闻
            n_title = get_news[n].dt.a.text
            n_detail = get_news[n].find('dd',{'class':'detail'}).text
            n_url = 'https://packetstormsecurity.com'+get_news[n].dt.a.attrs['href']


            a.write(str(n_time).strip()+'\n')
################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')

            # a.write(str(n_detail).strip()+'\n')
            a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def ten_4(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://threatpost.com/"
    a = open(way, str(how_write), encoding='utf-8')
    # st = str(tmp_x)
    # a = open(r'.\tmp'+st+'.html', str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    flag1 = 0
    flag2 = 0
    # while ((flag1!=1)&(flag2!=3)):
    #     try:
    #         html_text = spider(n_url)
    #         flag1 = 1
    #     except (requests.exceptions.SSLError, KeyError, UnicodeDecodeError, IndexError):
    #         flag2 = flag2 + 1
    #         print(n_url+"connect failed!")
    html_text,flag2 = spider(n_url)
    # html_text = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.html','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('article',{'class':'c-card c-card--horizontal--half@md c-card--horizontal@lg c-card--horizontal--flat@md'})  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].time.attrs['datetime']
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('h2').a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('p').text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].find('a').attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<6):
            n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
            ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
            ########只显示how_day内的新闻
            n_title = get_news[n].find('h2').a.text
            n_detail = get_news[n].find('p').text
            n_url = get_news[n].find('a').attrs['href']


            a.write(str(n_time).strip()+'\n')
################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')

            # a.write(str(n_detail).strip()+'\n')
            a.write(Youdao.go(str(n_detail).strip()) + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def ten_5(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://exploit.kitploit.com/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('div',{'class':'post'})  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].find('time').attrs['datetime']
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].div.h3.a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].div.h3.a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<6):
            ##时间
            n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].div.h3.a.text
            # ##细节
            # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
            ##链接
            n_url = get_news[n].div.h3.a.attrs['href']

            a.write(str(n_time).strip()+'\n')
        ################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
        ################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')
            # a.write(str(n_detail).strip()+'\n')
            # a.write(Youdao.go(str(n_detail).strip()) + '\n')
            #####################
            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def ten_6(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://labs.nettitude.com/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('article')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].time.attrs['datetime']
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('h3').a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].div.text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<6):
            ##时间
            n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].find('h3').a.text
            ##细节
            n_detail = get_news[n].div.text
            ##链接
            n_url = get_news[n].a.attrs['href']

            a.write(str(n_time).strip()+'\n')
        ################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
        ################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')
            # a.write(str(n_detail).strip()+'\n')
            a.write(Youdao.go(str(n_detail).strip()) + '\n')
            #####################
            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def ten_7(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "http://blogs.360.cn/archives"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find('article').find_all('li')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].span.text
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = 'http://blogs.360.cn'+str(get_news[n].a.attrs['href'])
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<6):
            # print(n)
            ##时间
            n_time = get_news[n].span.text
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].a.text
            ##细节
            # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
            ##链接
            n_url = 'http://blogs.360.cn'+str(get_news[n].a.attrs['href'])

            a.write(str(n_time).strip()+'\n')
        ################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
        ################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')
            # a.write(str(n_detail).strip()+'\n')
            # a.write(Youdao.go(str(n_detail).strip()) + '\n')
            #####################
            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def three_1(how_write,how_day,way=r'.\tmp.txt',header=0):
    n_url = "https://www.exploit-db.com/remote/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url,1)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find('tbody').find_all('tr')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].td.text
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('td',{'class':'description'}).text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].find('td',{'class':'description'}).a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<10):
            ##时间
            n_time = str(get_news[n].td.text).strip()
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].find('td',{'class':'description'}).text
            ##细节
            type = 1
            try:
                n_detail = get_news[n].find('td', {'class': 'platform'}).a.text
            except(AttributeError):
                print('no type')
                type = 0
            ##链接
            n_url = get_news[n].find('td', {'class': 'description'}).a.attrs['href']

            a.write(str(n_time).strip() + '\n')
            ################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
            ################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip()) + '\n')
            #####################
            # a.write(str(n_detail).strip()+'\n')
            if (type == 1):
                a.write('适用平台：' + str(n_detail).strip() + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.close()

def three_2(how_write,how_day,way=r'.\tmp.txt',header=0):
    n_url = "https://www.exploit-db.com/webapps/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url,1)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find('tbody').find_all('tr')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].td.text
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('td',{'class':'description'}).text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].find('td',{'class':'description'}).a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<10):
            ##时间
            n_time = str(get_news[n].td.text).strip()
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].find('td',{'class':'description'}).text
            ##细节
            type = 1
            try:
                n_detail = get_news[n].find('td', {'class': 'platform'}).a.text
            except(AttributeError):
                print('no type')
                type = 0
            ##链接
            n_url = get_news[n].find('td', {'class': 'description'}).a.attrs['href']

            a.write(str(n_time).strip() + '\n')
            ################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
            ################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip()) + '\n')
            #####################
            # a.write(str(n_detail).strip()+'\n')
            if (type == 1):
                a.write('适用平台：' + str(n_detail).strip() + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.close()

def three_3(how_write,how_day,way=r'.\tmp.txt',header=0):
    n_url = "https://www.exploit-db.com/local/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url,1)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find('tbody').find_all('tr')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].td.text
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('td',{'class':'description'}).text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].find('td',{'class':'description'}).a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<10):
            ##时间
            n_time = str(get_news[n].td.text).strip()
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].find('td',{'class':'description'}).text
            ##细节
            type = 1
            try:
                n_detail = get_news[n].find('td', {'class': 'platform'}).a.text
            except(AttributeError):
                print('no type')
                type = 0
            ##链接
            n_url = get_news[n].find('td', {'class': 'description'}).a.attrs['href']

            a.write(str(n_time).strip() + '\n')
            ################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
            ################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip()) + '\n')
            #####################
            # a.write(str(n_detail).strip()+'\n')
            if (type == 1):
                a.write('适用平台：' + str(n_detail).strip() + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.close()

def three_4(how_write,how_day,way=r'.\tmp.txt',header=0):
    n_url = "https://www.exploit-db.com/dos/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url,1)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find('tbody').find_all('tr')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].td.text
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('td',{'class':'description'}).text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].find('td',{'class':'description'}).a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<10):
            ##时间
            n_time = str(get_news[n].td.text).strip()
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].find('td',{'class':'description'}).text
            ##细节
            type = 1
            try:
                n_detail = get_news[n].find('td', {'class': 'platform'}).a.text
            except(AttributeError):
                print('no type')
                type = 0
            ##链接
            n_url = get_news[n].find('td', {'class': 'description'}).a.attrs['href']

            a.write(str(n_time).strip() + '\n')
            ################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
            ################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip()) + '\n')
            #####################
            # a.write(str(n_detail).strip()+'\n')
            if (type == 1):
                a.write('适用平台：' + str(n_detail).strip() + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.close()

def three_5(how_write,how_day,way=r'.\tmp.txt',header=0):
    n_url = "https://www.exploit-db.com/papers/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url,1)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find('tbody').find_all('tr')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].td.text
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('td',{'class':'description'}).text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].find('td',{'class':'description'}).a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<10):
            ##时间
            n_time = str(get_news[n].td.text).strip()
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].find('td',{'class':'description'}).text
            ##细节
            type = 1
            try:
                n_detail = get_news[n].find('td', {'class': 'platform'}).a.text
            except(AttributeError):
                print('no type')
                type = 0
            ##链接
            n_url = get_news[n].find('td', {'class': 'description'}).a.attrs['href']

            a.write(str(n_time).strip() + '\n')
            ################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
            ################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip()) + '\n')
            #####################
            # a.write(str(n_detail).strip()+'\n')
            if (type == 1):
                a.write('适用平台：' + str(n_detail).strip() + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.close()

def three_6(how_write,how_day,way=r'.\tmp.txt',header=0):
    n_url = "https://www.exploit-db.com/shellcode/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url,1)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find('tbody').find_all('tr')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].td.text
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('td',{'class':'description'}).text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].find('td',{'class':'description'}).a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<10):
            ##时间
            n_time = str(get_news[n].td.text).strip()
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].find('td',{'class':'description'}).text
            ##细节
            type = 1
            try:
                n_detail = get_news[n].find('td', {'class': 'platform'}).a.text
            except(AttributeError):
                print('no type')
                type = 0
            ##链接
            n_url = get_news[n].find('td', {'class': 'description'}).a.attrs['href']

            a.write(str(n_time).strip() + '\n')
            ################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
            ################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip()) + '\n')
            #####################
            # a.write(str(n_detail).strip()+'\n')
            if (type == 1):
                a.write('适用平台：' + str(n_detail).strip() + '\n')

            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("-------------------------------" + '\n')
    a.write("----------https://www.exploit-db.com/" + '\n')
    a.close()

def three_7(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://null-byte.wonderhowto.com/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    # html_text,flag2 = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    # n=0
    # soup = BeautifulSoup(html_text, 'html.parser')
    # get_news = soup.find('div',{'class':'article-list article-list-mode4'}).find_all('article')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].find('i',{'class':'fa fa-clock-o'}).attrs['datetime']
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].div.h3.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].div.p.text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].div.h3.a.attrs['href']
    # print(n_url)
#############################################################
    url_list=['https://null-byte.wonderhowto.com/how-to/metasploit-basics/',
              'https://null-byte.wonderhowto.com/how-to/facebook-hacks/',
              'https://null-byte.wonderhowto.com/how-to/password-cracking/',
              'https://null-byte.wonderhowto.com/how-to/wi-fi-hacking/',
              'https://null-byte.wonderhowto.com/how-to/linux-basics/',
              'https://null-byte.wonderhowto.com/how-to/mr-robot-hacks/',
              'https://null-byte.wonderhowto.com/how-to/hack-like-a-pro/',
              'https://null-byte.wonderhowto.com/how-to/forensics/',
              'https://null-byte.wonderhowto.com/how-to/recon/',
              'https://null-byte.wonderhowto.com/how-to/social-engineering/',
              'https://null-byte.wonderhowto.com/how-to/networking-basics/',
              'https://null-byte.wonderhowto.com/how-to/evading-av-software/',
              'https://null-byte.wonderhowto.com/how-to/spy-tactics/'
              ]
    for nx_url in url_list:
        html_text, flag2 = spider(nx_url)
        soup = BeautifulSoup(html_text, 'html.parser')
        get_news = soup.find('div', {'class': 'article-list article-list-mode4'}).find_all('article')
        a = open(way, 'a', encoding='utf-8')
        if(flag2 != 3):
            # soup = BeautifulSoup(html_text, 'html.parser')
            # get_news = soup.find_all('div', {'class':'col-md-4'})
            n=0

            while(n<6):
                ##时间
                n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
            ########只显示how_day内的新闻
                span_time = click.day_span(n_time,1,1)
                if(span_time>how_day):
                    break
                if(span_time==-1):
                    print(n_url+"时间格式有问题")
                    break
            ########只显示how_day内的新闻
                ##标题
                n_title = get_news[n].div.h3.text
                ##细节
                n_detail = get_news[n].div.p.text
                ##链接
                n_url = get_news[n].div.h3.a.attrs['href']

                a.write(re.findall('how-to/(.*?)/',nx_url)[0]+'---------------\n')
                a.write(str(n_time).strip()+'\n')
            ################不用翻译组
                # a.write(n_title.strip()+'\n')
                # a.write(str(n_detail).strip()+'\n')
            ################翻译组
                # a.write(n_title.strip()+'\n')
                a.write(Youdao.go(n_title.strip())+'\n')
                # a.write(str(n_detail).strip()+'\n')
                a.write(Youdao.go(str(n_detail).strip()) + '\n')
                #####################
                a.write(n_url+'\n')
                a.write('\n')
                n = n+1
        a.write("---------------------end"+'\n')
        a.close()

def three_8(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "http://ringk3y.com/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('article')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].find('span',{'class':'pull-left'}).text
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].find('a').text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'entry-content clearfix'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].find('a').attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<6):
            ##时间
            n_time = str(get_news[n].find('span',{'class':'pull-left'}).text).strip()
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,0,0)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].find('a').text
            ##细节
            n_detail = get_news[n].find('div',{'class':'entry-content clearfix'}).text
            ##链接
            n_url = get_news[n].find('a').attrs['href']

            a.write(str(n_time).strip()+'\n')
        ################不用翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
        ################翻译组
            # a.write(n_title.strip()+'\n')
            a.write(Youdao.go(n_title.strip())+'\n')
            # a.write(str(n_detail).strip()+'\n')
            a.write(Youdao.go(str(n_detail).strip()) + '\n')
            #####################
            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def three_9(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://www.seebug.org/vuldb/vulnerabilities"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    # html_text,flag2 = spider(n_url,2)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    # n=0
    # soup = BeautifulSoup(html_text, 'html.parser')
    # get_news = soup.find('tbody').find_all('tr')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].find('td',{'class':'text-center datetime hidden-sm hidden-xs'}).text
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].td.a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('a',{'class':'vul-title'}).text
    # print(n_detail)
    #####链接
    # n_url = "https://www.seebug.org"+get_news[n].td.a.attrs['href']
    # print(n_url)
#############################################################
    n_url=[
        'https://www.seebug.org/vuldb/vulnerabilities',
        'https://www.seebug.org/vuldb/vulnerabilities?has_poc=true'
    ]
    for n_urlx in n_url:
        html_text, flag2 = spider(n_urlx, 2)
        soup = BeautifulSoup(html_text, 'html.parser')
        get_news = soup.find('tbody').find_all('tr')  #找有某属性的标签
        a = open(way, 'a', encoding='utf-8')
        # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
        if(flag2 != 3):
            # soup = BeautifulSoup(html_text, 'html.parser')
            # get_news = soup.find_all('div', {'class':'col-md-4'})
            n=0

            while(n<6):
                ##时间
                n_time = get_news[n].find('td',{'class':'text-center datetime hidden-sm hidden-xs'}).text
            ########只显示how_day内的新闻
                span_time = click.day_span(n_time,1,1)
                if((n!=0)&(span_time>how_day)):
                    break
                if(span_time==-1):
                    print(n_url+"时间格式有问题")
                    break
            ########只显示how_day内的新闻
                ##标题
                n_title = get_news[n].td.a.text
                ##细节
                n_detail = get_news[n].find('a',{'class':'vul-title'}).text
                ##链接
                n_url = "https://www.seebug.org"+get_news[n].td.a.attrs['href']

                a.write(str(n_time).strip()+'\n')
            ################不用翻译组
                a.write(n_title.strip()+'\n')
                a.write(str(n_detail).strip()+'\n')
            ################翻译组
                # a.write(n_title.strip()+'\n')
                # a.write(Youdao.go(n_title.strip())+'\n')
                # a.write(str(n_detail).strip()+'\n')
                # a.write(Youdao.go(str(n_detail).strip()) + '\n')
                #####################
                a.write(n_url+'\n')
                a.write('\n')
                n = n+1
        a.write("---------------------"+'\n')
        a.close()

def three_10(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://paper.seebug.org/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('article')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].time.attrs['datetime']
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].header.h5.a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('section',{'class':'post-content'}).text
    # print(n_detail)
    #####链接
    # n_url = 'https://paper.seebug.org/'+get_news[n].header.h5.a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<6):
            ##时间
            n_time = get_news[n].time.attrs['datetime']
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].header.h5.a.text
            ##内容
            n_detail = get_news[n].find('section',{'class':'post-content'}).text
            ##链接
            n_url = 'https://paper.seebug.org/'+get_news[n].header.h5.a.attrs['href']

            a.write(str(n_time).strip()+'\n')
        ################不用翻译组
            a.write(n_title.strip()+'\n')
            a.write(str(n_detail).strip()+'\n')
        ################翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(Youdao.go(n_title.strip())+'\n')
            # a.write(str(n_detail).strip()+'\n')
            # a.write(Youdao.go(str(n_detail).strip()) + '\n')
            #####################
            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def three_11(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "http://www.freebuf.com/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url,3)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('div',{'class':'news-info'})  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].find('span',{'class':'time'}).text
    # print(str(n_time).strip())
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].dl.dt.a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].dl.find('dd',{'class':'text'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].dl.dt.a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<6):
            ##时间
            n_time = str(get_news[n].find('span',{'class':'time'}).text).strip()
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].dl.dt.a.text
            ##内容
            n_detail = get_news[n].dl.find('dd',{'class':'text'}).text
            ##链接
            n_url = get_news[n].dl.dt.a.attrs['href']

            a.write(str(n_time).strip()+'\n')
        ################不用翻译组
            a.write(n_title.strip()+'\n')
            a.write(str(n_detail).strip()+'\n')
        ################翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(Youdao.go(n_title.strip())+'\n')
            # a.write(str(n_detail).strip()+'\n')
            # a.write(Youdao.go(str(n_detail).strip()) + '\n')
            #####################
            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def three_12(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "http://www.cnvd.org.cn/flaw/list.htm"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=10
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find('tbody').find_all('tr')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = str(get_news[n].find_all('td',{'width':'13%'})[1].text).strip()
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].td.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = 'http://www.cnvd.org.cn'+get_news[n].td.a.attrs['href']
    # print(n_url)
#############################################################
    a = open(way, 'a', encoding='utf-8')
    # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    if(flag2 != 3):
        # soup = BeautifulSoup(html_text, 'html.parser')
        # get_news = soup.find_all('div', {'class':'col-md-4'})
        n=0

        while(n<6):
            ##时间
            n_time = str(get_news[n].find_all('td',{'width':'13%'})[1].text).strip()
        ########只显示how_day内的新闻
            span_time = click.day_span(n_time,1,1)
            if((n!=0)&(span_time>how_day)):
                break
            if(span_time==-1):
                print(n_url+"时间格式有问题")
                break
        ########只显示how_day内的新闻
            ##标题
            n_title = get_news[n].td.text
            ##细节
            # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
            ##链接
            n_url = 'http://www.cnvd.org.cn'+get_news[n].td.a.attrs['href']

            a.write(str(n_time).strip()+'\n')
        ################不用翻译组
            a.write(n_title.strip()+'\n')
            # a.write(str(n_detail).strip()+'\n')
        ################翻译组
            # a.write(n_title.strip()+'\n')
            # a.write(Youdao.go(n_title.strip())+'\n')
            # a.write(str(n_detail).strip()+'\n')
            # a.write(Youdao.go(str(n_detail).strip()) + '\n')
            #####################
            a.write(n_url+'\n')
            a.write('\n')
            n = n+1
    a.write("---------------------"+'\n')
    a.close()

def three_x(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://0x00sec.org/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp1.html','w',encoding='utf-8')
    # a.write(html_text)
    # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_newsx = soup.html.body  #找有某属性的标签
    get_news = BeautifulSoup(get_newsx, 'html.parser')
    print(get_news)
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].time.attrs['datetime']
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].h3.a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].h3.a.attrs['href']
    # print(n_url)
#############################################################
    # a = open(way, 'a', encoding='utf-8')
    # # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    # if(flag2 != 3):
    #     # soup = BeautifulSoup(html_text, 'html.parser')
    #     # get_news = soup.find_all('div', {'class':'col-md-4'})
    #     n=0
    #
    #     while(n<6):
    #         ##时间
    #         n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    #     ########只显示how_day内的新闻
    #         span_time = click.day_span(n_time)
    #         if((n!=0)&(span_time>how_day)):
    #             break
    #         if(span_time==-1):
    #             print(n_url+"时间格式有问题")
    #             break
    #     ########只显示how_day内的新闻
    #         ##标题
    #         n_title = get_news[n].h3.a.text
    #         ##细节
    #         n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    #         ##链接
    #         n_url = get_news[n].h3.a.attrs['href']
    #
    #         a.write(str(n_time).strip()+'\n')
    #     ################不用翻译组
    #         # a.write(n_title.strip()+'\n')
    #         # a.write(str(n_detail).strip()+'\n')
    #     ################翻译组
    #         # a.write(n_title.strip()+'\n')
    #         a.write(Youdao.go(n_title.strip())+'\n')
    #         # a.write(str(n_detail).strip()+'\n')
    #         a.write(Youdao.go(str(n_detail).strip()) + '\n')
    #         #####################
    #         a.write(n_url+'\n')
    #         a.write('\n')
    #         n = n+1
    # a.write("---------------------"+'\n')
    # a.close()

def m_news(how_write,how_day,way=r'.\tmp.txt'):
    n_url = "https://www.hackread.com/hacking-news/"
    a = open(way, str(how_write), encoding='utf-8')
    a.write("--------------")
    a.write(n_url+"\n")
    a.close()
    html_text,flag2 = spider(n_url)
################################测试
    ################将网站源码放到文本
    # a = open(r'./tmp.txt','w',encoding='utf-8')
    #     # a.write(html_text)
    #     # a.close()
    ###############打印源码
    # print(html_text)
    ###########找新闻在哪
    n=0
    soup = BeautifulSoup(html_text, 'html.parser')
    get_news = soup.find_all('article')  #找有某属性的标签
    # print(get_news[n])
    ###############新闻信息分类
    #####时间
    # n_time = get_news[n].time.attrs['datetime']
    # print(n_time)
    ##用模块re提取
    # n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    # print(n_time)
    ##用模块xpath提取出不在某个具体标签中的元素
    # n_time1 = etree.HTML(str(n_time)).xpath('//div[@class="item-label"]/text()')
    # print(n_time1)
    # ####
    # print(n_time1[n])
    #####标题
    # n_title = get_news[n].h3.a.text
    # print(n_title)
    #####内容
    # n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    # print(n_detail)
    #####链接
    # n_url = get_news[n].h3.a.attrs['href']
    # print(n_url)
#############################################################
    # a = open(way, 'a', encoding='utf-8')
    # # a = open(r'.\tmp'+st+'.html', 'a',encoding='utf-8')
    # if(flag2 != 3):
    #     # soup = BeautifulSoup(html_text, 'html.parser')
    #     # get_news = soup.find_all('div', {'class':'col-md-4'})
    #     n=0
    #
    #     while(n<6):
    #         ##时间
    #         n_time = re.findall('(.*?)T', (get_news[n].find('time').attrs['datetime']))[0]
    #     ########只显示how_day内的新闻
    #         span_time = click.day_span(n_time)
    #         if((n!=0)&(span_time>how_day)):
    #             break
    #         if(span_time==-1):
    #             print(n_url+"时间格式有问题")
    #             break
    #     ########只显示how_day内的新闻
    #         ##标题
    #         n_title = get_news[n].h3.a.text
    #         ##细节
    #         n_detail = get_news[n].find('div',{'class':'text hidden-xs'}).text
    #         ##链接
    #         n_url = get_news[n].h3.a.attrs['href']
    #
    #         a.write(str(n_time).strip()+'\n')
    #     ################不用翻译组
    #         # a.write(n_title.strip()+'\n')
    #         # a.write(str(n_detail).strip()+'\n')
    #     ################翻译组
    #         # a.write(n_title.strip()+'\n')
    #         a.write(Youdao.go(n_title.strip())+'\n')
    #         # a.write(str(n_detail).strip()+'\n')
    #         a.write(Youdao.go(str(n_detail).strip()) + '\n')
    #         #####################
    #         a.write(n_url+'\n')
    #         a.write('\n')
    #         n = n+1
    # a.write("---------------------"+'\n')
    # a.close()

if __name__ == '__main__':

    # file_name1 = r'C:\Users\gutou\Desktop\news\10_9_news.txt'   # 文件名
    file_name1 = r'.\news.txt'  # 文件名

    # file_name2 = r'C:\Users\gutou\Desktop\news\10_9_bugnews.txt'   # 文件名
    file_name2 = r'.\bugnews.txt'  # 文件名
    days = 0        # 几天以内的新闻（0代表今天）
    #
    try:
        eight('w',days,file_name1)
    except(IndexError):
        print("小飞机没开,快去点开")
        exit(1)
    one('a',days,file_name1)
    # print('\n')
    two('a',days,file_name1)
    # print('\n')
    three('a',days,file_name1)
    # print('\n')
    four('a',days,file_name1)
    # print('\n')
    five('a',days,file_name1)
    # print('\n')
    six('a',days,file_name1)
    # print('\n')
    nine('a',days,file_name1)
    # print('\n')
    ten('a',days,file_name1)
    # print('\n')
    ten_1('a',days,file_name1)
    # print('\n')
    ten_2('a',days,file_name1)
    # print('\n')
    ten_3('a',days,file_name1)
    # print('\n')
    ten_4('a',days,file_name1)
    # print('\n')
    ten_5('a',days,file_name1)
    # print('\n')
    ten_6('a', days, file_name1)
    ten_7('a',days,file_name1)

    #############漏洞信息
    three_1('w', days, file_name2)    # head = 1
    three_2('a', days, file_name2)
    three_3('a', days, file_name2)
    three_4('a', days, file_name2)
    three_5('a', days, file_name2)
    three_6('a', days, file_name2)    # head = 1
    three_7('a', days, file_name2)
    three_8('a', days, file_name2)
    three_10('a', days, file_name2)
    three_12('a', days, file_name2)
    three_9('a', days, file_name2)  # head = 2
    three_11('a', days, file_name2)     # head = 3
