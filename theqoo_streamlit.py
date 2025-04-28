import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import base64
import requests
from bs4 import BeautifulSoup

# 페이지 설정
st.set_page_config(page_title="더쿠 크롤러", page_icon="🔍")
st.title("더쿠(theqoo) 크롤러")
st.markdown("theqoo.net에서 특정 키워드가 포함된 게시물을 검색합니다.")

# 사이드바 설정
with st.sidebar:
    st.header("검색 설정")
    pages_to_crawl = st.slider("크롤링할 페이지 수", min_value=1, max_value=10, value=5)
    
    # 키워드 입력
    default_keywords = "유심, SKT"
    keywords_input = st.text_input("검색 키워드 (쉼표로 구분)", value=default_keywords)
    keywords = [k.strip() for k in keywords_input.split(",")]
    
    # 추가 설정
    show_links = st.checkbox("링크 표시", value=True)

# 크롤링 기능 정의
def crawl_theqoo(pages_to_crawl, keywords):
    filtered_posts = []
    
    # 진행상황 표시
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 크롬 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        status_text.text("브라우저를 초기화하는 중...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # 설정
        base_url = 'https://theqoo.net/hot?page='
        
        for page_idx, page in enumerate(range(1, pages_to_crawl + 1)):
            status_text.text(f"페이지 {page}/{pages_to_crawl} 크롤링 중...")
            progress_bar.progress((page_idx) / pages_to_crawl)
            
            url = base_url + str(page)
            driver.get(url)
            time.sleep(2)  # 페이지 로딩 대기
            
            posts = driver.find_elements(By.CSS_SELECTOR, 'td.title a')
            
            for post in posts:
                title = post.text.strip()
                link = post.get_attribute('href')
                
                if any(keyword in title for keyword in keywords):
                    filtered_posts.append({'title': title, 'link': link})
            
            time.sleep(1)  # 서버 부담 줄이기
        
        # 브라우저 종료
        driver.quit()
        progress_bar.progress(1.0)
        status_text.text("크롤링 완료!")
        
        return filtered_posts
    
    except Exception as e:
        st.error(f"크롤링 중 오류가 발생했습니다: {str(e)}")
        return []

# CSV 다운로드 기능
def get_csv_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="theqoo_results.csv">CSV 파일 다운로드</a>'
    return href

# 메인 로직
if st.button("크롤링 시작"):
    st.subheader("크롤링 상태")
    
    # 크롤링 실행
    filtered_posts = crawl_theqoo(pages_to_crawl, keywords)
    
    # 결과 표시
    if filtered_posts:
        st.subheader(f"검색 결과 ({len(filtered_posts)}개)")
        
        # 데이터프레임 생성
        df = pd.DataFrame(filtered_posts)
        
        # 결과 테이블 표시
        if show_links:
            # 링크를 클릭할 수 있게 만들기
            df_display = df.copy()
            df_display['link'] = df_display['link'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
            st.write(df_display.to_html(escape=False), unsafe_allow_html=True)
        else:
            st.dataframe(df)
        
        # CSV 다운로드 링크 제공
        st.markdown(get_csv_download_link(df), unsafe_allow_html=True)
    else:
        st.warning("검색 결과가 없습니다. 다른 키워드로 시도해보세요.")

# 주의사항
st.markdown("---")
st.caption("주의: 웹 크롤링은 대상 웹사이트의 이용약관을 준수해야 합니다. 개인적인 용도로만 사용하세요.") 
