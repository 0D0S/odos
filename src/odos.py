import csv
import datetime
import os
import time
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from SlackAPI import SlackAPI  # type: ignore
from SolvedCrowling import SolvedCrawler
from Student import Student  # type: ignore

TOTAL = 26  # 전체 인원
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
CSV_PATH = PARENT_DIR + "/doc/solved.csv"
SLACK_TOKEN_PATH = PARENT_DIR + "/doc/slack_token.txt"
XPATH = "/html/body/div[4]/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/div[2]/div"
TODAY = (datetime.datetime.now() - datetime.timedelta(hours=6)).strftime("%Y-%m-%d")
USERS: Dict[str, List] = {"solved": [], "unsolved": [], "none_user": []}
TIER: Dict[str, str] = {
    "Unrated 9": ":unranked:",
    "Unrated": ":unranked:",
    "Bronze V": ":bronze5:",
    "Bronze IV": ":bronze4:",
    "Bronze III": ":bronze3:",
    "Bronze II": ":bronze2:",
    "Bronze I": ":bronze1:",
    "Silver V": ":silver5:",
    "Silver IV": ":silver4:",
    "Silver III": ":silver3:",
    "Silver II": ":silver2:",
    "Silver I": ":silver1:",
    "Gold V": ":gold5:",
    "Gold IV": ":gold4:",
    "Gold III": ":gold3:",
    "Gold II": ":gold2:",
    "Gold I": ":gold1:",
    "Platinum V": ":platinum5:",
    "Platinum IV": ":platinum4:",
    "Platinum III": ":platinum3:",
    "Platinum II": ":platinum2:",
    "Platinum I": ":platinum1:",
    "Diamond V": ":diamond5:",
    "Diamond IV": ":diamond4:",
    "Diamond III": ":diamond3:",
    "Diamond II": ":diamond2:",
    "Diamond I": ":diamond1:",
    "Ruby V": ":ruby5:",
    "Ruby IV": ":ruby4:",
    "Ruby III": ":ruby3:",
    "Ruby II": ":ruby2:",
    "Ruby I": ":ruby1:",
}


def read_and_write_csv() -> None:
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rd = csv.reader(f)
        if not rd:
            return
        context = solved_and_blackhole_crawler(rd)
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerows(context)


def solved_and_blackhole_crawler(rd) -> List[List]:
    context = []
    cral = SolvedCrawler()

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

    for name, intra_id, baek_id, day, flag, date in tqdm(
        rd, desc="진행도", total=TOTAL, ncols=70, ascii=" =", leave=True
    ):
        time.sleep(0.1)

        driver.get(f"https://profile.intra.42.fr/users/{intra_id}")
        wait.until(EC.presence_of_element_located((By.XPATH, XPATH)))  # 로딩까지 기다림
        blackhole = driver.find_element(By.XPATH, XPATH).text
        try:
            blackhole = datetime.datetime.strptime(blackhole, "%Y. %m. %d.")
            blackhole = blackhole - datetime.datetime.now()
            blackhole = str(blackhole.days + 1)
        except ValueError:
            pass

        data = cral.get_info(baek_id)
        if type(data) == int:  # solved.ac id가 없는 사람
            context.append([name, intra_id, baek_id, "0", "0", TODAY])
            USERS["none_user"].append(
                Student(name, intra_id, baek_id, TIER["Unrated 9"], 0, blackhole)
            )
        elif date == TODAY and flag == "1":  # 이미 오늘 푼 사람
            context.append([name, intra_id, baek_id, str(data[1]), "1", TODAY])
            USERS["solved"].append(
                Student(name, intra_id, baek_id, TIER[data[0]], data[1], blackhole)
            )
        elif data[1] == 0:  # 연속으로 푼 문제가 없는 사람
            i_day = int(day)
            if date != TODAY:
                i_day = -1 if i_day > 0 else i_day - 1
            context.append([name, intra_id, baek_id, str(i_day), "0", TODAY])
            USERS["unsolved"].append(Student(name, intra_id, baek_id, TIER[data[0]], i_day, blackhole))  # type: ignore
        elif data[1] == int(day) and flag == "0":  # 연속으로 푼 문제가 어제와 동일한 사람
            context.append([name, intra_id, baek_id, day, "0", TODAY])
            USERS["unsolved"].append(
                Student(name, intra_id, baek_id, TIER[data[0]], i_day, blackhole)
            )
        elif data[1] > int(day):  # 연속으로 푼 문제가 늘어난 사람
            context.append([name, intra_id, baek_id, str(data[1]), "1", TODAY])
            USERS["solved"].append(
                Student(name, intra_id, baek_id, TIER[data[0]], data[1], blackhole)
            )
    driver.quit()
    return context


def print_result() -> str:
    text = f"\n\n:수빈: 현재 시각: {datetime.datetime.now()} :수빈:\n\n"  # 현재 시각
    pos: Dict[str, Dict[str, List[str]]] = {
        "solved": {"cluster": [], "home": [], "leave": []},
        "unsolved": {"cluster": [], "home": [], "leave": []},
        "none_user": {"cluster": [], "home": [], "leave": []},
    }
    for key, value in USERS.items():
        for student in value:
            if student.get_loc() == "null":
                if student.get_is_working():
                    pos[key]["leave"].append(
                        f"{student.get_name()} {student.get_rank()} ( solve: {student.get_day()}일  |  블랙홀: {student.get_blackhole()}일  |  퇴근함 )\n"
                    )
                else:
                    pos[key]["home"].append(
                        f"{student.get_name()} {student.get_rank()} ( solve: {student.get_day()}일  |  블랙홀: {student.get_blackhole()}일  |  출근 안 함 )\n"
                    )
            else:
                pos[key]["cluster"].append(
                    f"{student.get_name()} {student.get_rank()} ( solve: {student.get_day()}일  |  블랙홀: {student.get_blackhole()}일  |  {student.get_loc()} )\n"
                )
    if (
        len(pos["solved"]["cluster"])
        + len(pos["solved"]["home"])
        + len(pos["solved"]["leave"])
    ):
        text += "\n<푼 사람>\n"
        for v in pos["solved"].values():
            for t in v:
                text += t
            if v:
                text += "\n"
    if (
        len(pos["unsolved"]["cluster"])
        + len(pos["unsolved"]["home"])
        + len(pos["unsolved"]["leave"])
    ):
        text += "\n<안 푼 사람>\n"
        for v in pos["unsolved"].values():
            for t in v:
                text += t
            if v:
                text += "\n"
    if (
        len(pos["none_user"]["cluster"])
        + len(pos["none_user"]["home"])
        + len(pos["none_user"]["leave"])
    ):
        text += "\n<백준 아이디 알려 주고, solved.ac 동의 해주세요>\n"
        for v in pos["none_user"].values():
            for t in v:
                text += t
            if v:
                text += "\n"
    text += "\n:재권_공지: 하루 시작은 새벽 6시입니다. 백준 결과는 매일 21시에 제가 수동으로 올립니다. :재권_공지:\n"
    print(text)
    return text


def chat_message(channel: str, message: str) -> None:
    with open(SLACK_TOKEN_PATH, "r") as token:
        slack_token = token.readline()
    slack_api = SlackAPI(slack_token)
    slack_api.post_chat_message(channel, message)
