import re
import time

import numpy as np
import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def text_checker(tag, driver):
    if driver.find_elements(By.CSS_SELECTOR, tag):
        return True
    else:
        return False


def parsing_keywords(text):
    no_space = re.sub("\n", "", text)
    no_enter = re.sub("  ", "", no_space)
    no_nbsp = re.sub("&nbsp;", "", no_enter)
    return no_nbsp


def main():
    st.header("코인판 크롤러")
    iter = st.number_input("몇 페이지까지의 데이터를 추출하시겠습니까?: ", 1, 100)
    time.sleep(30)
    message_bar = st.empty()

    message_bar.text(f"{iter} 페이지까지의 키워드를 추출하고 있습니다.")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disble-gpu")

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.implicitly_wait(5)

    url = "https://coinpan.com/index.php?mid=free&page=1"
    driver.get(url)

    words = []
    text_tag = "div.board_read.rd > div.section_wrap.section_border_0 > div > div > p"

    for i in range(3, iter + 3):

        for j in range(6, 26):
            title = driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({j}) > td.title > a").text

            name = driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({j}) > td.author > a").text

            date = driver.find_element(
                By.CSS_SELECTOR, f"tr:nth-child({j}) > td.time > span.number > span.regdateHour"
            ).text

            freq = driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({j}) > td.readed > span.number").text

            driver.find_element(By.CSS_SELECTOR, f"table > tbody > tr:nth-child({j}) > td.title > a").click()

            # delaying
            seed = np.random.randint(100)
            np.random.seed(seed)
            a = np.random.randint(5)
            time.sleep(a)

            ptags = driver.find_elements(By.CSS_SELECTOR, text_tag)
            contexts = ""
            try:
                if ptags != 0:
                    for k in range(len(ptags)):
                        texts = f"div.board_read.rd > div.section_wrap.section_border_0 > div > div > p:nth-child({k+1})"
                        context = driver.find_element(By.CSS_SELECTOR, texts).text
                        context = parsing_keywords(context)
                        contexts = contexts + " " + context

                else:
                    pass
            except BaseException:
                pass
            driver.back()

            title = parsing_keywords(title)
            words.append([title, name, date, freq, contexts])

        if i <= 7:
            driver.find_element(
                By.CSS_SELECTOR, f"div.section_footer > div > ul > li:nth-child({i}) > a"
            ).click()
            time.sleep(3)

        else:
            driver.find_element(
                By.CSS_SELECTOR, "div.section_footer > div > ul > li:nth-child(8) > a"
            ).click()
            time.sleep(3)

    driver.quit()

    df = pd.DataFrame(words, columns=["제목", "작성자", "업로드_일자", "조회수", "게시글_내용"]).drop_duplicates(subset=["제목"])
    data = df.to_csv().encode("utf-8")

    message_bar.empty()
    message_bar.download_button(label="파일을 다운로드하세요.", data=data, file_name="coinpan.csv", mime="text/csv")


if __name__ == "__main__":
    main()
