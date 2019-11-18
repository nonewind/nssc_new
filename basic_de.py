# -*- coding: utf-8 -*-
# @ ziheng_wind

import json
import re
import csv
import time
import shutil
import sys

import requests
import urllib3
from bs4 import BeautifulSoup


def req_url_text_handle(data_url, keywords, year, xx, url):
    """ 
    title           文章标题
    type(title)     <class 'str'>
    data_bs         文章发布的时间
    line            text->每行内容
    xx              控制文章写入数目
    """
    
    keywords = keywords.replace('\n', '')
    bsobj = BeautifulSoup(data_url, 'html.parser')
    try:
        title = bsobj.title.text
        data_bs = (bsobj.find('span', class_="heading__meta").text).replace(
        '\r', '').replace('\n', '').replace('\t', '')
        text_bs = bsobj.findAll('p', class_="rte__paragraph")
    except:
        title = 'NoneType'
        data_bs = 'NoneType'
        text_bs = 'NoneType'
    # 直接写入date_code 再读取
    
    text_other_bs = bsobj.find_all('blockquote', class_="quote__content") #判定是否有内容
    if text_other_bs:
        for line in text_other_bs:
            line = str(line).replace('<blockquote class="quote__content">', '').replace('<br/>', '').replace(
                '<span class="quote__icon i-quote-marks" data-grunticon-embed="true"></span></blockquote>', '')
            text_bs.insert(-1,line)
    if text_bs:
        with open(str(year)+'/'+keywords+'/'+str(xx)+'.txt', 'w+', encoding='utf8') as f:
            # 为了断点续操时 写入文件不重 采用w+ 和 清空文双保险
            f.seek(0)
            f.truncate()

            f.write(title)
            f.write('\n')
            f.write(data_bs)
            f.write('\n')
            for line in text_bs:
                line = str(line)
                if '<' in line or '>' in line:
                    con = True
                    while con:
                        line_list = list(line)
                        try:
                            tag_l = line_list.index('<')
                            tag_r = line_list.index('>')
                        except:
                            break
                        del line_list[tag_l:tag_r+1]
                        
                        line = "".join(line_list)
                        if '<' in line or '>' in line:
                            con = True
                        else:
                            con = False
                f.write(line)
                f.write('\n')
    else:
        with open('href/error_url.log', 'a+', encoding='utf8') as f:
            f.write(url)
            f.write('\n')

def req_second(sock5, port, time_sleep, keywords, year):
    """
    data_url        获取的单个网址的详细内容
    """
    with open('href/url.log', 'r+', encoding='utf8') as f:
        url_list = f.readlines()
        f.seek(0)  # 将文件定位到文件首
        f.truncate()  # 清空文件
    xx = 0

    print('\t根据去除最后20%的无效内容的实施')
    print('\t当前原有:',len(url_list),'个页面')
    print('\t只取前80%后:',int(len(url_list)*0.8),'个页面')
    
    url_list = url_list[:int(len(url_list)*0.8)]
    for url in url_list:
        print(
            "\t=当前是关键词", keywords, "的第", xx+1, "个页面 总", len(url_list), "页面="
        )
        url = url.replace('\n', '')
        data_url = req_get(sock5, port, url)
        if data_url:
            req_url_text_handle(data_url, keywords, year, xx, url)
            xx += 1
        else:
            print("\t捕捉到一个错误 错误代码1001")
            continue

    print(
        "\t=当前关键词的页面爬取完毕 开始纠错="
    )
    with open('href/error_url.log', 'r+', encoding='utf8') as f:
        url_error_list = f.readlines()
        f.seek(0)
        f.truncate()


def req_json_dumps(req_json):
    """
    json_d          解码成dict
    """
    json_d = json.loads(req_json)
    i = 0
    if json_d["items"]:
        while i <= 20:
            try:
                link = json_d["items"][i]["link"]
                num_large = json_d['itemsTotal']
                url_addr = 'https://www.auswaertiges-amt.de'+link
                with open('href/url.log', 'a+', encoding='utf8') as f:
                    f.write(url_addr)
                    f.write('\n')
            except:
                break
            i += 1
        return True
    else:
        return False


def req_get(sock5, port, url):
    """
    函数部分
    url             网址
    sock5           代理开启
    port            代理端口
    headers         请求头
    proxies         代理端口
    """
    urllib3.disable_warnings()  # 去掉烦人的报警
    headers = {
        'Host': 'www.auswaertiges-amt.de',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'close'  # 关闭多余的连接 这里卡到我怀疑猿生
    }
    proxies = {
        'http': 'socks5://127.0.0.1:{}'.format(port)
    }  # 设置sock5代理
    if sock5 == '1':
        try:
            req = requests.get(url, headers=headers,
                               verify=False, proxies=proxies).text
        except:
            req = False
    else:
        try:
            req = requests.get(url, headers=headers, verify=False).text
        except:
            req = False
    return req


def time_change(year):
    """
    支持的时间为2018 - 2006
    """
    first = '-02-01 23:59:59'
    last = '-01-31 23:59:59'
    if year == '2018':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2017':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2016':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2015':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2014':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2013':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2012':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2011':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2010':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2009':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2008':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2007':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2006':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2005':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2004':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2003':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2002':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2001':
        time_first = year + first
        time_last = str(int(year)+1) + last
    elif year == '2000':
        time_first = year + first
        time_last = str(int(year)+1) + last
    else:
        print("\t=年份暂时不支持 ps 2006-2018=")
        oooo = input("\t=Error! 年份输入错误   按任意键结束程序=")
        exit()

    timeArray_F = int(time.mktime(time.strptime(
        time_first, "%Y-%m-%d %H:%M:%S"))) * 1000
    #timestamp_F = int(time.mktime(timeArray_F)) * 1000
    timeArray_L = int(time.mktime(time.strptime(
        time_last, "%Y-%m-%d %H:%M:%S"))) * 1000
    #timestamp_L = int(time.mktime(timeArray_L)) *1000

    return timeArray_F, timeArray_L


def reques(line, sock5, port, time_sleep, year):
    """
    函数部分
    line            关键词
    sock5           代理开启
    port            代理端口
    time_sleep      休眠时间
    year            年份

    url部分
        _time_F_   时间戳开始
        _time_F_   时间戳结束
        _limit_    页面最大可接受数据数 10-20
        _offset_   页面数据获取偏移量   
    """
    contral = True
    offset = 0
    conture = 0
    (time_F, time_L) = time_change(year)
    line = line.replace(' ', '%20')
    while contral:
        url = 'https://www.auswaertiges-amt.de/ajax/json-filterlist/en/search/-/101054?search={}'.format(line)+'&documenttype=2186712%23AAPress%2BOR%2BAASpeech%2BOR%2BAAInterview&startdate={}'.format(
            time_F)+'&enddate={}'.format(time_L)+'&startfield=date&endfield=date&limit=20&offset={}'.format(offset)
        req_json = req_get(sock5, port, url)
        if req_json:
            contral = req_json_dumps(req_json)
            time.sleep(int(time_sleep))
            offset += 20
        else:
            print("致命错误 错误原因:请求网址错误 返回值为空 等30s再来一次")
            req_json = req_get(sock5, port, url)
            conture += 1
            if conture == 2:
                print(
                    "重试达到最大次数 告辞"
                )
                req_error()

def req_error():
    vv = True
    while vv:
        error_input = input("输入Y退出")
        if error_input == 'Y' or error_input == 'y':
            vv = False
        else:
            vv = True
    exit()

if __name__ == "__main__":
    pass