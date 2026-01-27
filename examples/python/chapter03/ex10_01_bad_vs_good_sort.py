"""
예제 10-1: 나쁜 프롬프트 vs 좋은 프롬프트 — 정렬 요청
=======================================================
나쁜 프롬프트: "정렬 해줘"
좋은 프롬프트: "정수 리스트를 받아 내림차순으로 정렬하고,
              각 단계를 출력하는 버블 정렬 함수를 작성해줘"
"""

# --- 나쁜 프롬프트로 생성된 코드 ---
# 프롬프트: "정렬 해줘"
# → 무엇을 정렬? 어떤 순서? 어떤 알고리즘? 알 수 없음

def bad_sort(data):
    """모호한 요청의 결과: 기본 정렬만 수행"""
    return sorted(data)


# --- 좋은 프롬프트로 생성된 코드 ---
# 프롬프트: "정수 리스트를 받아 내림차순으로 버블 정렬하고,
#           각 단계(pass)를 출력하는 함수를 작성해줘.
#           함수명은 bubble_sort_descending으로 해줘."

def bubble_sort_descending(numbers):
    """
    내림차순 버블 정렬 — 각 단계를 출력합니다.

    Args:
        numbers: 정수 리스트
    Returns:
        내림차순으로 정렬된 리스트
    """
    arr = numbers.copy()
    n = len(arr)
    print(f"원본 리스트: {arr}")
    print(f"목표: 내림차순 버블 정렬\n")

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] < arr[j + 1]:       # 내림차순이므로 < 비교
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        print(f"  Pass {i + 1}: {arr}")
        if not swapped:
            print("  (더 이상 교환 없음 — 조기 종료)")
            break

    print(f"\n정렬 결과: {arr}")
    return arr


# ── 실행 ──
if __name__ == "__main__":
    sample = [64, 25, 12, 22, 11]

    print("=" * 50)
    print("[나쁜 프롬프트 결과]")
    print(f"  sorted → {bad_sort(sample)}")
    print("  → 오름차순인지 내림차순인지, 알고리즘은 무엇인지 불명확")
    print()

    print("=" * 50)
    print("[좋은 프롬프트 결과]")
    bubble_sort_descending(sample)
    print("  → 명확한 알고리즘, 정렬 방향, 과정 출력까지 포함")
