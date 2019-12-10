# -*- coding: utf-8 -*-
# @ ziheng_wind

import configparser
import csv
import os
import shutil

import basic_de
import ten_fen


def flie_reader(year):
    keyword = []
    row = ['Keywords', 'Date', 'Article Title',
           'Grounds', 'Original Text', 'Num']
    # 这里改写赋值 利用ini文件的特性 将每一个主题下的关键词存为一个list 方便读取 
    with open(year+'.csv', 'a+', encoding='utf-8', newline='') as csvflie:
        w_csv_f = csv.writer(csvflie)
        w_csv_f.writerow(row)
    with open('app/关键词.txt', 'r', encoding='utf8') as f:
        keywords_list = f.read()
    keyword = keywords_list.split('\n')

    with open('app/赋值关键词.txt', 'r', encoding='utf8') as f:
        _Assignment_list = f.read()
    Assignment = _Assignment_list.split('\n')

    with open('app/赋值人物.txt', 'r', encoding='utf8') as f:
        _Assignment_character = f.read()
    Assignment_character = _Assignment_character.split('\n')

    rank_text_and_res = ten_fen.Fen(
        keyword, year, Assignment, Assignment_character)
    rank_text_and_res.text_read()

    # shutil.rmtree(year) #删除临时爬取的文件
    print(
        year, '搞定!'
    )


def class_1(sock5, port, keywords, time_sleep, year):
    for line in keywords:
        try:  # 写入断点文件 方便未来续断操作
            with open('app/断点.txt', 'w', encoding='utf8') as f:
                f.write(line)
        except:
            pass
        line = line.replace('\n', '')
        print(
            "\t=开始爬取关键词", line, '=\n'
        )
        basic_de.reques(line, sock5, port, time_sleep,
                        year)  # 获取json中的url拼接写入url.log
        print(
            "\t=关键词", line, "url获取完成 进入关键词深度爬取=\n"
        )
        basic_de.req_second(sock5, port, time_sleep, line, year)
        print(
            "\t=..关键词", line, "爬完了..=\n"
        )
        # 清空断点文件
        try:
            with open('app/断点.txt', 'w+', encoding='utf8') as f:
                f.seek(0)  # 将文件定位到文件首
                f.truncate()  # 清空文件
        except:
            pass
    print(
        "=所有的关键词都已经爬取到本地了 接下来是本地处理已经爬取好的文件=\n",
        "=这次使用的是一个py文件调用自编函数 打包以后还是必须要py源文件存在 无法对我的源码进行加密处理=\n",
        "=下一次考虑使用单个exe解决问题=\n"
    )


def contral():
    """
    这是爬虫的主控函数 包含一个class_1函数 
    class_1 函数中的所有的引入均来自 basic_de.py
    """
    # 导入配置文件
    print(
        "================================\n",
        '       @python 3.7.0 @ziheng_wind  \n',
        '================================\n\n\n\n\n',
        '= 默认第一步结束后开始第二步 =\n'
    )
    print(
        "\t=初始化部分=\n"
    )
    year = input("\t=输入年份=")
    config = configparser.ConfigParser()
    config.read('app/爬虫设置.ini', encoding='utf8')
    # type(sock5) = str
    sock5 = config['User']['sock5']
    port = config['User']['sock5_prot']
    time_sleep = config['User']['time_sleep']
    try:
        os.mkdir(year)
    except:
        print("\t=目录已经创建==")
    # 获取关键词list
    with open('app/关键词.txt', 'r', encoding='utf8') as f:
        keywords = f.readlines()
    path_frist = os.getcwd()  # 获取当前目录 组合成新的目录 按照关键词进行建目录
    path = path_frist + '/' + year
    os.chdir(path)
    for line in keywords:
        line = line.replace('\n', '')
        try:
            os.makedirs(line)
        except:
            continue
    print(
        "\t=初始化结束 步入正题="
    )
    path_last = os.path.abspath(os.path.join(os.getcwd(), ".."))  # 获取上级目录 并返回
    os.chdir(path_last)
    # 传入函数
    class_1(sock5, port, keywords, time_sleep, year)  # 关键词爬取
    print(
        "\n\n\t=开始文件操作=\n"
    )
    return year


def duandian(year):
    list_keyword = []
    config = configparser.ConfigParser()
    config.read('app/爬虫设置.ini', encoding='utf8')
    # type(sock5) = str
    sock5 = config['User']['sock5']
    port = config['User']['sock5_prot']
    time_sleep = config['User']['time_sleep']

    with open('app/断点.txt', 'r+', encoding='utf8') as f:
        data_duandian = f.read()
        data_duandian = str(data_duandian).replace('\n', '')
        f.seek(0)
        f.truncate()

    with open('app/关键词.txt', 'r', encoding='utf8') as f:
        data_keywords_list = f.readlines()
        for line in data_keywords_list:
            line = line.replace('\n', '')
            list_keyword.append(line)
    index_seek = list_keyword.index(data_duandian)
    list_keyword_new = list_keyword[index_seek:]
    # 调用本身的函数
    print(
        "断点续操的起始点为", data_duandian
    )
    class_1(sock5, port, list_keyword_new, time_sleep, year)


if __name__ == "__main__":
    oo = str(input("输入操作步骤 1为爬虫部分-2为文件操作部分 -3为断点续操\n"))
    if oo == '1':
        year = contral()
        flie_reader(year)
    elif oo == '2':
        year = str(input('请输入文件操作年份:\n'))
        flie_reader(year)
    elif oo == '3':
        year = str(input('请输入文件操作年份:\n'))
        duandian(year)
        flie_reader(year)
        # 根据输入确定的年份 找到断点文件中的关键词 根据关键词 删除关键词log中的所有的文件 而后接着爬
    else:
        print("输入错误 告辞")
        exit()
