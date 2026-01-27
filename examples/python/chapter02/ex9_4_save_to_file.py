# examples/python/chapter02/ex9_4_save_to_file.py
# 예제 9-4: 인사말 파일로 저장하기

from datetime import datetime

name = input("이름을 입력하세요: ").strip()

if not name:
    name = "익명"

now = datetime.now()
current_time = now.strftime("%Y년 %m월 %d일 %H시 %M분")

greeting = f"[{current_time}] 환영합니다, {name}님! 바이브 코딩의 세계에 오신 것을 축하합니다!"

print(greeting)

with open("greeting_log.txt", "a", encoding="utf-8") as f:
    f.write(greeting + "\n")

print("인사 기록이 greeting_log.txt에 저장되었습니다.")
