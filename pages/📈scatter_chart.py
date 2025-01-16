import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib import font_manager, rc
import seaborn as sns

# Streamlit 제목
st.title("	:bar_chart:영화 비교하기_scatter chart")
'-----------------------'
# 폰트 설정
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

st.markdown('''##### :star2:**2024 vs 과거 영화**''')
col1, col2, col3, col4 = st.columns(4)
col1_button = col1.button('영화별 평점 비교')
col2_button = col2.button('북미 박스오피스 수익 비교')
col3_button = col3.button('OTT개수와 영화별 수상 갯수 비교')
col4_button = col4.button('영화별 러닝타임 비교')

# JSON 파일에서 데이터 읽기
with open("C:\sesac\project1\_current_movie.json", "r",encoding="utf-8") as f:
    movies_total = json.load(f)
with open("C:\sesac\project1\_famous_movie.json", "r",encoding="utf-8") as f:
    movies_total2 = json.load(f)
 
# DataFrame으로 변환
df = pd.DataFrame(movies_total).T
df.reset_index(inplace=True)
df.rename(columns={"index": "2024영화"}, inplace=True)
df2 = pd.DataFrame(movies_total2).T
df2.reset_index(inplace=True)
df2.rename(columns={"index": "과거영화"}, inplace=True)

# 필요한 데이터 형식 변환
df["cine21전문가 평점"] = pd.to_numeric(df["cine21전문가 평점"], errors="coerce")
df["cine21네티즌 평점"] = pd.to_numeric(df["cine21네티즌 평점"], errors="coerce")
df["imdbscore"] = pd.to_numeric(df["imdbscore"], errors="coerce")
df["북미boxoffice"] = df["북미boxoffice"].str.replace("[\$,]", "", regex=True).astype(float, errors="ignore")
df["수상갯수"] = pd.to_numeric(df["수상갯수"], errors="coerce")
df["OTT개수"] = pd.to_numeric(df["OTT개수"], errors="coerce")
df["신호등지수"] = df["신호등지수"].replace("%","", regex=True).astype(float, errors="ignore")/10
df["러닝타임"] = df["러닝타임"].str.replace("분", "").astype(float)
df2["cine21전문가 평점"] = pd.to_numeric(df["cine21전문가 평점"], errors="coerce")
df2["cine21네티즌 평점"] = pd.to_numeric(df["cine21네티즌 평점"], errors="coerce")
df2["imdbscore"] = pd.to_numeric(df["imdbscore"], errors="coerce")
df2["북미boxoffice"] = df["북미boxoffice"].str.replace("[\$,]", "", regex=True).astype(float, errors="ignore")
df2["수상갯수"] = pd.to_numeric(df["수상갯수"], errors="coerce")
df2["OTT개수"] = pd.to_numeric(df["OTT개수"], errors="coerce")
df2["신호등지수"] = df["신호등지수"].replace("%","", regex=True).astype(float, errors="ignore")/10
df2["러닝타임"] = df["러닝타임"].str.replace("분", "").astype(float)

if col1_button:
    st.subheader("영화별 평점 비교")

    # 데이터 변환
    ratings = df[["2024영화", "cine21전문가 평점", "cine21네티즌 평점", "imdbscore", "신호등지수"]].melt(
        id_vars="2024영화", var_name="평점종류", value_name="평점"
    )

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=ratings, x="2024영화", y="평점", hue="평점종류", palette="coolwarm", s=100, ax=ax)

    # 그래프 설정
    ax.set_title("영화별 평점 비교", fontsize=16)
    ax.set_xlabel("영화", fontsize=12)
    ax.set_ylabel("평점", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()

