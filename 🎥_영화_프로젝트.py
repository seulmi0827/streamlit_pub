import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import webbrowser 


st.set_page_config(
    page_icon="🎥",
    page_title="영화 프로젝트"
)

# Title
st.title("🎥 영화 프로젝트")


# 영화 제목 입력
st.caption("Search for movies on Kinolights :cherries:")
name_input = st.text_input("영화 제목을 입력하세요:", "")


if name_input:
    driver = webdriver.Chrome()
    driver.implicitly_wait(2)

    try:
        driver.get('https://m.kinolights.com/')

        # 팝업 처리
        div_tag1 = driver.find_element(By.CSS_SELECTOR, '#contents div.mini-popup-footer > button')
        div_tag1.click()
        div_tag2 = driver.find_element(By.CSS_SELECTOR, '#contents section.home-shortcut-list.shortcut-section div > button')
        div_tag2.click()
        div_tag2.click()
        div_tag2.click()

        # 검색 페이지 이동 및 검색어 입력
        driver.find_element(By.CSS_SELECTOR, '#contents > div.main-content-wrap > div > div > a').click()
        driver.find_element(By.CSS_SELECTOR, '#contents > div.search-header.search-header--empty-page > div > div > form > input').click()
        driver.find_element(By.CSS_SELECTOR, '#contents > div.search-header.search-header--empty-page > div > div > form > input').send_keys(f'{name_input}')
        
        # 첫 번째 검색 결과 클릭
        driver.find_element(By.CSS_SELECTOR, '#searchContentList > div:nth-child(1) > a > div.body__info').click()
        time.sleep(1)

        action = ActionChains(driver)
        if driver.find_elements(By.CSS_SELECTOR, '#contents > div.info.tab-item > section:nth-child(2)'):
            action.move_to_element(driver.find_element(By.CSS_SELECTOR, '#contents > div.info.tab-item > section:nth-child(2)')).perform()
        else:
            action.move_to_element(driver.find_element(By.CSS_SELECTOR, '#contents > div.info.tab-item > section.mx-16.mt-40.mb-40')).perform()
        
        if driver.find_elements(By.CSS_SELECTOR, '#contents > div.info.tab-item > section:nth-child(1) > div > div > div > button'):
            더보기 = driver.find_element(By.CSS_SELECTOR, '#contents > div.info.tab-item > section:nth-child(1) > div > div > div > button')
            더보기.click()
        time.sleep(1)

        # 제목 및 점수 정보
        name_score = driver.find_elements(By.CSS_SELECTOR, '#contents > div.movie-info-container > div.content-info > div.movie-header-area')
        title, indicators = name_score[0].text.split('\n', 1)

        st.markdown("### 📋 영화 정보", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<p style='font-size:14px;'>제목</p><p style='font-size:16px;'><b>{title}</b></p>", unsafe_allow_html=True)
        col2.markdown(f"<p style='font-size:14px;'>영문 제목 · 제작년도</p><p style='font-size:16px;'>{indicators.splitlines()[0]}</p>", unsafe_allow_html=True)
        col3.markdown(f"<p style='font-size:14px;'>신호등 지수</p><p style='font-size:16px;'>{indicators.splitlines()[1]}</p>", unsafe_allow_html=True)

        col4, col5, col6 = st.columns(3)
        col4.markdown(f"<p style='font-size:14px;'>로튼토마토</p><p style='font-size:16px;'>{indicators.splitlines()[2]}</p>", unsafe_allow_html=True)
        col5.markdown(f"<p style='font-size:14px;'>IMDb</p><p style='font-size:16px;'>{indicators.splitlines()[3]}</p>", unsafe_allow_html=True)
        col6.markdown(f"<p style='font-size:14px;'>별점</p><p style='font-size:16px;'>{indicators.splitlines()[4]}</p>", unsafe_allow_html=True)

        # 서비스 중인 OTT 정보
        st.markdown("### 📡 OTT 서비스 정보", unsafe_allow_html=True)
        if driver.find_elements(By.CSS_SELECTOR, '#contents > div.info.tab-item > section.mx-16.mt-40.mb-40 > div.movie-ott-wrap > div > button.price-tab.active > span:nth-child(2)'):
            OTT = driver.find_elements(By.CSS_SELECTOR, '#contents > div.info.tab-item > section.mx-16.mt-40.mb-40 > div.movie-ott-wrap > div > button.price-tab.active > span:nth-child(2)')
            st.markdown(f"<p style='font-size:16px;'>현재 <b>{OTT[0].text}</b>개의 OTT에서 서비스 중입니다.</p>", unsafe_allow_html=True)
        elif '2024' in indicators.splitlines()[0]:
            st.write("현재 영화관에서 상영 중인 영화입니다.")
        else:
            st.write("OTT에 등록되지 않은 영화입니다.")

        # 줄거리
        st.markdown("### 📖 이야기 소개", unsafe_allow_html=True)
        Intro = driver.find_elements(By.CSS_SELECTOR, '#contents > div.info.tab-item > section:nth-child(1) > div > div > div > span')
        if '줄거리' in Intro[0].text:
            st.markdown(f"<p style='font-size:14px;'>{Intro[0].text}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='font-size:14px;'>줄거리: {Intro[0].text}</p>", unsafe_allow_html=True)

        # 부가 정보
        st.markdown("### ℹ️ 추가 정보", unsafe_allow_html=True)
        Info = driver.find_elements(By.CSS_SELECTOR, '#contents > div.info.tab-item > section:nth-child(1) > ul')
        info_lines = Info[0].text.split('\n')
        col_a, col_b, col_c = st.columns(3)
        for i in range(0, len(info_lines), 6):  # 분산 표시
            if i + 1 < len(info_lines):
                col_a.markdown(f"<p style='font-size:14px;'>{info_lines[i]}:</p><p style='font-size:16px;'>{info_lines[i + 1]}</p>", unsafe_allow_html=True)
            if i + 3 < len(info_lines):
                col_b.markdown(f"<p style='font-size:14px;'>{info_lines[i + 2]}:</p><p style='font-size:16px;'>{info_lines[i + 3]}</p>", unsafe_allow_html=True)
            if i + 5 < len(info_lines):
                col_c.markdown(f"<p style='font-size:14px;'>{info_lines[i + 4]}:</p><p style='font-size:16px;'>{info_lines[i + 5]}</p>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"영화 정보를 찾을 수 없습니다: {e}")
    finally:
        driver.quit()
