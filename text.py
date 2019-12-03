# -*- coding: utf-8 -*-
# @ ziheng_wind

import re
from rake_nltk import Rake

with open('2010/Peace in the Middle East/20.txt','r',encoding='utf8') as f:
    txt = f.read()
r = Rake()
r.extract_keywords_from_text(txt)
text_rank = r.get_ranked_phrases()

for line in text_rank[:int(len(text_rank)*float('0.06'))]:
    if re.search('Peace in the Middle East',line,re.IGNORECASE):
        print('1')
    else:
        print('0')

