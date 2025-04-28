import streamlit as st
import requests
from bs4 import BeautifulSoup

def crawl_theqoo(base_url, last_page, keyword):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    collected_titles = []
    
    try:
        for page in range(1, last_page + 1):
            url = f"{base_url}?page={page}"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for post in soup.select('.title'):
                title_text = post.get_text(strip=True)
                if title_text and keyword.lower() in title_text.lower():
                    collected_titles.append((page, title_text))

    except Exception as e:
        st.error(f"크롤링 중 오류 발생: {e}")

    return collected_titles

def main():
    st.title("더쿠 키워드 크롤러 (1페이지부터 마지막 페이지까지)")

    base_url = st.text_input("더쿠 게시판 기본 URL 입력", "https://theqoo.net/hot")
    last_page = st.number_input("마지막 페이지 번호 입력", min_value=1, value=5, step=1)
    keyword = st.text_input("검색할 키워드 입력", "")

    if st.button("크롤링 시작"):
        if not keyword:
            st.warning("키워드를 입력해 주세요!")
        else:
            with st.spinner("크롤링 중입니다..."):
                titles = crawl_theqoo(base_url, last_page, keyword)

            if titles:
                st.success(f"'{keyword}' 키워드가 포함된 글 {len(titles)}개 찾음!")
                for idx, (page, title) in enumerate(titles, start=1):
                    st.write(f"{idx}. [p{page}] {title}")
            else:
                st.warning(f"'{keyword}' 키워드가 포함된 글을 찾지 못했습니다.")

if __name__ == "__main__":
    main()
