import requests
!pip install fake_useragent
from fake_useragent import UserAgent
import json
import numpy as np
import pandas as pd

def ua():
    return(UserAgent().random)
headers = {'User-Agent': ua()}
#ID of parties if it is needed:
#party_id_dict = {'72100024': 'Единая Россия',
#                '72100027' : 'Справедливая Россия',
#                '72100005' : 'ЛДПР',
#                '72100004' : 'КПРФ',
#                '72100029': 'неизвестно',
#                '-' : 'другие'}

#===================================for only one word===================================:
bad_word = 'экология'
z = requests.get('https://stateduma.api.dekoder.org/term/ru/' + bad_word, headers = headers)
z1 = z.json()
df = pd.DataFrame({'Date' : [int(i) for i in list(z1['frequencies'].keys())],
                   'count' : [z1['frequencies'][i]['count'] for i in list(z1['frequencies'].keys())],
                   'frequencies' : [z1['frequencies'][i]['freq'] for i in list(z1['frequencies'].keys())],
                  } )
df.set_index('Date', inplace = True)
print(df.head(3))

#===================================for different words===================================:
words = ('экология', 'климат', 'климатический', 'экологическая безопасность', 'экологическая проблема', 'экологически чистый',
         'загрязнение', 'экосистема', 'окружающая среда', 'биоресурсы', 'озоновый', 'вырубка лес', 'отходы',
         'мусор', 'мусорный', 'мусороперерабатывающий', 'мусоросжигательный', 'мусоропереработка', 'свалка', 'техногенный',
         'киотский', 'радиоактивный', 'шиес', 'парниковый', 'примесь', 'ТБО', 'парижское соглашение', 'водоохранный', 'сточная вода')

eco_df = pd.DataFrame({'Date' : [int(i) for i in list(z1['frequencies'].keys())]})
eco_df.set_index('Date', inplace = True)
for j in words:
    z = requests.get('https://stateduma.api.dekoder.org/term/ru/' + j)#, headers = headers)
    z1 = z.json()
    df = pd.DataFrame({'Date' : [int(i) for i in list(z1['frequencies'].keys())],
                       j : [z1['frequencies'][i]['count'] for i in list(z1['frequencies'].keys())]}
                      )
    df.set_index('Date', inplace = True)
    #print(df.tail(2))
    eco_df = pd.concat([eco_df, df], axis=1)
    del df
eco_df = eco_df.fillna(0)
eco_df['sum'] = eco_df.sum(axis=1)
print(eco_df.iloc[0:5,-5:])

eco_df['sum'].plot()
