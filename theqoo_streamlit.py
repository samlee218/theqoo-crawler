import streamlit as st
import requests
from bs4 import BeautifulSoup

def crawl_theqoo(base_url, last_page):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    collected_titles = []

    keywords = ['skt', '유심', 'usim']  # 키워드 리스트 (소문자 기준)

    try:
        for page in range(1, last_page + 1):
            url = f"{base_url}?page={page}"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for post in soup.select('.title'):
                title_text = post.get_text(strip=True)
                if title_text:
                    title_lower = title_text.lower()
                    if any(keyword in title_lower for keyword in keywords):
                        collected_titles.append((page, title_text))

    except Exception as e:
        st.error(f"크롤링 중 오류 발생: {e}")

    return collected_titles

def main():
    st.title("더쿠 SKT/유심 키워드 전용 크롤러")

    base_url = st.text_input("더쿠 게시판 기본 URL 입력", "https://theqoo.net/hot")
    last_page = st.number_input("마지막 페이지 번호 입력", min_value=1, value=5, step=1)

    if st.button("크롤링 시작"):
        with st.spinner("크롤링 중입니다..."):
            titles = crawl_theqoo(base_url, last_page)

        if titles:
            st.success(f"총 {len(titles)}개 글 찾음 (SKT/유심 관련)")
            for idx, (page, title) in enumerate(titles, start=1):
                st.write(f"{idx}. [p{page}] {title}")
        else:
            st.warning("SKT 또는 유심 관련 글을 찾지 못했습니다.")

if __name__ == "__main__":
    main()
