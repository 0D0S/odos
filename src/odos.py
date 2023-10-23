import csv
import datetime
import os
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from SlackAPI import SlackAPI  # type: ignore
from Student import Student  # type: ignore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
CSV_PATH = PARENT_DIR + "/doc/solved.csv"
SLACK_TOKEN_PATH = PARENT_DIR + "/doc/slack_token.txt"
GRADE_XPATH = (
    "/html/body/div[4]/div[2]/div/div[2]/div/div[1]/div[2]/div/div[1]/div[5]/span[2]"
)
BLACKHOLE_XPATH = "/html/body/div[4]/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/div[2]/div"
USERS: List = []


def csv_read() -> None:
    with open(PARENT_DIR + "/doc/42intra.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    name = lines[0].strip()
    pwd = lines[1].strip()

    service = Service(PARENT_DIR + "/chromedriver")
    option = Options()
    option.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=option)
    driver.get("https://profile.intra.42.fr/users")
    driver.find_element(By.ID, "username").send_keys(name)
    driver.find_element(By.ID, "password").send_keys(pwd)
    driver.find_element(By.ID, "kc-login").click()
    wait = WebDriverWait(driver, 10)

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rd = csv.reader(f)
        if not rd:
            return
        for name, intra_id, baek_id in rd:
            USERS.append(Student(name, intra_id, baek_id))
            driver.get(f"https://profile.intra.42.fr/users/{intra_id}")
            wait.until(
                ec.presence_of_element_located((by.xpath, blackhole_xpath))
            )  # 로딩까지 기다림
            blackhole = driver.find_element(by.xpath, blackhole_xpath).text
            grade = driver.find_element(By.XPATH, GRADE_XPATH).text
            if blackhole == "" and grade == "Learner":
                driver.get(f"https://profile.intra.42.fr/users/{intra_id}")
                wait.until(
                    ec.presence_of_element_located((by.xpath, blackhole_xpath))
                )  # 로딩까지 기다림
                blackhole = driver.find_element(by.xpath, blackhole_xpath).text
            try:
                blackhole = datetime.datetime.strptime(blackhole, "%Y. %m. %d.")
                blackhole = blackhole - datetime.datetime.now()
                USERS[-1].set_blackhole(str(blackhole.days + 1))
            except ValueError:
                if blackhole == "":
                    if grade == "Learner":
                        USERS[-1].set_blackhole("Not found")
                    elif grade == "Member":
                        USERS[-1].set_blackhole("∞")
                    elif grade == "Novice":
                        USERS[-1].set_blackhole("Piscine")
                else:
                    USERS[-1].set_blackhole(blackhole)
    driver.quit()


def print_loc() -> str:
    text = f":수빈: 현재 시각 {datetime.datetime.now()} :수빈:\n\n"  # 현재 시각
    pos: Dict[str, List[str]] = {"cluster": [], "home": [], "leave": []}
    for student in USERS:
        print(type(student.get_loc()), student.get_loc())
        if student.get_loc() == "null":
            if student.get_is_working():
                pos["leave"].append(
                    f"{student.get_name()} ( 블랙홀: {student.get_blackhole()}  |  퇴근함)\n"
                )
            else:
                pos["home"].append(
                    f"{student.get_name()} ( 블랙홀: {student.get_blackhole()}  |  출근 안함 )\n"
                )
        else:
            pos["cluster"].append(
                f"{student.get_name()} ( 블랙홀: {student.get_blackhole()}  |  {student.get_loc()} )\n"
            )
    if pos["cluster"]:
        text += "\n<아마 코딩 중>\n"
    for t in pos["cluster"]:
        text += t
    if pos["leave"]:
        text += "\n<퇴근 or 클러스터 어딘가>\n"
    for t in pos["leave"]:
        text += t
    if pos["home"]:
        text += "\n<출근 안함 or 노트북>\n"
    for t in pos["home"]:
        text += t
    text += (
        "\n:재권_공지: 백준 문제 풀이는 21시에 수동으로 한 번 올라옵니다. 블랙홀 기간은 조금의 차이가 있을 수 있습니다. :재권_공지:\n"
    )
    print(text)
    return text


def chat_message(channel: str, message: str) -> None:
    with open(SLACK_TOKEN_PATH, "r") as token:
        slack_token = token.readline()
    slack_api = SlackAPI(slack_token)
    slack_api.post_chat_message(channel, message)
