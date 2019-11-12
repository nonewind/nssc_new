# -*- coding: utf-8 -*-
# @ ziheng_wind

import re
import os
import csv
import shutil
import sys


def flie_cleaner(keyword,year):
    for row in keyword:
        list_flie_name = []
        path = year+'/'+row+'/'
        flies_cea = os.listdir(path)
        for line in flies_cea:
            line = line.replace('.txt','')
            list_flie_name.append(line)
        
        
def re_seach(bat, flags):
    """
    默认判定不区分大小写\n
    bat         正则规则\n
    flags       需匹配的字符串\n
    return      返回的是bool 
    """
    result = re.compile(bat, re.IGNORECASE).findall(flags)
    return bool(result)

def re_findALL(bat,flags):
    result = re.compile(bat).findall(flags)
    if len(result)>=2:
        return True
    else:
        return False

def csv_fuzhi(text,title,date,keyword_one):
    if re_seach('Humanitarian Aid',text):
        if re_seach('million',text) or re_seach('Billion',text):
            if re_seach('dollar',text) or re_seach('euro',text) or 'EUR' in text:
                return '0.4'
            elif re_seach('speech',date):
                return '0.2'
            elif re_seach('statement',text):
                return '0.1'
            else:
                return False
        elif re_seach('International Conference',text):
            if re_seach('speech',date):
                return '0.3'
            elif re_seach('statement',text):
                return '0.2'
            else:
                return False
        elif re_seach('speech',date):
            if re_seach('speech',text):
                return '0.2'
            else:
                return False
        elif re_seach('statement',text):
            return '0.1'
        else:
            return False
    else:
        return False 


class tran():
    def __init__(self, keyword, year, Assignment, Assignment_character):
        self.keyword = keyword
        self.year = year
        self.Assignment = Assignment
        self.Assignment_character = Assignment_character
        self.csv_row = []
        self.csv_row_new = []
        self.text = ''
        self.date = ''
        self.title = ''

    def flie_read(self):
        for keyword_one in self.keyword:
            xx = 0
            con = True
            while con:
                flie_path = self.year+"/"+keyword_one+"/"+str(xx)+".txt"
                try:
                    with open(flie_path, 'r', encoding='utf8') as f:
                        data = f.readlines()
                    self.contr_key(data, keyword_one)
                except:
                    con = False
                xx += 1


        for lien in self.csv_row:
            print('xxx')
            with open(self.year+'.csv', 'a+', encoding='utf-8', newline='') as csvflie:
                w_csv_f = csv.writer(csvflie)
                w_csv_f.writerow(lien)
            

    def contr_key(self, data, keyword_one):
        """
        除了year 为str外 均为list\n
        keyword                 关键词\n
        year                    年份\n
        Assignment              赋值关键词\n
        Assignment_character    赋值关键人物
        """
        conc = True
        tt = 0
        # 这里使用的是赋值关键词和搜索关键词进行匹配
        while conc:
            try:
                line = self.Assignment[tt]
            except:
                break
            for row in self.Assignment_character:
                # re_seach(keyword_one,str(data)):
                if re_seach(line, str(data)) and re_seach(row, str(data)):
                    if re_findALL(keyword_one,str(data)):
                        self.date = data[1]
                        self.title = data[0]
                        self.data = data[2:]
                        self.csv_write(line, keyword_one, data)
                        conc = False
                        break
            tt += 1

    def csv_write(self, Assignment, keyword_one, data):
        self.text = ''
        self.title = self.title.replace('“', '"').replace('”', '"').replace(
            '’', "'").replace('ö', 'o').replace(' – ', '-').replace('é', 'e').replace(' ´', "'").replace('\n','')
        self.date = self.date.replace('\n','')
        for line in data:
            line = str(line).replace('\n', '////').replace('<strong class="rte__strong">', '').replace(
                '</strong>', '').replace('—', '').replace('<span lang="en-GB">', '').replace(
                    '<abbr class=""rte__abbreviation"" title=""United Nations"">', '').replace(
                        ' <abbr class="rte__abbreviation" title="Organization for Security and Co-operation in Europe">', '').replace(
                            '<abbr class="rte__abbreviation" title="United Nations">', '').replace('“', '"').replace('”', '"').replace(
                                '’', "'").replace('ö', 'o').replace(' – ', '-').replace('é', 'e').replace('é', 'e').replace(
                                ' ´', "'").replace('--', '__')
            self.text+=line
        global rows
        num = csv_fuzhi(self.text,self.title,self.date,keyword_one)
        if 'Speech' in self.date:
            assignment = 'Speech'
        else:
            assignment = Assignment
        if len(self.text)>=30000:
            #text = text.replace(', ',',').replace(' ,',',')
            text_1 = self.text[:15000]
            text_2 = self.text[15000:]
            rows = [keyword_one, self.date, self.title, assignment, text_1,text_2, num]
        elif 'Commissioner' in self.text or 'Human Rights Commissioner' in self.text:
            if keyword_one == 'Death penalty':
                pass
            else:
                rows = []
        # elif year not in date or str(int(year)+1) not in date:
        #     row = []
        elif re_seach(self.year,self.date)  or re_seach(str(int(self.year)+1),self.date):
            rows = [keyword_one, self.date, self.title, assignment, self.text, num]
        else:
            rows = []

        if num:
            pass
        else:
            rows = []
        if bool(rows):
            self.csv_row.append(rows)
        else:
            pass

if __name__ == "__main__":
    pass
