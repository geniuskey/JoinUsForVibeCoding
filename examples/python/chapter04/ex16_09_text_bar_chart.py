#!/usr/bin/env python3
"""예제 16-09: 텍스트 막대 그래프

터미널에서 볼 수 있는 수평 막대 그래프를 출력합니다.
"""

def horizontal_bar_chart(title, data, max_width=40, value_suffix=""):
    """수평 막대 그래프를 출력합니다.

    Args:
        title: 차트 제목
        data: [(라벨, 값), ...] 형태의 리스트
        max_width: 막대의 최대 너비(문자 수)
        value_suffix: 값 뒤에 붙일 단위
    """
    if not data:
        return

    max_val = max(v for _, v in data)
    max_label_len = max(len(str(l)) for l, _ in data)

    print()
    print(f"  {title}")
    print(f"  {'=' * (max_label_len + max_width + 15)}")

    for label, value in data:
        bar_len = int(value / max_val * max_width) if max_val > 0 else 0
        bar = "█" * bar_len
        print(f"  {label:<{max_label_len}} │{bar} {value:,}{value_suffix}")

    print(f"  {' ' * max_label_len} └{'─' * (max_width + 1)}")


# === 차트 1: 프로그래밍 언어 인기도 ===
languages = [
    ("Python", 85),
    ("JavaScript", 78),
    ("Java", 65),
    ("TypeScript", 58),
    ("C++", 42),
    ("Go", 35),
    ("Rust", 30),
    ("Swift", 25),
]
horizontal_bar_chart("프로그래밍 언어 인기도 (2024)", languages, value_suffix="점")

# === 차트 2: 월별 방문자 수 ===
monthly_visitors = [
    ("1월", 12500),
    ("2월", 11800),
    ("3월", 15200),
    ("4월", 16800),
    ("5월", 18500),
    ("6월", 21000),
    ("7월", 19800),
    ("8월", 17500),
    ("9월", 20200),
    ("10월", 22100),
    ("11월", 19500),
    ("12월", 23800),
]
horizontal_bar_chart("월별 웹사이트 방문자 수", monthly_visitors, value_suffix="명")

# === 차트 3: 카테고리별 매출 비중 (퍼센트 차트) ===
categories = [
    ("전자기기", 45.2),
    ("의류", 22.8),
    ("식품", 15.5),
    ("도서", 9.3),
    ("생활용품", 7.2),
]

print()
print("  카테고리별 매출 비중")
print(f"  {'=' * 55}")
for label, pct in categories:
    filled = int(pct / 100 * 40)
    empty = 40 - filled
    bar = "█" * filled + "░" * empty
    print(f"  {label:<8} │{bar}│ {pct:.1f}%")
print(f"  {' ' * 8} └{'─' * 40}┘")
print(f"  {' ' * 9} 0%{' ' * 16}50%{' ' * 15}100%")

# === 차트 4: 비교 차트 (두 데이터 세트) ===
print()
print("  분기별 매출 비교 (올해 vs 작년)")
print(f"  {'=' * 55}")
quarters = [
    ("Q1", 3200, 2800),
    ("Q2", 4100, 3500),
    ("Q3", 3800, 3900),
    ("Q4", 4500, 4200),
]

max_val = max(max(a, b) for _, a, b in quarters)
for label, this_year, last_year in quarters:
    bar1_len = int(this_year / max_val * 30)
    bar2_len = int(last_year / max_val * 30)
    bar1 = "█" * bar1_len
    bar2 = "░" * bar2_len
    print(f"  {label} 올해 │{bar1} {this_year:,}만원")
    print(f"  {label} 작년 │{bar2} {last_year:,}만원")
    print(f"  {'':4} │")

print(f"  범례: █ 올해  ░ 작년")
