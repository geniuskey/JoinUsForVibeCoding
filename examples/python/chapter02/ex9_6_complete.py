# examples/python/chapter02/ex9_6_complete.py
# 예제 9-6: 완성된 인사 프로그램

from datetime import datetime

def get_time_greeting():
    """현재 시간대에 맞는 인사말을 반환합니다."""
    hour = datetime.now().hour
    if hour < 12:
        return "좋은 아침이에요"
    elif hour < 18:
        return "좋은 오후예요"
    else:
        return "좋은 저녁이에요"

def get_user_name():
    """사용자 이름을 입력받습니다. 빈 입력이면 '익명'을 반환합니다."""
    name = input("이름을 입력하세요: ").strip()
    if not name:
        name = "익명"
    return name

def save_greeting(greeting, filename="greeting_log.txt"):
    """인사 기록을 파일에 저장합니다."""
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(greeting + "\n")
        print(f"인사 기록이 {filename}에 저장되었습니다.")
    except PermissionError:
        print("오류: 파일에 쓸 권한이 없습니다.")
    except OSError as e:
        print(f"오류: 파일 저장 중 문제가 발생했습니다 - {e}")

def main():
    """메인 함수: 인사 프로그램을 실행합니다."""
    name = get_user_name()
    time_greeting = get_time_greeting()
    now = datetime.now()
    current_time = now.strftime("%Y년 %m월 %d일 %H시 %M분")

    print(f"\n{'='*40}")
    print(f"  {time_greeting}, {name}님!")
    print(f"  현재 시간: {current_time}")
    print(f"  바이브 코딩의 세계에 오신 것을 축하합니다!")
    print(f"{'='*40}\n")

    greeting = f"[{current_time}] {time_greeting}, {name}님! 바이브 코딩의 세계에 오신 것을 축하합니다!"
    save_greeting(greeting)

if __name__ == "__main__":
    main()
