import streamlit as st
import requests
from bs4 import BeautifulSoup

def crawl_theqoo(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 에러가 있으면 예외 발생
        soup = BeautifulSoup(response.text, "html.parser")
        
        titles = []
        for post in soup.select('.title'):
            title_text = post.get_text(strip=True)
            if title_text:
                titles.append(title_text)
        return titles

    except Exception as e:
        st.error(f"크롤링 중 오류 발생: {e}")
        return []

def main():
    st.title("더쿠 핫이슈 크롤러")

    url = st.text_input("크롤링할 더쿠 게시판 URL 입력", "https://theqoo.net/hot")

    if st.button("크롤링 시작"):
        with st.spinner("크롤링 중입니다..."):
            titles = crawl_theqoo(url)

        if titles:
            st.success(f"총 {len(titles)}개의 글을 가져왔습니다.")
            for idx, title in enumerate(titles, start=1):
                st.write(f"{idx}. {title}")
        else:
            st.warning("글을 가져오지 못했습니다.")

if __name__ == "__main__":
    main()

