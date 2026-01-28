"""
Chapter 22 - 성능 최적화
예제 22-08: 실습 - 느린 코드 최적화 (before/after 비교)

실제로 흔히 발생하는 성능 문제를 가진 코드를 분석하고
최적화하는 과정을 단계별로 보여줍니다.

시나리오: 학생 성적 데이터를 처리하는 프로그램
"""

import time
import random
import functools


# ============================================================
# 데이터 생성
# ============================================================

def generate_students(n):
    """학생 성적 데이터 생성"""
    subjects = ["수학", "영어", "과학", "국어", "사회"]
    random.seed(42)
    students = []
    for i in range(n):
        scores = {subj: random.randint(30, 100) for subj in subjects}
        students.append({
            "id": i + 1,
            "name": f"학생_{i+1:05d}",
            "class": random.choice(["A", "B", "C", "D", "E"]),
            "scores": scores,
        })
    return students


# ============================================================
# BEFORE: 최적화 전 (느린 코드)
# ============================================================

def slow_get_average(student):
    """느린 평균 계산: 매번 과목 목록을 순회"""
    total = 0
    count = 0
    for subject in student["scores"]:
        total = total + student["scores"][subject]
        count = count + 1
    return total / count


def slow_find_top_students(students, n=10):
    """느린 상위 학생 찾기: 매번 전체를 정렬"""
    # 문제 1: 매 호출마다 평균을 다시 계산
    # 문제 2: 전체를 정렬한 후 상위 n개만 사용
    sorted_students = sorted(
        students,
        key=lambda s: slow_get_average(s),
        reverse=True,
    )
    return sorted_students[:n]


def slow_class_statistics(students):
    """느린 반별 통계: 비효율적인 반복"""
    classes = []
    # 문제 1: 반 목록을 비효율적으로 추출
    for s in students:
        if s["class"] not in classes:
            classes.append(s["class"])

    result = {}
    for cls in classes:
        # 문제 2: 매 반마다 전체 학생을 순회
        class_students = []
        for s in students:
            if s["class"] == cls:
                class_students.append(s)

        # 문제 3: 평균을 매번 다시 계산
        averages = []
        for s in class_students:
            avg = slow_get_average(s)
            averages.append(avg)

        # 문제 4: 수동으로 합계/최대/최소 계산
        total = 0
        for a in averages:
            total += a
        class_avg = total / len(averages)

        max_avg = averages[0]
        for a in averages:
            if a > max_avg:
                max_avg = a

        min_avg = averages[0]
        for a in averages:
            if a < min_avg:
                min_avg = a

        result[cls] = {
            "학생수": len(class_students),
            "평균": class_avg,
            "최고": max_avg,
            "최저": min_avg,
        }

    return result


def slow_find_failing_students(students, threshold=50):
    """느린 과락 학생 찾기: 중첩 반복"""
    failing = []
    for student in students:
        for subject, score in student["scores"].items():
            if score < threshold:
                # 문제: 이미 추가된 학생인지 비효율적으로 확인
                already_added = False
                for f in failing:
                    if f["id"] == student["id"]:
                        already_added = True
                        break
                if not already_added:
                    failing.append(student)
    return failing


def slow_full_pipeline(students):
    """느린 전체 파이프라인"""
    top = slow_find_top_students(students, 10)
    stats = slow_class_statistics(students)
    failing = slow_find_failing_students(students)
    return top, stats, failing


# ============================================================
# AFTER: 최적화 후 (빠른 코드)
# ============================================================

def fast_get_average(scores):
    """빠른 평균 계산: 내장 함수 활용"""
    return sum(scores.values()) / len(scores)


def fast_find_top_students(students_with_avg, n=10):
    """
    빠른 상위 학생 찾기:
    - 미리 계산된 평균을 사용
    - heapq 대신 정렬 사용 (Python sort는 Timsort로 매우 빠름)
    """
    sorted_students = sorted(
        students_with_avg,
        key=lambda s: s["average"],
        reverse=True,
    )
    return sorted_students[:n]


def fast_class_statistics(students_with_avg):
    """
    빠른 반별 통계:
    - 한 번의 순회로 반별 그룹핑
    - 내장 함수 활용
    """
    # 한 번의 순회로 반별 그룹핑
    class_groups = {}
    for s in students_with_avg:
        cls = s["class"]
        if cls not in class_groups:
            class_groups[cls] = []
        class_groups[cls].append(s["average"])

    result = {}
    for cls, averages in class_groups.items():
        result[cls] = {
            "학생수": len(averages),
            "평균": sum(averages) / len(averages),
            "최고": max(averages),
            "최저": min(averages),
        }

    return result


def fast_find_failing_students(students, threshold=50):
    """
    빠른 과락 학생 찾기:
    - set으로 중복 확인
    - any() 활용
    """
    failing = []
    seen_ids = set()
    for student in students:
        if student["id"] not in seen_ids:
            if any(score < threshold for score in student["scores"].values()):
                failing.append(student)
                seen_ids.add(student["id"])
    return failing


def fast_full_pipeline(students):
    """빠른 전체 파이프라인: 평균을 한 번만 계산"""
    # 핵심 최적화: 평균을 한 번만 계산하여 재사용
    students_with_avg = []
    for s in students:
        s_copy = s.copy()
        s_copy["average"] = fast_get_average(s["scores"])
        students_with_avg.append(s_copy)

    top = fast_find_top_students(students_with_avg, 10)
    stats = fast_class_statistics(students_with_avg)
    failing = fast_find_failing_students(students)
    return top, stats, failing


# ============================================================
# 실행 및 비교
# ============================================================

def measure(func, *args):
    """실행 시간 측정"""
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed


if __name__ == "__main__":
    print("=" * 65)
    print("  실습: 느린 코드 최적화 (Before vs After)")
    print("=" * 65)

    # 데이터 생성
    sizes = [1_000, 5_000, 10_000]

    for size in sizes:
        students = generate_students(size)
        print(f"\n{'=' * 65}")
        print(f"  학생 수: {size:,}명")
        print(f"{'=' * 65}")

        # --- BEFORE: 느린 코드 ---
        (slow_top, slow_stats, slow_failing), slow_time = measure(
            slow_full_pipeline, students
        )

        # --- AFTER: 빠른 코드 ---
        (fast_top, fast_stats, fast_failing), fast_time = measure(
            fast_full_pipeline, students
        )

        # --- 결과 비교 ---
        print(f"\n  [ 실행 시간 비교 ]")
        print(f"  {'최적화 전:':>12} {slow_time:.4f}초")
        print(f"  {'최적화 후:':>12} {fast_time:.4f}초")
        if fast_time > 0:
            print(f"  {'속도 향상:':>12} {slow_time / fast_time:.1f}배")

        # 결과 정확성 검증
        slow_top_ids = sorted([s["id"] for s in slow_top])
        fast_top_ids = sorted([s["id"] for s in fast_top])
        stats_match = all(
            abs(slow_stats[c]["평균"] - fast_stats[c]["평균"]) < 0.01
            for c in slow_stats
        )
        failing_match = len(slow_failing) == len(fast_failing)

        print(f"\n  [ 결과 정확성 검증 ]")
        print(f"    상위 학생 일치: {'예' if slow_top_ids == fast_top_ids else '아니오'}")
        print(f"    반별 통계 일치: {'예' if stats_match else '아니오'}")
        print(f"    과락 학생 수:   느린 코드={len(slow_failing)}, 빠른 코드={len(fast_failing)} ({'일치' if failing_match else '불일치'})")

    # --- 최종 결과 상세 (가장 큰 데이터 기준) ---
    print(f"\n{'=' * 65}")
    print(f"  상세 결과 (학생 {sizes[-1]:,}명 기준)")
    print(f"{'=' * 65}")

    print(f"\n  [ 상위 10명 ]")
    for i, s in enumerate(fast_top[:10], 1):
        print(f"    {i:>2}위: {s['name']} (반: {s['class']}) 평균: {s['average']:.1f}점")

    print(f"\n  [ 반별 통계 ]")
    for cls in sorted(fast_stats.keys()):
        s = fast_stats[cls]
        print(f"    {cls}반: 학생수={s['학생수']:,}명, "
              f"평균={s['평균']:.1f}, 최고={s['최고']:.1f}, 최저={s['최저']:.1f}")

    print(f"\n  [ 과락 학생 수 ]: {len(fast_failing):,}명")

    # --- 최적화 포인트 정리 ---
    print(f"\n{'=' * 65}")
    print("  최적화 포인트 정리")
    print(f"{'=' * 65}")
    print()
    print("  1. 반복 계산 제거")
    print("     - Before: 평균을 필요할 때마다 매번 다시 계산")
    print("     - After:  한 번 계산하여 결과를 재사용")
    print()
    print("  2. 적절한 자료구조 사용")
    print("     - Before: 리스트에서 선형 탐색으로 중복 확인 O(n)")
    print("     - After:  집합(set)으로 O(1) 중복 확인")
    print()
    print("  3. 불필요한 순회 제거")
    print("     - Before: 반 목록 추출에 별도 순회 + 반별 필터에 전체 순회")
    print("     - After:  한 번의 순회로 반별 그룹핑 완료")
    print()
    print("  4. 내장 함수 활용")
    print("     - Before: 수동 for 루프로 합계/최대/최소 계산")
    print("     - After:  sum(), max(), min(), any() 내장 함수 활용")
    print()
    print("  5. 조기 종료 (Early Exit)")
    print("     - Before: 모든 과목을 확인 후 과락 판정")
    print("     - After:  any()로 첫 과락 과목 발견 시 즉시 판정")
