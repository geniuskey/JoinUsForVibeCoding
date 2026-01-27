"""
예제 12-1: 생성된 코드 설명 요청
==================================
AI가 생성한 복잡한 함수를 이해하기 위해 설명을 요청하는 예제입니다.

프롬프트: "이 코드가 무엇을 하는지 설명해줘"
→ AI에게 코드 설명을 요청하면, 각 부분의 역할을 명확히 이해할 수 있습니다.
"""


# --- AI가 생성한 코드 (처음 보면 복잡해 보임) ---
def find_longest_streak(data):
    """연속으로 증가하는 가장 긴 구간을 찾습니다."""
    if not data:
        return []

    best_start, best_length = 0, 1
    curr_start, curr_length = 0, 1

    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            curr_length += 1
        else:
            if curr_length > best_length:
                best_start = curr_start
                best_length = curr_length
            curr_start = i
            curr_length = 1

    if curr_length > best_length:
        best_start = curr_start
        best_length = curr_length

    return data[best_start:best_start + best_length]


# --- "이 코드 설명해줘" 요청 후 AI가 제공한 설명 ---
def find_longest_streak_explained(data):
    """
    [AI 설명] 연속으로 증가하는 가장 긴 구간을 찾는 함수입니다.

    동작 원리:
    1. 리스트를 처음부터 끝까지 순회합니다.
    2. 현재 값이 이전 값보다 크면 → 연속 증가 구간이 계속됩니다.
    3. 현재 값이 이전 값 이하이면 → 증가 구간이 끊어집니다.
    4. 끊어질 때마다, 지금까지 가장 긴 구간과 비교합니다.
    5. 최종적으로 가장 긴 연속 증가 구간을 반환합니다.

    예시: [3, 1, 2, 4, 7, 2, 5] → [1, 2, 4, 7] (길이 4)
    """
    if not data:
        return []

    # 가장 긴 구간의 시작 위치와 길이
    best_start = 0
    best_length = 1

    # 현재 탐색 중인 구간의 시작 위치와 길이
    curr_start = 0
    curr_length = 1

    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            # 아직 증가 중 → 현재 구간 연장
            curr_length += 1
        else:
            # 증가가 끊김 → 최장 기록 갱신 확인
            if curr_length > best_length:
                best_start = curr_start
                best_length = curr_length
            # 새로운 구간 시작
            curr_start = i
            curr_length = 1

    # 마지막 구간이 최장일 수 있으므로 한 번 더 확인
    if curr_length > best_length:
        best_start = curr_start
        best_length = curr_length

    return data[best_start:best_start + best_length]


# ── 실행 ──
if __name__ == "__main__":
    test_data = [3, 1, 2, 4, 7, 2, 5]

    print("=" * 55)
    print("[예제 12-1] 생성된 코드 설명 요청")
    print("=" * 55)

    print(f"\n입력 데이터: {test_data}")
    print()

    # 원본 코드 실행
    result = find_longest_streak(test_data)
    print(f"[원본 코드 실행 결과]")
    print(f"  가장 긴 연속 증가 구간: {result}")
    print()

    # 설명이 추가된 버전 실행
    result_explained = find_longest_streak_explained(test_data)
    print(f"[설명 추가 버전 실행 결과]")
    print(f"  가장 긴 연속 증가 구간: {result_explained}")
    print()

    # 추가 테스트
    more_tests = [
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [10, 20, 5, 6, 7, 8, 9, 1],
    ]
    print("[추가 테스트]")
    for data in more_tests:
        streak = find_longest_streak(data)
        print(f"  {data} → {streak}")

    print()
    print("Tip: AI에게 '이 코드 설명해줘'라고 요청하면")
    print("     복잡한 코드도 단계별로 이해할 수 있습니다.")
