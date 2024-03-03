import csv
import datetime
import os
import time
from typing import List, Dict

from tqdm import tqdm

from Crawler import Crawler
from SlackAPI import SlackAPI  # type: ignore
from Student import Student  # type: ignore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
CSV_PATH = PARENT_DIR + "/doc/solved.csv"

SLACK_TOKEN_PATH = PARENT_DIR + "/doc/slack_token.txt"
TODAY = (datetime.datetime.now() - datetime.timedelta(hours=6)).strftime("%Y-%m-%d")
USERS: Dict[str, List] = {"solved": [], "unsolved": [], "none_user": []}
TIER: List = [
    ":unranked:",
    ":bronze5:",
    ":bronze4:",
    ":bronze3:",
    ":bronze2:",
    ":bronze1:",
    ":silver5:",
    ":silver4:",
    ":silver3:",
    ":silver2:",
    ":silver1:",
    ":gold5:",
    ":gold4:",
    ":gold3:",
    ":gold2:",
    ":gold1:",
    ":platinum5:",
    ":platinum4:",
    ":platinum3:",
    ":platinum2:",
    ":platinum1:",
    ":diamond5:",
    ":diamond4:",
    ":diamond3:",
    ":diamond2:",
    ":diamond1:",
    ":ruby5:",
    ":ruby4:",
    ":ruby3:",
    ":ruby2:",
    ":ruby1:",
]


def read_and_write_csv(is_last_check: bool) -> None:
    """
    csv 파일을 읽어서 처리 후, csv 파일을 최신화 하는 함수
    Args:
        is_last_check: 그 날의 마지막 검사인지 판별하는 flag
    """
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rd = csv.reader(f)
        if not rd:
            return
        context = solved_and_blackhole_crawler(list(rd), is_last_check)
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerows(context)


def solved_and_blackhole_crawler(rd: list, is_last_check: bool) -> List[List]:
    """
    solved.ac와 42intra에서 필요한 정보를 얻어서 저장하고 csv파일에 저장할 데이터를 반환하는 함수
    Args:
        rd: csv파일 내용이 들어있는 리스트
        is_last_check: 그 날의 마지막 검사인지 판별하는 flag

    Returns:
        얻어온 정보를 사람 별로 저장한 리스트
    """
    context = []

    with open(PARENT_DIR + "/doc/42intra.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    name = lines[0].strip()
    pwd = lines[1].strip()

    cral = Crawler(name, pwd)
    for name, intra_id, baek_id, day, count, flag, date in tqdm(
        rd, desc="진행도", total=len(rd), ncols=70, ascii=" =", leave=True
    ):
        time.sleep(0.1)
        # blackhole = cral.get_blackhole(intra_id)
        blackhole = "현재 블랙홀 기간은 가져오지 않습니다."
        data = cral.get_info(baek_id)
        if type(data) is int:  # solved.ac id가 없는 사람
            context.append([name, intra_id, baek_id, "0", "0", "0", TODAY])
            # USERS["none_user"].append(
            #     Student(name, intra_id, baek_id, TIER[0], 0, blackhole)
            # )
            USERS["none_user"].append(
                Student(name, intra_id, baek_id, TIER[0], 0, blackhole)
            )
            continue

        rank, solved_count = data
        if date == TODAY and flag == "1":  # 이미 오늘 푼 사람
            context.append([name, intra_id, baek_id, day, solved_count, flag, TODAY])
            USERS["solved"].append(
                Student(name, intra_id, baek_id, TIER[rank], day, blackhole)
            )
        elif int(count) >= solved_count:  # 안 푼 사람
            i_day = int(day)
            if is_last_check:  # 그 날의 마지막 검사일 때 최신화
                i_day = 0 if int(day) > 0 else int(day) - 1
            context.append([name, intra_id, baek_id, i_day, solved_count, "0", TODAY])
            USERS["unsolved"].append(Student(name, intra_id, baek_id, TIER[rank], i_day, blackhole))  # type: ignore
        elif int(count) < solved_count:  # 오늘 푼 사람
            i_day = int(day) + 1 if int(day) > 0 else 1
            context.append([name, intra_id, baek_id, i_day, solved_count, "1", TODAY])
            USERS["solved"].append(
                Student(name, intra_id, baek_id, TIER[rank], i_day, blackhole)
            )
    return context


def print_result() -> str:
    """
    정리한 정보를 일정 형태로 가공하여 반환하는 함수
    Returns:
        일정 형태로 가공한 문자열
    """
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
                        f"{student.get_name()} {student.get_rank()} ( solve: {student.get_day()}일  |  블랙홀: {student.get_blackhole()}일  |  퇴근함 or 노트북)\n"
                    )
                else:
                    pos[key]["home"].append(
                        f"{student.get_name()} {student.get_rank()} ( solve: {student.get_day()}일  |  블랙홀: {student.get_blackhole()}일  |  출근 안 함 or 노트북 )\n"
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
    text += "\n:재권_공지: 하루 시작은 백준과 동일하게 6시입니다. 5시 55분 ~ 6시 사이에 푼 문제는 반영되지 않을 수 있습니다. :재권_공지:\n"
    print(text)
    return text


def chat_message(channel: str, message: str) -> None:
    """
    슬랙 채널에 주어진 메세지를 출력하는 함수
    Args:
        channel: 메세지를 출력할 슬랙 채널명
        message: 출력할 메세지
    """
    with open(SLACK_TOKEN_PATH, "r") as token:
        slack_token = token.readline()
    slack_api = SlackAPI(slack_token)
    slack_api.post_chat_message(channel, message)
