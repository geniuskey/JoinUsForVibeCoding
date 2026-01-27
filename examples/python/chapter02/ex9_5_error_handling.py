# examples/python/chapter02/ex9_5_error_handling.py
# 예제 9-5: 오류 처리 추가

from datetime import datetime

name = input("이름을 입력하세요: ").strip()

if not name:
    name = "익명"

now = datetime.now()
current_time = now.strftime("%Y년 %m월 %d일 %H시 %M분")

greeting = f"[{current_time}] 환영합니다, {name}님! 바이브 코딩의 세계에 오신 것을 축하합니다!"

print(greeting)

try:
    with open("greeting_log.txt", "a", encoding="utf-8") as f:
        f.write(greeting + "\n")
    print("인사 기록이 greeting_log.txt에 저장되었습니다.")
except PermissionError:
    print("오류: 파일에 쓸 권한이 없습니다.")
except OSError as e:
    print(f"오류: 파일 저장 중 문제가 발생했습니다 - {e}")
