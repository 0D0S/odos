import os
import csv
import datetime
from typing import List, Dict
from SlackAPI import SlackAPI  # type: ignore
from Student import Student  # type: ignore


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
CSV_PATH = PARENT_DIR + "/doc/solved.csv"
SLACK_TOKEN_PATH = PARENT_DIR + "/doc/slack_token.txt"
USERS: List = []


def csv_read() -> None:
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rd = csv.reader(f)
        if not rd:
            return
        for name, intra_id, baek_id in rd:
            USERS.append(Student(name, intra_id, baek_id))


def print_loc() -> str:
    text = f":수빈: 현재 시각: {datetime.datetime.now()} :수빈:\n\n"  # 현재 시각
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
