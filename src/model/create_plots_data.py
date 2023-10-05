from datetime import datetime

import pandas as pd
from konlpy.tag import Okt


def get_csv_data():
    now = datetime.today().strftime("%Y%m%d")
    df = pd.read_csv(f"src/data/coinpan_{now}.csv", index_col=0)
    return df


def create_wordcloud_data():
    okt = Okt()

    def word_counter(value):
        key_words = {}
        for i in value:
            if i not in key_words:
                key_words[i] = 1
            elif i in key_words:
                key_words[i] += 1
        return key_words

    def tokenizer(text):
        lis = []
        for i in text:
            if isinstance(i, str):
                word = okt.nouns(i)
                for k in word:
                    lis.append(k)
        return lis

    def counter_to_DataFrame(key_words):
        word_df = pd.DataFrame(key_words.items())
        word_df.columns = ['words', 'frequent']
        word_df = word_df.sort_values(['frequent'], ascending=False).reset_index(drop=True)
        return word_df

    df = get_csv_data()
    lis = df['게시글_내용'].tolist()

    data = counter_to_DataFrame(word_counter(tokenizer(lis)))
    word_dic = data.to_dict()
    return word_dic


def create_barplot_data():
    df = get_csv_data()
    df1 = pd.DataFrame(df.groupby('작성자').size()).reset_index()
    df1.columns = ['name', 'frequent']
    name_dic = df1.to_dict()
    return name_dic
