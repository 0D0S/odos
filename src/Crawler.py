import datetime
from typing import Tuple

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import odos


class Crawler:
    def __init__(self, name: str, pwd: str):
        """
        api 요청 및 웹 크롤링을 위한 객체
        Args:
            name: 42intra id
            pwd:  42intra pwd
        """
        self.solved_url = "https://solved.ac/api/v3/user/show"
        self.blackhole_xpath = "/html/body/div[4]/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/div[2]/div"
        self.grade_xpath = "/html/body/div[4]/div[2]/div/div[2]/div/div[1]/div[2]/div/div[1]/div[5]/span[2]"

        self.service = Service(odos.PARENT_DIR + "/chromedriver")
        self.option = Options()
        self.option.add_argument("--headless")
        self.driver = webdriver.Chrome(service=self.service, options=self.option)
        self.driver.get("https://profile.intra.42.fr")
        self.driver.find_element(By.ID, "username").send_keys(name)
        self.driver.find_element(By.ID, "password").send_keys(pwd)
        self.driver.find_element(By.ID, "kc-login").click()
        self.wait = WebDriverWait(self.driver, 10)

    def __del__(self):
        """
        Crawler 객체가 소멸할 때, driver을 꺼준다.
        """
        self.driver.quit()

    def get_blackhole(self, intra_id: str) -> str:
        """
        blackhole을 반환하는 함수
        Args:
            intra_id

        Returns:
            카뎃: blackhole 기간
            멤버: 빈 문자열
        """
        self.driver.get(f"https://profile.intra.42.fr/users/{intra_id}")
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.blackhole_xpath))
        )  # 로딩까지 기다림
        blackhole = self.driver.find_element(By.XPATH, self.blackhole_xpath).text
        grade = self.driver.find_element(By.XPATH, self.grade_xpath).text
        try:
            blackhole = datetime.datetime.strptime(blackhole, "%Y. %m. %d.")
            blackhole = blackhole - datetime.datetime.now()
            blackhole = str(blackhole.days + 1)
        except ValueError:
            blackhole = "∞" if grade == "Member" else "???"

        return blackhole

    def get_info(self, baek_id: str) -> Tuple[int, int] | int:
        """
        백준 유저의 rank와 연속 문제 풀이 일 수를 가져 오는 함수
        Returns:
            tuple: 랭크와 총 푼 문제 수가 들어 있음
            int: 에러 코드가 들어 있음
        """
        querystring = {"handle": baek_id}
        headers = {"Accept": "application/json"}
        response = requests.get(self.solved_url, headers=headers, params=querystring)
        if response.status_code != 200:
            return response.status_code
        data = response.json()
        return data["tier"], data["solvedCount"]
