##module import 

import time
import json
import urllib
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from konlpy.tag import Okt
import streamlit as st

#set font & size
plt.rcParams["font.family"] = "Hancom MalangMalang"
plt.rcParams['figure.figsize'] = 10,10
sns.set(font="Hancom MalangMalang", rc={"axes.unicode_minus":False}, style='white')
okt = Okt()


def word_counter(value, key_words):
    for i in value:
        if i not in key_words:
            key_words[i] = 1 #최초 언어
        elif i in key_words:
            key_words[i] += 1 #중복 언어
    return key_words


def tokenizer(text):
    lis = []
    for i in text:
        word = okt.nouns(i) #토큰화
        for k in word:
            lis.append(k)
    return lis


def counter_to_DataFrame(key_words):
    word_df = pd.DataFrame(key_words.items()) #Data Frame 형성
    word_df.columns = ['단어', '빈도']
    word_df = word_df.sort_values(['빈도'],ascending = False).reset_index(drop = True) #내림차순 정렬
    return word_df

def main():
    st.header('코인판 키워드 분석기')
    st.subheader('최대 100페이지까지의 키워드를 찾을 수 있습니다.')
    iter = st.number_input('몇 페이지까지의 키워드를 확인하겠습니까?: ', 1, 100)
    
    key_words = {}
    word_lis = []

    for i in range(iter):
        url = 'https://coinpan.com/index.php?mid=free&page=' + str(i)
        
        #딜레이 생성
        seed = np.random.randint(100)
        np.random.seed(seed)
        a = np.random.randint(5)
        time.sleep(a)

        #url 호출
        session = requests.session()
        res = session.get(url)
        res.raise_for_status()

        #html 추출
        soup = BeautifulSoup(res.text, 'html.parser')
        a = soup.find_all("td", attrs = {'class':'title'}) #제목이 들어있는 태그의 텍스트 추출
        text = str(a)
        num = len(a)
        words = re.compile('[가-힣]+').findall(text) #한글 제외 전부 제거
        words = words[25:-18] #불용어 제거
        
        token = tokenizer(words) #토큰화
        word_lis.append(token)
        key_words = word_counter(token, key_words) #Counter Dict 형성
        
    df = counter_to_DataFrame(key_words)
    df = df.drop([0,1,2,3]) #불용어 제거
    df = df[df['단어'].str.len() > 1]
    df.reset_index(drop=True, inplace=True)
    
    wc = WordCloud(font_path = 'C:\\Users\\cjsso\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NanumBarunGothic.ttf',
                    width = 500,
                    height = 500,
                    background_color='white').generate_from_frequencies(df.set_index('단어').to_dict()['빈도'])

    fig = plt.figure()
    plt.title(str(iter) +'페이지까지의 '+ 'KeyWords')
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    st.pyplot(fig)


if __name__ == '__main__':
    main()