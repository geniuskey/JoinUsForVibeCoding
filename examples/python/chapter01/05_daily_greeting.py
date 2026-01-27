# examples/python/chapter01/05_daily_greeting.py
# 예제 5-1: 비개발자가 만든 자동화 스크립트
# 프롬프트: "매일 아침 오늘 날짜와 요일을 알려주고, 간단한 동기부여 명언을 보여주는 프로그램을 만들어줘"

import random
from datetime import datetime

# 동기부여 명언 목록
quotes = [
    "작은 걸음이라도 앞으로 나아가는 것이 중요합니다.",
    "오늘 하루도 최선을 다하면 내일이 달라집니다.",
    "실패는 성공의 어머니입니다. 포기하지 마세요!",
    "배움에는 끝이 없습니다. 오늘도 한 가지를 배워봅시다.",
    "할 수 있다고 믿으면, 이미 반은 이룬 것입니다.",
    "천리길도 한 걸음부터. 지금 시작하세요!",
    "어제보다 나은 오늘을 만들어 갑시다.",
    "꾸준함은 재능을 이깁니다.",
]

# 요일 이름 (한국어)
weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

# 현재 날짜와 요일 가져오기
today = datetime.now()
date_str = today.strftime("%Y년 %m월 %d일")
weekday_str = weekday_names[today.weekday()]

# 랜덤 명언 선택
quote = random.choice(quotes)

# 출력
print("=" * 50)
print(f"  좋은 아침이에요!")
print(f"  오늘은 {date_str} {weekday_str}입니다.")
print()
print(f"  오늘의 명언:")
print(f"  \"{quote}\"")
print("=" * 50)
