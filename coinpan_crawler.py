import re
import time

import chromedriver_autoinstaller
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from konlpy.tag import Okt
from selenium import webdriver
from selenium.webdriver.common.by import By
from wordcloud import WordCloud

# set font & size
plt.rcParams["font.family"] = "Apple Gothic"
plt.rcParams["figure.figsize"] = 10, 10
okt = Okt()


def word_counter(value, key_words):
    for i in value:
        if i not in key_words:
            key_words[i] = 1
        elif i in key_words:
            key_words[i] += 1
    return key_words


def tokenizer(text):
    lis = []
    for i in text:
        word = okt.nouns(i)
        for k in word:
            lis.append(k)
    return lis


def no_space(text):
    a = re.sub("\n", "", text)
    b = re.sub("  ", "", a)
    c = re.sub("[0-9]+ ", "", b)
    return c


def counter_to_DataFrame(key_words):
    word_df = pd.DataFrame(key_words.items())
    word_df.columns = ["단어", "빈도"]
    word_df = word_df.sort_values(["빈도"], ascending=False).reset_index(drop=True)  # 내림차순 정렬
    return word_df


def wordcloud(key_words):
    df = counter_to_DataFrame(key_words)
    df = df.drop([0, 1, 2])  # 불용어 제거
    df = df[df["단어"].str.len() > 1]
    df.reset_index(drop=True, inplace=True)

    wc = WordCloud(font_path="Apple Gothic", width=500, height=500, background_color="white").generate_from_frequencies(
        df.set_index("단어").to_dict()["빈도"]
    )
    return wc


def main():
    st.header("코인판 키워드 분석기")
    st.subheader("페이지가 너무 많을 경우, 속도가 느려질 수 있습니다.")
    iter = st.number_input("몇 페이지까지의 키워드를 확인하겠습니까?: ", 1, 100)

    key_words = {}

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--window-size=1920x1080")
    # options.add_argument("--disble-gpu")

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.implicitly_wait(5)

    url = "https://coinpan.com/index.php?mid=free&page=1"
    driver.get(url)

    for i in range(3, iter + 3):

        word_lis = []

        # 딜레이 생성
        seed = np.random.randint(100)
        np.random.seed(seed)
        a = np.random.randint(5)
        time.sleep(a)

        for j in range(6, 26):
            title = driver.find_element(
                By.CSS_SELECTOR, f"table > tbody > tr:nth-child({j}) > td.title > a"
            ).get_attribute("text")
            title = no_space(title)
            name = driver.find_element(
                By.CSS_SELECTOR, f"table > tbody > tr:nth-child({j}) > td.author > a"
            ).get_attribute("text")

            word_lis.append(title)
        token = tokenizer(word_lis)
        key_words = word_counter(token, key_words)

        if i <= 7:
            driver.find_element(By.XPATH, f"/div[2]/div/ul/li[{i}]/a").click()
            time.sleep(3)
        else:
            driver.find_element(By.XPATH, f"/div[2]/div/ul/li[8]/a").click()
            time.sleep(3)

    driver.quit()

    counter = counter_to_DataFrame(key_words)
    counter = counter[counter["단어"].str.len() > 1]
    counter.reset_index(drop=True, inplace=True)

    fig = plt.figure()
    plt.title(str(iter) + "페이지까지의 " + "KeyWords")
    wc = wordcloud(key_words)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    st.pyplot(fig)


if __name__ == "__main__":
    main()
