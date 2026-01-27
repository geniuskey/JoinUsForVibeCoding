# examples/python/chapter01/ex01_04_cycle_demo.py
# 바이브 코딩의 요청-생성-수정 사이클 데모
#
# [1차 요청] "이름을 입력받아 인사하는 프로그램을 만들어줘"
# [1차 결과] 기본 인사 프로그램 생성
# [2차 요청] "인사말에 현재 날짜도 포함해주고, 이름이 비어있으면 '손님'으로 처리해줘"
# [2차 결과] 개선된 버전 생성 (아래 코드)

from datetime import datetime

def greet(name=""):
    """이름을 받아 날짜와 함께 인사합니다."""
    if not name.strip():
        name = "손님"

    today = datetime.now().strftime("%Y년 %m월 %d일")
    hour = datetime.now().hour

    if hour < 12:
        time_greeting = "좋은 아침이에요"
    elif hour < 18:
        time_greeting = "좋은 오후예요"
    else:
        time_greeting = "좋은 저녁이에요"

    print(f"{'='*40}")
    print(f"  {time_greeting}, {name}님!")
    print(f"  오늘은 {today}입니다.")
    print(f"  바이브 코딩과 함께 멋진 하루 보내세요!")
    print(f"{'='*40}")

# 다양한 경우 테스트
print("[테스트 1: 이름 입력]")
greet("홍길동")

print("\n[테스트 2: 빈 이름]")
greet("")

print("\n[테스트 3: 공백만 입력]")
greet("   ")
