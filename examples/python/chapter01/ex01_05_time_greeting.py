# examples/python/chapter01/ex01_05_time_greeting.py
# 바이브 코딩으로 만든 시간대별 인사 프로그램
# AI에게 "현재 시간에 따라 다른 인사말을 보여주고,
# 오늘의 명언도 랜덤으로 하나 출력해주는 프로그램을 만들어줘"라고 요청

import random
from datetime import datetime

def get_time_emoji(hour):
    """시간대에 맞는 이모지를 반환합니다."""
    if hour < 6:
        return "[밤]"
    elif hour < 12:
        return "[아침]"
    elif hour < 18:
        return "[오후]"
    else:
        return "[저녁]"

def get_greeting(hour):
    """시간대에 맞는 인사말을 반환합니다."""
    if hour < 6:
        return "늦은 밤까지 수고하시네요!"
    elif hour < 12:
        return "좋은 아침입니다! 오늘도 화이팅!"
    elif hour < 18:
        return "좋은 오후입니다! 힘내세요!"
    else:
        return "좋은 저녁입니다! 오늘 하루도 수고했어요!"

def get_random_quote():
    """바이브 코딩 관련 명언을 랜덤으로 반환합니다."""
    quotes = [
        "코드를 잊어버리세요. 비전에 집중하세요. - 바이브 코딩의 철학",
        "완벽한 코드보다 동작하는 프로그램이 먼저입니다.",
        "AI는 도구이고, 여러분은 창작자입니다.",
        "질문하는 능력이 곧 프로그래밍 능력입니다.",
        "작게 시작하고, 자주 실행하고, 계속 개선하세요.",
    ]
    return random.choice(quotes)

def main():
    now = datetime.now()
    hour = now.hour
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    emoji = get_time_emoji(hour)
    greeting = get_greeting(hour)
    quote = get_random_quote()

    print(f"\n{'*' * 50}")
    print(f"  {emoji} 현재 시각: {time_str}")
    print(f"  {greeting}")
    print(f"{'*' * 50}")
    print(f"\n  [오늘의 한마디]")
    print(f"  \"{quote}\"")
    print(f"\n{'*' * 50}")
    print(f"  바이브 코딩으로 이 프로그램이 만들어졌습니다!")
    print(f"{'*' * 50}\n")

if __name__ == "__main__":
    main()
