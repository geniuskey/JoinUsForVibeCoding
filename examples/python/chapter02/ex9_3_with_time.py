# examples/python/chapter02/ex9_3_with_time.py
# 예제 9-3: 현재 시간 표시 추가

from datetime import datetime

name = input("이름을 입력하세요: ").strip()

if not name:
    name = "익명"

now = datetime.now()
current_time = now.strftime("%Y년 %m월 %d일 %H시 %M분")

print(f"환영합니다, {name}님!")
print(f"현재 시간: {current_time}")
print(f"바이브 코딩의 세계에 오신 것을 축하합니다!")
