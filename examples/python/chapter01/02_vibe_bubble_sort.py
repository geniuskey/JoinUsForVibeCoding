# examples/python/chapter01/02_vibe_bubble_sort.py
# 예제 3-2: [바이브 코딩] 정렬 AI에게 요청
#
# 프롬프트: "리스트를 정렬하는 함수를 만들어줘.
#           버블 정렬 알고리즘을 사용하고, 각 단계를 출력해줘"
#
# 아래는 AI가 생성한 결과물입니다.

def bubble_sort_with_steps(arr):
    """
    버블 정렬을 수행하며 각 단계를 시각적으로 출력합니다.

    Args:
        arr: 정렬할 숫자 리스트
    Returns:
        정렬된 리스트
    """
    result = arr.copy()
    n = len(result)
    total_swaps = 0

    print(f"초기 상태: {result}")
    print(f"배열 길이: {n}")
    print("-" * 50)

    for i in range(n - 1):
        swapped = False
        print(f"\n[패스 {i + 1}]")

        for j in range(n - 1 - i):
            if result[j] > result[j + 1]:
                print(f"  {result[j]} > {result[j + 1]} -> 교환!", end="")
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
                total_swaps += 1
                print(f"  결과: {result}")
            else:
                print(f"  {result[j]} <= {result[j + 1]} -> 유지")

        if not swapped:
            print("  교환 없음 - 정렬 완료!")
            break

    print("-" * 50)
    print(f"총 교환 횟수: {total_swaps}")
    return result


# 실행
numbers = [64, 34, 25, 12, 22, 11, 90]
print("=== 바이브 코딩: 버블 정렬 (단계별 출력) ===\n")
sorted_numbers = bubble_sort_with_steps(numbers)
print(f"\n최종 결과: {sorted_numbers}")
