import os
import re
from datetime import datetime
from time import sleep

import chromedriver_autoinstaller
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


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


def get_data(data):
    now = datetime.today().strftime("%Y%m%d")
    df = pd.DataFrame.from_dict(data)
    df.columns = ["제목", "작성자", "업로드_일자", "조회수", "게시글_내용"]
    df.drop_duplicates(subset=["제목"], inplace=True)
    df.to_csv(f"coinpan_{now}.csv", encoding="utf-8-sig")


def main():
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split(".")[0]
    driver_path = f"./{chrome_ver}/chromedriver"
    if os.path.exists(driver_path):
        print(f"chrome driver is installed: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {"download.default_directory": os.getcwd()})

    options = ["--headless", "--no-sandbox"]
    for option in options:
        chrome_options.add_argument(option)

    driver = webdriver.Chrome(options=chrome_options)

    url = "https://coinpan.com/index.php?mid=free&page=1"
    driver.get(url)

    data = []

    text_tag = "div.board_read.rd > div.section_wrap.section_border_0 > div > div > p"
    print(" ")
    print("\033[96m" + "코인판 크롤러 작동을 시작합니다." + "\033[0m")
    print(" ")
    sleep(3)
    iter = int(input("몇 페이지까지의 키워드를 추출하길 원하시나요? >> "))

    for i in range(3, iter + 3):
        print(" ")
        print("\033[32m" + f"{i-2} 페이지의 키워드를 추출하고 있습니다." + "\033[0m")

        for j in range(6, 26):
            print(" ")
            print("\033[96m" + "================crawling 진행 중==============" + "\033[0m")
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
    get_data(data)


if __name__ == "__main__":
    main()
