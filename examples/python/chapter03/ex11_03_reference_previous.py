# examples/python/chapter03/ex11_03_reference_previous.py
# 예제 11-3: "이전 코드에서..." 참조하기
#
# AI와의 대화에서 이전에 작성한 코드를 참조하는 방법을 보여줍니다.
# 효과적인 참조 vs 비효과적인 참조의 차이를 설명합니다.

import sys


def show_reference_patterns():
    """이전 코드 참조 패턴을 보여줍니다"""
    print("=" * 58)
    print("  AI 대화에서 이전 코드 참조하기")
    print("=" * 58)

    print()
    print("  ✓ 효과적인 참조 방법:")
    print("  ─" * 27)
    good_examples = [
        (
            "구체적 함수 참조",
            "이전에 만든 calculate_total() 함수에\n"
            "                    할인율 매개변수를 추가해줘"
        ),
        (
            "구조 참조",
            "아까 만든 학생 딕셔너리에\n"
            "                    '출석률' 필드를 추가해줘"
        ),
        (
            "동작 참조",
            "방금 만든 코드에서 파일을 읽는 부분이\n"
            "                    에러가 나. 예외 처리를 추가해줘"
        ),
        (
            "단계 참조",
            "2단계에서 만든 정렬 기능을\n"
            "                    역순 정렬도 가능하게 수정해줘"
        ),
    ]
    for title, example in good_examples:
        print(f"    • {title}: \"{example}\"")
        print()

    print("  ✗ 비효과적인 참조 방법:")
    print("  ─" * 27)
    bad_examples = [
        (
            "모호한 참조",
            "그거 수정해줘",
            "'이전에 만든 정렬 함수를 수정해줘'라고 구체적으로",
        ),
        (
            "너무 광범위",
            "전체 코드를 개선해줘",
            "'성능이 느린 검색 부분을 개선해줘'라고 범위를 좁혀서",
        ),
        (
            "맥락 없는 참조",
            "에러 고쳐줘",
            "에러 메시지를 포함하여 '이 에러가 발생해: ...'라고",
        ),
    ]
    for title, bad, better in bad_examples:
        print(f"    • {title}: \"{bad}\"")
        print(f"      → 대신: \"{better}\"")
        print()


def demo_reference_conversation():
    """참조를 활용한 대화 시뮬레이션"""
    print("\n" + "=" * 58)
    print("  참조를 활용한 대화 시뮬레이션")
    print("=" * 58)

    # 1단계: 기본 코드 작성
    print("\n[1단계 대화]")
    print('  사용자: "학생 성적 관리 프로그램을 만들어줘"')
    print('  AI: 네, 기본 성적 관리 프로그램을 작성하겠습니다.')
    print()

    students_v1 = [
        {"이름": "김민수", "국어": 85, "영어": 90, "수학": 78},
        {"이름": "이서연", "국어": 92, "영어": 88, "수학": 95},
        {"이름": "박지훈", "국어": 78, "영어": 82, "수학": 88},
    ]

    print("  [생성된 코드 - v1]")
    print("  students = [")
    for s in students_v1:
        print(f'    {{"이름": "{s["이름"]}", '
              f'"국어": {s["국어"]}, "영어": {s["영어"]}, "수학": {s["수학"]}}},')
    print("  ]")

    # 2단계: 이전 코드 참조하여 기능 추가
    print("\n[2단계 대화] - 이전 코드 참조")
    print('  사용자: "이전에 만든 학생 데이터에 평균 계산 기능을 추가해줘"')
    print('  AI: 네, 학생 데이터를 활용해서 평균을 계산하겠습니다.')
    print()

    print("  [생성된 코드 - v2] (참조로 인해 기존 구조 유지)")
    print("  ─" * 27)
    for s in students_v1:
        avg = (s["국어"] + s["영어"] + s["수학"]) / 3
        print(f'  {s["이름"]}: 국어={s["국어"]}, 영어={s["영어"]}, '
              f'수학={s["수학"]} → 평균: {avg:.1f}')

    # 3단계: 구체적 참조로 수정 요청
    print(f"\n[3단계 대화] - 구체적 참조로 수정")
    print('  사용자: "2단계에서 만든 평균 계산에서 가장 높은 과목도 표시해줘"')
    print('  AI: 네, 평균과 함께 최고 점수 과목을 표시하겠습니다.')
    print()

    print("  [생성된 코드 - v3] (단계를 명시하여 정확한 참조)")
    print("  ─" * 27)
    for s in students_v1:
        avg = (s["국어"] + s["영어"] + s["수학"]) / 3
        scores = {"국어": s["국어"], "영어": s["영어"], "수학": s["수학"]}
        best = max(scores, key=scores.get)
        print(f'  {s["이름"]}: 평균 {avg:.1f} | '
              f'최고 과목: {best}({scores[best]}점)')

    print()
    print("  핵심: '2단계에서 만든', '이전에 만든 학생 데이터에'처럼")
    print("  구체적으로 참조하면 AI가 정확하게 이해합니다.")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--patterns":
        show_reference_patterns()
    else:
        show_reference_patterns()
        demo_reference_conversation()
