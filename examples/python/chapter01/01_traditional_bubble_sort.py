# examples/python/chapter01/01_traditional_bubble_sort.py
# 예제 3-1: [전통적 코딩] 버블 정렬 직접 구현
# 개발자가 알고리즘을 이해하고 한 줄씩 직접 작성한 코드

def bubble_sort(arr):
    """버블 정렬: 인접한 두 요소를 비교하여 정렬"""
    # 원본 배열을 변경하지 않기 위해 복사
    result = arr.copy()
    n = len(result)

    # 바깥 루프: 전체 패스 횟수
    for i in range(n - 1):
        # 안쪽 루프: 인접 요소 비교
        for j in range(n - 1 - i):
            # 앞 요소가 뒤 요소보다 크면 교환
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]

    return result


# 테스트 데이터
numbers = [64, 34, 25, 12, 22, 11, 90]

print("=== 전통적 코딩: 버블 정렬 ===")
print(f"정렬 전: {numbers}")
sorted_numbers = bubble_sort(numbers)
print(f"정렬 후: {sorted_numbers}")
