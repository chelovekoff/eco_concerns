import requests
!pip install fake_useragent
from fake_useragent import UserAgent
import json
import numpy as np
import pandas as pd
!pip install wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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
word = 'экология' #'ecology' in Russian
z = requests.get('https://stateduma.api.dekoder.org/term/ru/' + word, headers = headers)
#----------------adapted from Nikita Kharakhnin 03.02.2022-----------------
z1 = z.json()
df = pd.DataFrame({'Date' : [int(i) for i in list(z1['frequencies'].keys())],
                   'count' : [z1['frequencies'][i]['count'] for i in list(z1['frequencies'].keys())],
                   'frequencies' : [z1['frequencies'][i]['freq'] for i in list(z1['frequencies'].keys())],
                  } )
df.set_index('Date', inplace = True)
#---------------------------end of adaptation------------------------------
print(df.head(3))

#===================================for different words===================================:
#Russian words mentioned during deliberations in the State Duma and associated with environmental issues:
words = ('экология', 'климат', 'климатический', 'экологическая безопасность', 'экологическая проблема', 'экологически чистый',
         'загрязнение', 'экосистема', 'окружающая среда', 'биоресурсы', 'озоновый', 'вырубка лес', 'отходы',
         'мусор', 'мусорный', 'мусороперерабатывающий', 'мусоросжигательный', 'мусоропереработка', 'свалка', 'техногенный',
         'киотский', 'радиоактивный', 'шиес', 'парниковый', 'примесь', 'ТБО', 'парижское соглашение', 'водоохранный', 'сточная вода'
         'лесной пожар', 'питьевая вода', 'радиация', 'чернобыль', 'фукусим', 'ядерный отходы'
         )

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
eco_df['total'] = eco_df.sum(axis=1)
print(eco_df.iloc[0:3,-6:])
eco_df.to_excel("eco_duma.xlsx")
#===========================================================================================

#------The plot for the total number of environmental concern mentions each year:
plt.figure(figsize=(18,4))
plt.bar(x = eco_df.index, height=eco_df['total'])
plt.title('Total number of environmental concern')
plt.ylabel('mentions')
plt.xticks(np.arange(1994, 2022, 1))
plt.axvline(2004, color='pink', linestyle='--', lw=2, label='The Kyoto Protocol Ratification')
plt.axvline(2018, color='lightblue', linestyle='--', lw=2, label='The Beginning of Shiyes Protests')
plt.legend(loc='upper left')
plt.show()

#-----------------The plot for the word map of environmental concerns, 2014-2021:
eco_sum = pd.DataFrame(eco_df.iloc[:,:-1].sum(axis=0))
eco_sum.columns = ['total']

#Phrases as a single word:
for el in eco_sum.index:
  new_word = el.replace(' ', '_')
  eco_sum = eco_sum.rename(index={el: new_word})

text = eco_sum.to_string(header=None)
wordcloud = WordCloud(width=1600, height=800).generate(str(text))
plt.figure(figsize=(15,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
