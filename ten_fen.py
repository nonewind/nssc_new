# -*- coding: utf-8 -*-
# @ ziheng_wind

import csv
import re
import configparser

from rake_nltk import Rake


def search_re(bat, flat):
    result = re.search(bat, flat, flags=re.IGNORECASE)
    if result:
        return True
    else:
        return False


def replace_str(string):
    return string.replace('“', '"').replace('”', '"').replace(
        '’', "'").replace('ö', 'o').replace(' – ', '-').replace('é', 'e').replace('é', 'e').replace(
        ' ´', "'").replace('--', '__').replace('\n', '').replace('ú', 'u').replace('á', 'a').replace('‘', "'").replace(
        'ü', '')


class Fen():
    def __init__(self, keyword, year, Assignment, Assignment_character):
        self.keyword = keyword
        self.year = year
        self.Assignment = Assignment
        self.Assignment_character = Assignment_character
        self.path = ''
        self.data_text = ''
        self.Assignment_rate = ''
        self.key_theme = []

    def text_read(self):
        config = configparser.ConfigParser()
        config.read('app/爬虫设置.ini', encoding='utf8')
        self.Assignment_rate = config['User']['rate']
        for key in self.keyword:
            theme_key = configparser.ConfigParser()
            theme_key.read('app/theme.ini', encoding='utf8')
            key_theme_keyword = '{}'.format(key)
            list_key = theme_key['theme'][key_theme_keyword]
            list_key = list_key.split(', ')
            for line in list_key:
                self.key_theme.append(line)

            for i in range(0, 1000):
                self.path = self.year+'/'+key+'/'+str(i)+'.txt'
                try:
                    with open(self.path, 'r', encoding='utf8') as f:
                        self.data_text = f.read()
                    self.text_rank(key)
                except:
                    break

    def text_rank(self, key):
        con = True
        xx = 0
        r = Rake()
        r.extract_keywords_from_text(self.data_text)
        text_rank = r.get_ranked_phrases()
        text_rank_new = text_rank[:int(
            len(text_rank)*float(self.Assignment_rate))]
        while con:
            try:
                text_rank_new_line = text_rank_new[xx]
            except:
                break
            for Assignment_row in self.Assignment:
                if search_re(Assignment_row, text_rank_new_line):
                    self.csv_w(Assignment_row, key, text_rank_new)
                    con = False
                    break  # 这里只需要匹配一次
                else:
                    pass
            xx += 1

    def csv_w(self, Assignment_row, key, text_rank_new):
        line_text = ''
        xy = 0
        for line in self.Assignment_character:
            if search_re(line, self.data_text):
                with open(self.path, 'r', encoding='utf8') as f:
                    text = f.readlines()
                title = replace_str(text[0])
                date = replace_str(text[1])
                if Assignment_row == 'humanitarian aid':
                    num = '0.4'
                    xy = 1
                elif Assignment_row == 'International Conference' or Assignment_row == 'summit' or Assignment_row == 'forum' or Assignment_row == 'dialogue':
                    if search_re('summit',title) or search_re('forum',title) or search_re('dialogue',title):
                        num = '0.3'
                    else:
                        num = '0.2'
                elif Assignment_row == 'Speech':
                    num = '0.2'
                else:
                    num = '0.1'

                for line in text[2:]:
                    line = line.replace('\n', '/////')
                    line_text += line
                line_text = replace_str(line_text)

                # 如果标题中不出现主题内含有关键词，赋值为0.1
                if float(num) < 0.4:
                    for line in self.key_theme:
                        if search_re(line, title):
                            xy = 1
                            break
                if xy == 0:
                    num = '0.1'

                # Law of sea 需要完全匹配
                if key == 'Law of sea':
                    if search_re(key, title):
                        pass
                    else:
                        num = ''
                # interview
                if num != '0.1':
                    if num == '0.4':
                        pass
                    else:
                        if search_re('interview', title):
                            num = '0.1'

                if num:
                    row = [key, date, title, Assignment_row, line_text, num]
                # 人权专员不配拥有姓名
                if 'Human Rights Commissioner' in line_text or 'Human Rights Commissioner' in title:
                    row = []
                if row:
                    with open(self.year+'.csv', 'a+', encoding='utf-8', newline='') as csvflie:
                        w_csv_f = csv.writer(csvflie)
                        w_csv_f.writerow(row)
                break
            else:
                pass


if __name__ == "__main__":
    pass
