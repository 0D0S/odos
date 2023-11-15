import datetime
from typing import Tuple

from Intra import ic  # type: ignore


class Student:  # type: ignore
    def __init__(
        self,
        name: str,
        intra_id: str,
        baek_id: str,
        rank: str,
        day: int,
        blackhole: str,
    ) -> None:
        self._name: str = name  # 별명이 포함된 이름
        self._intra_id: str = intra_id  # 42seoul 인트라 아이디
        self._baek_id: str = baek_id  # 백준 아이디
        self._loc, self._is_working = self._get_location()  # 클러스터 위치, 출퇴근 여부
        self._blackhole: str = blackhole  # 남은 블랙홀 기간
        self._rank: str = rank  # 백준 랭크
        self._day: int = day  # 연속으로 문제 푼 일 수

    def _get_location(self) -> Tuple[str, bool]:
        """
        앉아 있는 위치와 출퇴근 여부를 조사 하는 함수
        Returns:
            (위치, 출퇴근 여부)
        """
        response = ic.get(
            "users", params={"filter[login]": self._intra_id}
        )  # 42api 정보 받기
        loc = response.json()[0]["location"]  # 현재 위치
        date, time = response.json()[0]["updated_at"].split("T")  # 최근 맥 로그인 시간(UTC)
        date = list(map(int, date.split("-")))
        time = list(map(int, time[:-5].split(":")))
        last_time = datetime.datetime(date[0], date[1], date[2], time[0], time[1], 0)
        last_time += datetime.timedelta(hours=9)  # 최근 맥 로그인 시간(한국 시간)
        now_day = datetime.datetime.now() - datetime.timedelta(
            hours=6
        )  # 익일 새벽 6시를 하루의 끝으로 두고 구한 날짜 -> 6월 5일 0시 0분 0초
        now_day = datetime.datetime(
            now_day.year, now_day.month, now_day.day, 6, 0, 0, 0
        )
        cluster = True if last_time >= now_day else False  # 최근 맥 로그인 시간이 오늘이면 1, 아니면 0
        return (loc, cluster) if loc else ("null", cluster)

    def get_name(self) -> str:
        return self._name

    def get_intra_id(self) -> str:
        return self._intra_id

    def get_baek_id(self) -> str:
        return self._baek_id

    def get_loc(self) -> str:
        return self._loc

    def get_is_working(self) -> bool:
        """
        출퇴근 여부를 반환 하는 함수
        Returns:
            True: 클러스터 옴
            False: 클러스터 안 옴
        """
        return self._is_working

    def get_blackhole(self) -> str:
        return f"{self._blackhole:>5}"

    def get_rank(self) -> str:
        return self._rank

    def get_day(self) -> str:
        return f"{self._day:>5}"
