import re
from time import sleep

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
    st.header("Coinpan Crawler")
    iter = st.number_input("몇 페이지까지의 데이터를 추출하시겠습니까?: ", 1, 10)
    sleep(30)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disble-gpu")

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.implicitly_wait(5)

    url = "https://coinpan.com/index.php?mid=free&page=1"
    driver.get(url)

    data = []

    text_tag = "div.board_read.rd > div.section_wrap.section_border_0 > div > div > p"

    for i in range(3, iter + 3):
        message_bar = st.empty()
        message_bar.text(f"{i-2} 페이지의 키워드를 추출하고 있습니다.")

        for j in range(6, 26):
            words = {}
            title = driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({j}) > td.title > a").text
            words["title"] = parsing_keywords(title)

            words["name"] = driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({j}) > td.author > a").text

            words["date"] = driver.find_element(
                By.CSS_SELECTOR,
                f"tr:nth-child({j}) > td.time > span.number > span.regdateHour",
            ).text

            words["freq"] = driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({j}) > td.readed > span.number").text

            driver.find_element(By.CSS_SELECTOR, f"table > tbody > tr:nth-child({j}) > td.title > a").click()

            sleep(3)

            ptags = driver.find_elements(By.CSS_SELECTOR, text_tag)
            contexts = ""
            try:
                if ptags != 0:
                    for k in range(len(ptags)):
                        texts = f"div.board_read.rd > div.section_wrap.section_border_0 > div > div > p:nth-child({k+1})"
                        context = driver.find_element(By.CSS_SELECTOR, texts).text
                        context = parsing_keywords(context)
                        contexts = contexts + " " + context
                    words["contexts"] = contexts

                else:
                    pass
            except BaseException:
                pass
            driver.back()

            data.append(words)

        if i <= 7:
            driver.find_element(
                By.CSS_SELECTOR,
                f"div.section_footer > div > ul > li:nth-child({i}) > a",
            ).click()
            sleep(3)

        else:
            driver.find_element(
                By.CSS_SELECTOR,
                "div.section_footer > div > ul > li:nth-child(8) > a",
            ).click()
            sleep(3)

    driver.quit()

    df = pd.DataFrame.from_dict(data).drop_duplicates(subset=["제목"])
    df.columns = ["제목", "작성자", "업로드_일자", "조회수", "게시글_내용"]
    csv = df.to_csv().encode("utf-8")

    message_bar.empty()
    message_bar.download_button(label="파일을 다운로드하세요.", data=csv, file_name="coinpan.csv", mime="text/csv")


if __name__ == "__main__":
    main()
