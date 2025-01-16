import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib import font_manager, rc
import seaborn as sns

# Streamlit 제목
st.title("	:bar_chart:영화 모아보기_barchart")
'-----------------------'
# 폰트 설정
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

st.markdown('''##### :star2:**2024 영화 데이터**  
: 베테랑2, 하얼빈, 서울의 봄, 탈주, 파일럿, 소방관, 핸섬가이즈, 하이재킹, 파묘
''')
col1, col2, col3, col4 = st.columns(4)
col1_button = col1.button('영화별 평점 비교')
col2_button = col2.button('북미 박스오피스 수익 비교')
col3_button = col3.button('OTT개수와 영화별 수상 갯수 비교')
col4_button = col4.button('영화별 러닝타임 비교')
'--------------------------------'
st.markdown('''##### :star2:**과거 성공 영화 데이터**  
: 기생충, 설국열차, 명량, 괴물, 국제시장, 봄 여름 가을 겨울 그리고 봄, 아가씨, 올드보이, 신과함께-인과연, 부산행, 버닝)
''')
col5, col6, col7, col8 = st.columns(4)
col5_button = col5.button('과거 영화별 평점 비교')
col6_button = col6.button('과거 북미 박스오피스 수익 비교')
col7_button = col7.button('과거 OTT개수와 수상 갯수 비교')
col8_button = col8.button('과거 영화별 러닝타임 비교')


# JSON 파일에서 데이터 읽기
with open("C:\sesac\project1\_current_movie.json", "r",encoding="utf-8") as f:
    movies_total = json.load(f)
 
# DataFrame으로 변환
df = pd.DataFrame(movies_total).T
df.reset_index(inplace=True)
df.rename(columns={"index": "영화"}, inplace=True)

# 필요한 데이터 형식 변환
df["cine21전문가 평점"] = pd.to_numeric(df["cine21전문가 평점"], errors="coerce")
df["cine21네티즌 평점"] = pd.to_numeric(df["cine21네티즌 평점"], errors="coerce")
df["imdbscore"] = pd.to_numeric(df["imdbscore"], errors="coerce")
df["북미boxoffice"] = df["북미boxoffice"].str.replace("[\$,]", "", regex=True).astype(float, errors="ignore")
df["수상갯수"] = pd.to_numeric(df["수상갯수"], errors="coerce")
df["OTT개수"] = pd.to_numeric(df["OTT개수"], errors="coerce")
df["신호등지수"] = df["신호등지수"].replace("%","", regex=True).astype(float, errors="ignore")/10
df["러닝타임"] = df["러닝타임"].str.replace("분", "").astype(float)

# 영화별 평점 비교

# 버튼 생성
if col1_button:
    st.subheader("영화별 평점 비교")

    # 데이터 변환
    ratings = df[["영화", "cine21전문가 평점", "cine21네티즌 평점", "imdbscore", "신호등지수"]].melt(
        id_vars="영화", var_name="평점종류", value_name="평점"
    )

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=ratings, x="영화", y="평점", hue="평점종류", palette="coolwarm", ax=ax)

    # 그래프 설정
    ax.set_title("영화별 평점 비교", fontsize=16)
    ax.set_xlabel("영화", fontsize=12)
    ax.set_ylabel("평점", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()

    # Streamlit에 그래프 출력
    st.pyplot(fig)


# 북미 박스오피스 수익 비교
if col2_button:
    st.subheader("북미 박스오피스 수익 비교")

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df, x="영화", y="북미boxoffice", palette="coolwarm", ax=ax)

    # 그래프 설정
    ax.set_title("북미 박스오피스 수익 비교", fontsize=16)
    ax.set_xlabel("영화", fontsize=12)
    ax.set_ylabel("수익 ($)", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()

    # Streamlit에 출력
    st.pyplot(fig)

# OTT개수와 영화별 수상 갯수 비교
if col3_button:
    st.subheader("OTT 개수와 수상 개수 비교")

    # 데이터 준비
    ott_data = df[["영화", "OTT개수", "수상갯수"]].melt(id_vars="영화", var_name="종류", value_name="개수")

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=ott_data, x="영화", y="개수", hue="종류", palette="coolwarm", ax=ax)

    # 그래프 설정
    ax.set_title("OTT 개수와 수상 개수 비교", fontsize=16)
    ax.set_xlabel("영화", fontsize=12)
    ax.set_ylabel("개수", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.legend(title="종류")
    plt.tight_layout()

    # Streamlit에 출력
    st.pyplot(fig)

# 영화별 러닝타임 비교
if col4_button:
    st.subheader("영화별 러닝타임 비교")

    # 데이터 확인 및 전처리
    if df["러닝타임"].isnull().any():
        st.write("러닝타임에 결측값이 있습니다. 결측값을 0으로 대체합니다.")
        df["러닝타임"] = df["러닝타임"].fillna(0)

    # 러닝타임 기준으로 정렬
    sorted_df = df.sort_values("러닝타임", ascending=False)

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=sorted_df, x="영화", y="러닝타임", palette="coolwarm", ax=ax)

    # 그래프 설정
    ax.set_title("영화별 러닝타임 비교", fontsize=16)
    ax.set_xlabel("영화", fontsize=12)
    ax.set_ylabel("러닝타임 (분)", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()

    # Streamlit에 출력
    st.pyplot(fig)

#과거---------------------------------------------------------------------------

# JSON 파일에서 데이터 읽기
with open("C:\sesac\project1\_famous_movie.json", "r",encoding="utf-8") as f:
    movies_total = json.load(f)
 
# DataFrame으로 변환
df = pd.DataFrame(movies_total).T
df.reset_index(inplace=True)
df.rename(columns={"index": "영화"}, inplace=True)

# 필요한 데이터 형식 변환
df["cine21전문가 평점"] = pd.to_numeric(df["cine21전문가 평점"], errors="coerce")
df["cine21네티즌 평점"] = pd.to_numeric(df["cine21네티즌 평점"], errors="coerce")
df["imdbscore"] = pd.to_numeric(df["imdbscore"], errors="coerce")
df["북미boxoffice"] = df["북미boxoffice"].str.replace("[\$,]", "", regex=True).astype(float, errors="ignore")
df["수상갯수"] = pd.to_numeric(df["수상갯수"], errors="coerce")
df["OTT개수"] = pd.to_numeric(df["OTT개수"], errors="coerce")
df["신호등지수"] = df["신호등지수"].replace("%","", regex=True).astype(float, errors="ignore")/10
df["러닝타임"] = df["러닝타임"].str.replace("분", "").astype(float)

# 영화별 평점 비교
# 영화별 평점 비교

# 버튼 생성
if col5_button:
    st.subheader("영화별 평점 비교")

    # 데이터 변환
    ratings = df[["영화", "cine21전문가 평점", "cine21네티즌 평점", "imdbscore", "신호등지수"]].melt(
        id_vars="영화", var_name="평점종류", value_name="평점"
    )

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=ratings, x="영화", y="평점", hue="평점종류", palette="coolwarm", ax=ax)

    # 그래프 설정
    ax.set_title("영화별 평점 비교", fontsize=16)
    ax.set_xlabel("영화", fontsize=12)
    ax.set_ylabel("평점", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()

    # Streamlit에 그래프 출력
    st.pyplot(fig)


# 북미 박스오피스 수익 비교
if col6_button:
    st.subheader("북미 박스오피스 수익 비교")

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df, x="영화", y="북미boxoffice", palette="coolwarm", ax=ax)

    # 그래프 설정
    ax.set_title("북미 박스오피스 수익 비교", fontsize=16)
    ax.set_xlabel("영화", fontsize=12)
    ax.set_ylabel("수익 ($)", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()

    # Streamlit에 출력
    st.pyplot(fig)

# OTT개수와 영화별 수상 갯수 비교
if col7_button:
    st.subheader("OTT 개수와 수상 개수 비교")

    # 데이터 준비
    ott_data = df[["영화", "OTT개수", "수상갯수"]].melt(id_vars="영화", var_name="종류", value_name="개수")

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=ott_data, x="영화", y="개수", hue="종류", palette="coolwarm", ax=ax)

    # 그래프 설정
    ax.set_title("OTT 개수와 수상 개수 비교", fontsize=16)
    ax.set_xlabel("영화", fontsize=12)
    ax.set_ylabel("개수", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.legend(title="종류")
    plt.tight_layout()

    # Streamlit에 출력
    st.pyplot(fig)

# 영화별 러닝타임 비교
if col8_button:
    st.subheader("영화별 러닝타임 비교")

    # 데이터 확인 및 전처리
    if df["러닝타임"].isnull().any():
        st.write("러닝타임에 결측값이 있습니다. 결측값을 0으로 대체합니다.")
        df["러닝타임"] = df["러닝타임"].fillna(0)

    # 러닝타임 기준으로 정렬
    sorted_df = df.sort_values("러닝타임", ascending=False)

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=sorted_df, x="영화", y="러닝타임", palette="coolwarm", ax=ax)

    # 그래프 설정
    ax.set_title("영화별 러닝타임 비교", fontsize=16)
    ax.set_xlabel("영화", fontsize=12)
    ax.set_ylabel("러닝타임 (분)", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()

    # Streamlit에 출력
    st.pyplot(fig)