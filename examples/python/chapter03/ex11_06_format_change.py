# examples/python/chapter03/ex11_06_format_change.py
# 예제 11-6: 수정 요청 피드백 예시
#
# AI에게 출력 형식 변경을 요청하는 피드백 방법을 보여줍니다.
# "출력 형식을 표로 바꿔줘"

import sys


# ============================================================
# 샘플 데이터
# ============================================================

SALES_DATA = [
    {"제품": "노트북", "1분기": 150, "2분기": 180, "3분기": 200, "4분기": 220},
    {"제품": "태블릿", "1분기": 90, "2분기": 110, "3분기": 95, "4분기": 130},
    {"제품": "스마트폰", "1분기": 300, "2분기": 280, "3분기": 320, "4분기": 350},
    {"제품": "이어폰", "1분기": 200, "2분기": 250, "3분기": 230, "4분기": 270},
    {"제품": "스마트워치", "1분기": 60, "2분기": 80, "3분기": 100, "4분기": 120},
]


# ============================================================
# [1차 대화] "판매 데이터를 분석해서 보여줘"
# → AI가 기본 텍스트 형식으로 출력
# ============================================================

def format_v1_basic(data):
    """1차: 기본 텍스트 출력"""
    print("=" * 50)
    print("  [1차] 기본 텍스트 출력")
    print('  → "판매 데이터를 분석해서 보여줘"')
    print("=" * 50)
    print()

    for item in data:
        total = item["1분기"] + item["2분기"] + item["3분기"] + item["4분기"]
        avg = total / 4
        print(f"  {item['제품']}: "
              f"1분기={item['1분기']}, 2분기={item['2분기']}, "
              f"3분기={item['3분기']}, 4분기={item['4분기']} "
              f"(합계: {total}, 평균: {avg:.0f})")
    print()


# ============================================================
# [2차 대화] "출력 형식을 표로 바꿔줘"
# → 수정 피드백: 구체적으로 어떤 형식을 원하는지 전달
# ============================================================

def format_v2_table(data):
    """2차: 표 형식 출력"""
    print("=" * 65)
    print("  [2차] 표 형식 출력")
    print('  → "출력 형식을 표로 바꿔줘"')
    print("=" * 65)
    print()

    # 헤더
    header = f"  {'제품':<10} {'1분기':>6} {'2분기':>6} {'3분기':>6} {'4분기':>6} {'합계':>6} {'평균':>6}"
    separator = "  " + "─" * 58

    print(header)
    print(separator)

    # 데이터 행
    grand_total = 0
    for item in data:
        total = item["1분기"] + item["2분기"] + item["3분기"] + item["4분기"]
        avg = total / 4
        grand_total += total
        print(f"  {item['제품']:<10} {item['1분기']:>6} {item['2분기']:>6} "
              f"{item['3분기']:>6} {item['4분기']:>6} {total:>6} {avg:>6.0f}")

    print(separator)
    print(f"  {'전체 합계':<10} {'':>6} {'':>6} {'':>6} {'':>6} "
          f"{grand_total:>6} {grand_total / len(data):>6.0f}")
    print()


# ============================================================
# [3차 대화] "증감 추세도 표시해주고, 보기 좋게 정리해줘"
# → 더 구체적인 수정 피드백
# ============================================================

def format_v3_rich_table(data):
    """3차: 추세 포함 리치 테이블"""
    print("=" * 72)
    print("  [3차] 추세 포함 리치 테이블")
    print('  → "증감 추세도 표시해주고, 보기 좋게 정리해줘"')
    print("=" * 72)
    print()

    print("  ┌──────────┬───────┬───────┬───────┬───────┬───────┬──────┬──────┐")
    print("  │ 제품     │ 1분기 │ 2분기 │ 3분기 │ 4분기 │ 합계  │ 평균 │ 추세 │")
    print("  ├──────────┼───────┼───────┼───────┼───────┼───────┼──────┼──────┤")

    grand_total = 0
    for item in data:
        q = [item["1분기"], item["2분기"], item["3분기"], item["4분기"]]
        total = sum(q)
        avg = total / 4
        grand_total += total

        # 추세 계산 (1분기 대비 4분기 증감률)
        change = ((q[3] - q[0]) / q[0]) * 100

        if change > 10:
            trend = "▲▲"
        elif change > 0:
            trend = " ▲"
        elif change == 0:
            trend = " ─"
        elif change > -10:
            trend = " ▼"
        else:
            trend = "▼▼"

        # 한국어 이름 패딩 처리
        name = item["제품"]
        name_display = f"{name}{'　' * (4 - len(name))}" if len(name) < 4 else name[:4]

        print(f"  │ {name_display}   │ {q[0]:>5} │ {q[1]:>5} │ "
              f"{q[2]:>5} │ {q[3]:>5} │ {total:>5} │ {avg:>4.0f} │  {trend}  │")

    print("  ├──────────┼───────┼───────┼───────┼───────┼───────┼──────┼──────┤")
    grand_avg = grand_total / len(data)
    print(f"  │ 합계     │       │       │       │       │ {grand_total:>5} │ {grand_avg:>4.0f} │      │")
    print("  └──────────┴───────┴───────┴───────┴───────┴───────┴──────┴──────┘")
    print()
    print("  추세: ▲▲ = 10% 이상 성장, ▲ = 소폭 성장, ▼ = 소폭 하락, ▼▼ = 10% 이상 하락")
    print()


# ============================================================
# 수정 피드백 가이드
# ============================================================

def show_feedback_guide():
    """효과적인 수정 피드백 방법을 안내합니다"""
    print("\n" + "=" * 58)
    print("  수정 요청 피드백 가이드")
    print("=" * 58)
    print()
    print("  효과적인 수정 피드백 패턴:")
    print()
    print('  1. 형식 변경: "출력을 표로 바꿔줘"')
    print('                "JSON 형식으로 출력해줘"')
    print('                "CSV로 저장할 수 있게 해줘"')
    print()
    print('  2. 정보 추가: "여기에 합계도 표시해줘"')
    print('                "증감률도 보여줘"')
    print('                "비율(%)도 포함해줘"')
    print()
    print('  3. 스타일 변경: "더 보기 좋게 정리해줘"')
    print('                  "정렬을 맞춰줘"')
    print('                  "구분선을 추가해줘"')
    print()
    print("  핵심: 무엇을 어떻게 바꾸고 싶은지 구체적으로!")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--v1":
        format_v1_basic(SALES_DATA)
    elif len(sys.argv) > 1 and sys.argv[1] == "--v2":
        format_v2_table(SALES_DATA)
    elif len(sys.argv) > 1 and sys.argv[1] == "--v3":
        format_v3_rich_table(SALES_DATA)
    elif len(sys.argv) > 1 and sys.argv[1] == "--guide":
        show_feedback_guide()
    else:
        show_feedback_guide()
        format_v1_basic(SALES_DATA)
        format_v2_table(SALES_DATA)
        format_v3_rich_table(SALES_DATA)
