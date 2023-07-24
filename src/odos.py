import os
import csv
import datetime
import time
from tqdm import tqdm
from typing import List, Dict
from SlackAPI import SlackAPI  # type: ignore
from Student import Student  # type: ignore
from SolvedCrowling import SolvedCrawler


TOTAL = 26  # 전체 인원
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
CSV_PATH = PARENT_DIR + "/doc/solved.csv"
SLACK_TOKEN_PATH = PARENT_DIR + "/doc/slack_token.txt"
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
        context = solved_crawler(rd)
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerows(context)


def solved_crawler(rd) -> List[List]:
    context = []
    cral = SolvedCrawler()
    for name, intra_id, baek_id, day, flag in tqdm(
        rd, desc="진행도", total=TOTAL, ncols=70, ascii=" =", leave=True
    ):
        time.sleep(0.1)
        data = cral.get_info(baek_id)
        if type(data) == int:
            context.append([name, intra_id, baek_id, "0", "0"])
            USERS["none_user"].append(
                Student(name, intra_id, baek_id, TIER["Unrated 9"], 0)
            )
        elif data[1] == 0:  # type: ignore
            i_day = int(day)
            if flag == "0":
                i_day = -1 if i_day > 0 else i_day - 1
            context.append([name, intra_id, baek_id, str(i_day), "1"])
            USERS["unsolved"].append(Student(name, intra_id, baek_id, TIER[data[0]], i_day))  # type: ignore
        elif data[1] == int(day) and flag == "0":  # type: ignore
            context.append([name, intra_id, baek_id, day, "0"])
            USERS["unsolved"].append(Student(name, intra_id, baek_id, TIER[data[0]], 0))  # type: ignore
        elif data[1] > 0:  # type: ignore
            context.append([name, intra_id, baek_id, str(data[1]), "1"])  # type: ignore
            USERS["solved"].append(Student(name, intra_id, baek_id, TIER[data[0]], data[1]))  # type: ignore
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
