import requests
from bs4 import BeautifulSoup
from typing import Tuple


class SolvedCrawler:
    def __init__(self):
        self._url = "https://solved.ac/profile/"

    def get_info(self, baek_id: str) -> Tuple[str, int] | int:
        """
        백준 유저의 rank와 연속 문제 풀이 일 수를 가져오는 함수
        Returns:
             tuple: rank와 day가 들어있음
             int: 에러 코드가 들어있음
        """
        response = requests.get(self._url + baek_id)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            data = soup.find_all("div", {"class": "css-1midmz7"})
            rank = data[0].find("span").get_text()
            day = data[1].find("b").get_text()
            return rank, int(day)
        else:
            return response.status_code
