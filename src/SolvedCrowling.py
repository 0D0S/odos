from typing import Tuple

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from odos import PARENT_DIR


class SolvedCrawler:
    def __init__(self):
        self._url = "https://solved.ac/profile/"
        self._rank_xpath = "/html/body/div[1]/div[2]/div[2]/div[4]/span[2]/b"
        self._day_xpath = (
            "/html/body/div[1]/div[3]/div/div[4]/div[1]/div[2]/div[1]/div/div/b"
        )

    def get_info(self, baek_id: str) -> Tuple[str, int] | int:
        """
        백준 유저의 rank와 연속 문제 풀이 일 수를 가져 오는 함수
        Returns:
             tuple: rank와 day가 들어 있음
             int: 에러 코드가 들어 있음
        """
        webdriver_service = Service(PARENT_DIR + "/chromedriver")
        options = Options()
        options.add_argument("--headless")  # 브라우저 창 숨기기

        driver = webdriver.Chrome(service=webdriver_service, options=options)
        driver.get(self._url + baek_id)

        try:
            wait = WebDriverWait(driver, 10)
            wait.until(
                EC.presence_of_element_located((By.XPATH, self._rank_xpath))
            )  # 로딩까지 기다림
            day = driver.find_element(By.XPATH, self._day_xpath).text
            rank = driver.find_element(By.XPATH, self._rank_xpath).text
            return rank, int(day)
        except:
            return -1
