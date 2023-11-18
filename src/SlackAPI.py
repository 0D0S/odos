from slack_sdk import WebClient


class SlackAPI:
    def __init__(self, token: str):
        """
        slack api 관련 동작을 정의한 객체
        Args:
            token: 슬랙에 접근하기 위한 토큰
        """
        self._client = WebClient(token)

    def get_channel_id(self, channel_name: str) -> str:
        """
        슬랙 채널ID를 조회하는 함수
        Args:
            channel_name: 조회할 채널 이름

        Returns:
            조회한 채널 ID
        """
        # conversations_list() 메서드 호출
        result = self._client.conversations_list()
        # 채널 정보 딕셔너리 리스트
        channels = result.data["channels"]
        # 채널 이름이 'test'인 채널 딕셔너리 쿼리
        channel = list(filter(lambda c: c["name"] == channel_name, channels))[0]
        # 채널ID 파싱
        channel_id = channel["id"]
        return channel_id

    def get_message_ts(self, channel_id, query) -> str:
        """
        슬랙 채널 내 메세지를 조회하는 함수
        Args:
            channel_id: 조회할 채널의 ID
            query: 비교할 메세지

        Returns:
            조회한 메세지
        """
        # conversations_history() 메서드 호출
        result = self._client.conversations_history(channel=channel_id)
        # 채널 내 메세지 정보 딕셔너리 리스트
        messages = result.data["messages"]
        # 채널 내 메세지가 query와 일치하는 메세지 딕셔너리 쿼리
        message = list(filter(lambda m: m["text"] == query, messages))[0]
        # 해당 메세지ts 파싱
        message_ts = message["ts"]
        return message_ts

    def post_thread_message(self, channel_id, message_ts, text):
        """
        슬랙 채널 내 메세지 thread에 댓글 달기
        Args:
            channel_id: 채널 ID
            message_ts:
            text: 댓글 달 메세지

        Returns:

        """
        # chat_postMessage() 메서드 호출
        result = self._client.chat_postMessage(
            channel=channel_id, text=text, thread_ts=message_ts
        )
        return result

    def post_chat_message(self, channel_id, text) -> None:
        """
        슬랙 채널에 메세지를 올리는 함수
        Args:
            channel_id: 메세지를 올릴 채널의 ID
            text: 올릴 메세지
        """
        result = self._client.chat_postMessage(
            channel=channel_id,
            text=text,
        )
