##module import 

import time
import json
import urllib
import requests
import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from wordcloud import WordCloud
from konlpy.tag import Okt

import streamlit as st

#set font & size
plt.rcParams["font.family"] = "Hancom MalangMalang"
plt.rcParams['figure.figsize'] = 10,10
sns.set(font="apple gothic", rc={"axes.unicode_minus":False}, style='white')
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


def no_space(text):
    a = re.sub("\n", "", text)
    b = re.sub("  ", "", a)
    c = re.sub("[0-9]+ ", "", b)
    return c


def counter_to_DataFrame(key_words):
    word_df = pd.DataFrame(key_words.items()) #Data Frame 형성
    word_df.columns = ['단어', '빈도']
    word_df = word_df.sort_values(['빈도'],ascending = False).reset_index(drop = True) #내림차순 정렬
    return word_df


def wordcloud(key_words):
    df = counter_to_DataFrame(key_words)
    df = df.drop([0,1,2]) #불용어 제거
    df = df[df['단어'].str.len() > 1]
    df.reset_index(drop=True, inplace=True)
    
    wc = WordCloud(font_path = '/NanumBarunGothic.ttf',
                    width = 500,
                    height = 500,
                    background_color='white').generate_from_frequencies(df.set_index('단어').to_dict()['빈도'])
    return wc
    

def main():
    st.header('코인판 키워드 분석기')
    st.subheader('페이지가 너무 많을 경우, 속도가 느려집니다.')
    iter = st.number_input('몇 페이지까지의 키워드를 확인하겠습니까?: ', 1, 100)
    
    
    key_words = {}
    token_list = []
    words = []

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--window-size=1920x1080')
    options.add_argument("--disble-gpu")

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.implicitly_wait(5)

    url = 'https://coinpan.com/index.php?mid=free&page=1'
    driver.get(url)


    for i in range(3, iter + 3):
        
        word_lis = []
            
        #딜레이 생성
        seed = np.random.randint(100)
        np.random.seed(seed)
        a = np.random.randint(5)
        time.sleep(a)
        
        
        for j in range(6,26):
            title = driver.find_element_by_css_selector(f'table > tbody > tr:nth-child({j}) > td.title > a').get_attribute('text')
            name = driver.find_element_by_css_selector(f'table > tbody > tr:nth-child({j}) > td.author > a').get_attribute('text')
            date = driver.find_element_by_xpath(f'/table/tbody/tr[{j}]/td[4]/span').get_attribute('innerText')
            freq = driver.find_element_by_xpath(f'/table/tbody/tr[{j}]/td[5]/span').get_attribute('innerText')
            title = no_space(title)
            
            words.append([title, name, date, freq])
            word_lis.append(title)
        token = tokenizer(word_lis) #tokenizer
        key_words = word_counter(token, key_words) #Counter Dict 형성
        
        if i <= 7:
            driver.find_element_by_xpath(f'/div[2]/div/ul/li[{i}]/a').click()
            time.sleep(3)
        else : 
            driver.find_element_by_xpath(f'/div[2]/div/ul/li[8]/a').click()
            time.sleep(3)


    driver.quit()

    fig = plt.figure()
    plt.title(str(iter) +'페이지까지의 '+ 'KeyWords')
    wc = wordcloud(key_words)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    st.pyplot(fig)


if __name__ == '__main__':
    main()
