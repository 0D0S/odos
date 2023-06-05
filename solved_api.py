import requests
import csv
import os
import datetime
from intra import ic
from slack_bot import SlackAPI

# 직접 실행하는 경우, os.getcwd()로 실행하면 되지만
# crontab으로 실행하는 경우 getcwd로 가져오는 경로가 다른 것으로 보임
# 그래서 우선 절대 경로를 직접 넣는 것으로 수정
# PATH = os.getcwd() + "/solved.csv"
PATH = "/home/ubuntu/odos/solved.csv"  # 파일의 절대 경로
TODAY = (datetime.datetime.now() - datetime.timedelta(hours=6)).strftime(
    "%Y-%m-%d"
)  # 현재 날짜 (새벽 6시부터 시작하도록)
URL = "https://solved.ac/api/v3/user/show"  # solved.ac 홈페이지 주소
HEADERS = {"Content-Type": "application/json"}
USERS = {
    "unsolved": [],
    "solved": [],
    "new_user": [],
    "none_user": [],
}  # 결과 출력할 때, 사용할 정보들을 담고 있는 사전
TIER = [
    "🖤 newbie",
    "🤎 V",
    "🤎 IV",
    "🤎 III",
    "🤎 II",
    "🤎 I",
    "🤍 V",
    "🤍 IV",
    "🤍 III",
    "🤍 II",
    "🤍 I",
    "💛 V",
    "💛 IV",
    "💛 III",
    "💛 II",
    "💛 I",
    "💙 V",
    "💙 IV",
    "💙 III",
    "💙 II",
    "💙 I",
    "💎 V",
    "💎 IV",
    "💎 III",
    "💎 II",
    "💎 I",
    "💖 V",
    "💖 IV",
    "💖 III",
    "💖 II",
    "💖 I",
]


def atoi(num: str) -> int:
    """
    문제 푼 자릿수가 다 다르기에 넉넉하게 받고 숫자만 반환
    Args:
        num: 푼 문제의 수로 시작하는 문자열

    Returns:
        ans: 푼 문제의 수

    """
    ans = 0
    for n in num:
        if not n.isdigit():
            break
        ans = ans * 10 + int(n)
    return ans


def total_solve(user: str) -> list:
    """
    solved.ac api로 접근하여 푼 문제의 수를 가져오는 함수
    Args:
        user: 백준 아이디

    Returns:
        0 or 양수: 푼 문제의 수
        -1: 잘못된 아이디일 경우

    """
    querystring = {"handle": user}
    response = requests.request("GET", URL, headers=HEADERS, params=querystring)
    info = [float("inf"), float("inf")]
    if response.text == "Not Found":
        return info
    for r in response.text.split(",")[::-1]:
        values = r.split(":")
        if values[0][1:-1] == "solvedCount":
            info[0] = min(atoi(values[1]), info[0])
        elif values[0][1:-1] == "tier":
            info[1] = atoi(values[1])
    return info


def csv_read() -> list:
    """
    기존 csv의 내용을 읽고 갱신하는 함수

    Returns:
        tmp_lst: 새로 갱신할 내용을 저장한 리스트

    """
    tmp_lst = []
    with open(PATH, "r", encoding="utf-8") as f:
        rd = csv.reader(f)
        if not rd:  # 정보가 없으면 아무것도 안씀
            return []
        for name, intra_id, baek_id, solve, update, flag, tier, continuity in rd:
            tmp = total_solve(baek_id)  # solved에 정보를 요청해서 최신화
            if tmp[0] == float("inf") and tmp[1] == float("inf"):  # solved에 없는 유저 처리
                tmp_lst.append([name, intra_id, baek_id, 0, TODAY, flag, 0, 1])
                USERS["none_user"].append([name, intra_id])
                continue

            if update == TODAY and flag == "0":  # 오늘 이미 푼 것을 확인한 유저
                tmp_lst.append(
                    [name, intra_id, baek_id, tmp[0], TODAY, flag, tmp[1], continuity]
                )
                USERS["solved"].append([name, intra_id, int(tmp[1]), continuity])
                continue

            if str(tmp[0]) <= solve:  # 오늘 안 푼 유저
                if int(flag) > 1:  # 2일 이상 안 풀면 연속 기록이 깨짐
                    continuity = "0"
                if update == TODAY:  # 오늘 이미 확인한 유저
                    tmp_lst.append(
                        [
                            name,
                            intra_id,
                            baek_id,
                            tmp[0],
                            TODAY,
                            int(flag),
                            tmp[1],
                            continuity,
                        ]
                    )
                    USERS["unsolved"].append((name, intra_id, int(flag), int(tmp[1])))
                else:  # 오늘 확인하지 않은 유저 -> 안 푼 날짜를 하루 늘림
                    tmp_lst.append(
                        [
                            name,
                            intra_id,
                            baek_id,
                            tmp[0],
                            TODAY,
                            int(flag) + 1,
                            tmp[1],
                            continuity,
                        ]
                    )
                    USERS["unsolved"].append(
                        (name, intra_id, int(flag) + 1, int(tmp[1]))
                    )
            else:  # 오늘 푼 유저 -> 연속 날짜를 하루 늘리고 안 푼 날짜를 0으로 초기화
                tmp_lst.append(
                    [
                        name,
                        intra_id,
                        baek_id,
                        tmp[0],
                        TODAY,
                        0,
                        int(tmp[1]),
                        str(int(continuity) + 1),
                    ]
                )
                USERS["solved"].append(
                    [name, intra_id, int(tmp[1]), str(int(continuity) + 1)]
                )
    return tmp_lst


def csv_write(tmp_lst: list, option: str):
    """
    csv 파일에 갱신한 데이터를 작성하는 함수
    Args:
        tmp_lst: 갱신된 데이터를 저장한 리스트
        option:
            a: 이어쓰기
            w: 기존 내용은 지우고 새로 쓰기

    """
    with open(PATH, option, newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerows(tmp_lst)


def get_location(intra_id: str) -> tuple:
    """
    위치와 출퇴근을 조사하는 함수
    Args:
        intra_id: 인트라 아이디

    Returns:
        위치와 출퇴근 여부를 반환
    """
    response = ic.get("users", params={"filter[login]": intra_id})  # 42api에서 정보 받기
    loc = response.json()[0]["location"]  # 현재 위치
    date, time = response.json()[0]["updated_at"].split("T")  # 마지막으로 맥에 로그인 한 시간(UTC)
    date = list(map(int, date.split("-")))
    time = list(map(int, time[:-5].split(":")))
    last_time = datetime.datetime(date[0], date[1], date[2], time[0], time[1], 0)
    last_time += datetime.timedelta(hours=9)  # 마지막으로 맥에 로그인 한 시간(한국시간)
    now_day = datetime.datetime.now() - datetime.timedelta(
        hours=6
    )  # 익일 새벽 6시를 하루의 끝으로 두고 구한 날짜 -> 6월 5일 0시 0분 0초
    now_day = datetime.datetime(now_day.year, now_day.month, now_day.day, 6, 0, 0, 0)
    cluster = 1 if last_time >= now_day else 0  # 마지막 맥 로그인 시간이 오늘이면 1, 아니면 0
    return (loc, cluster) if loc else ("null", cluster)


def print_name():
    """
    푼 사람, 안 푼 사람, 새로운 사람을 정리해서 출력하는 함수

    """
    text = ""
    text += f"⏰현재 시각: {datetime.datetime.now()}\n\n"  # 현재 시각
    if USERS["solved"]:
        text += "😀푼 사람😀\n"
    no_cluster = []
    for name, intra_id, tier, continuity in USERS["solved"]:
        loc, cluster = get_location(intra_id)  # 42api에서 정보 받아오기
        if loc == "null":  # 지금 클러스터에 없는 사람
            if cluster:  # 출근을 했던 사람
                no_cluster.append(
                    f"- {intra_id} ({name}) {TIER[tier]} \n({continuity}일 연속으로 푸는 중, 퇴근함)"
                )
            else:  # 출근도 안 한 사람
                no_cluster.append(
                    f"- {intra_id} ({name}) {TIER[tier]} \n({continuity}일 연속으로 푸는 중, 출근 안 함)"
                )
        else:  # 현재 클러스터에 있는 사람
            text += f"- {intra_id} ({name}) {TIER[tier]} \n({continuity}일 연속으로 푸는 중, 현재 위치: {loc})\n"
    for s in no_cluster:
        text += s + "\n"

    if USERS["unsolved"]:
        text += "\n😢안 푼 사람😢\n"
    no_cluster = []
    for name, intra_id, day, tier in USERS["unsolved"]:
        loc, cluster = get_location(intra_id)  # 42 api 정보 가져오기
        if loc == "null":  # 현재 클러스터에 없는 사람
            if cluster:  # 출근은 한 사람
                if day > 99:  # 100일 넘어가면
                    text += f"- {intra_id} ({name}) {TIER[tier]} \n({day}일 째... 집에서라도 풀어요, 퇴근함)\n"
                else:  # 100일 미만이면
                    text += (
                        f"- {intra_id} ({name}) {TIER[tier]} \n({day}일 째 안 푸는 중, 퇴근함)\n"
                    )
            else:  # 출근도 안 한 사람
                if day > 99:
                    no_cluster.append(
                        f"- {intra_id} ({name}) {TIER[tier]} \n({day}일 째... 살아있나요)"
                    )
                else:
                    no_cluster.append(
                        f"- {intra_id} ({name}) {TIER[tier]} \n({day}일 째 안 푸는 중, 출근 안 함)"
                    )
        else:  # 현재 클러스터에 있는 사람
            if day > 99:
                text += f"- {intra_id} ({name}) {TIER[tier]} \n({day}일 째... 과제쉴 때 게임하지 말고 백준 풀어요, 현재 위치: {loc})\n"
            else:
                text += f"- {intra_id} ({name}) {TIER[tier]} \n({day}일 째 안 푸는 중, 현재 위치: {loc})\n"
    if no_cluster:  # 출근도 안 하고 백준도 안 풀고
        text += "\n🙏백준도 안 풀고, 클러스터에도 없고🙏\n"
    for s in no_cluster:
        text += s + "\n"

    if USERS["none_user"]:  # solved에 없는 사람
        text += "\n🙏백준 아이디 알려주시고 solved.ac 동의 해주세요🙏\n"
    for name, intra_id in USERS["none_user"]:
        loc, cluster = get_location(intra_id)
        if loc == "null" and cluster == 0:
            if cluster:
                text += f"- {intra_id} ({name})\n(퇴근함)\n"
            else:
                text += f"- {intra_id} ({name})\n(출근 안 함)\n"
        else:
            text += f"- {intra_id} ({name})\n(현재 위치: {loc})\n"
    text += "\n주의 사항: 출근은 새벽 6시 ~ 익일 새벽 5시 55분 사이 맥 로그인 기록으로 판단합니다.\n"
    return text


if __name__ == "__main__":
    lst = csv_read()  # csv 파일 정보를 가져옴
    csv_write(lst, "w")  # csv 파일 최신화
    message = print_name()  # 현재 위치, 결과 출력
    print(message)
    base_dir = os.path.dirname(os.path.realpath(__file__))
    with open(base_dir + "/token.txt", "r") as token:
        SLACK_TOKEN = token.readline()
    if 7 < datetime.datetime.now().hour:
        slack = SlackAPI(SLACK_TOKEN)
        slack.post_chat_message("독촉", message)
