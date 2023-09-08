import requests
import datetime
from intra import ic


def intra_api(user: str) -> None:
    """
    42api를 통해 유저 정보를 출력하는 함수
    Args:
        user: intra id
    """
    response = ic.get("users", params={"filter[login]": user})
    loc = response.json()
    try:
        print(loc)
    except requests.exceptions.JSONDecodeError:
        print(response)


def solved_api() -> None:
    """
    solved api를 통해 유저 정보를 출력하는 함수
    Args:
        user: baekjoon id
    """
    url = "https://api.evaluation.42seoul.link/user/yejinam"
    response = requests.get(url)
    date = response.json()["blackhole"].split("T")[0]
    date = list(map(int, date.split("-")))
    blackhole = datetime.date(date[0], date[1], date[2])
    left = blackhole - datetime.date.today()
    print(left.days)


if __name__ == "__main__":
    intra_api(input("42seoul ID: "))
    # print()
    solved_api()
