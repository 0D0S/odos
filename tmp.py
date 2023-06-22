import requests
from intra import ic


def intra_api(user: str) -> None:
    """
    42api를 통해 유저 정보를 출력하는 함수
    Args:
        user: intra id
    """
    response = ic.get("users", params={"filter[login]": user})
    try:
        loc = response.json()
        print(loc)
    except:
        print(response)


def solved_api(user: str) -> None:
    """
    solved api를 통해 유저 정보를 출력하는 함수
    Args:
        user: baekjoon id
    """
    url = "https://solved.ac/api/v3/user/show"
    querystring = {"handle": user}
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers, params=querystring)
    print(response)
    print(response.json())


if __name__ == "__main__":
    intra_api("myko")
    solved_api("kmj951015")
