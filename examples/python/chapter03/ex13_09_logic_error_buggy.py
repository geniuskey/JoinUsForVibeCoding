"""
예제 13-9: 논리 오류 — 성적 계산기의 잘못된 조건
==================================================
오류 없이 실행되지만 잘못된 결과를 출력하는 논리 오류
조건문 순서가 잘못되어 모든 점수가 "A학점"으로 판정됨
"""

# 버그가 있는 코드: 조건문 순서가 잘못됨
def calculate_grade(score):
    """점수를 받아 학점을 반환 (잘못된 버전)"""
    if score >= 60:       # ← 버그! 60점 이상이면 모두 여기에 걸림
        grade = "A"
    elif score >= 70:     # ← 도달 불가능!
        grade = "B"
    elif score >= 80:     # ← 도달 불가능!
        grade = "C"
    elif score >= 90:     # ← 도달 불가능!
        grade = "D"
    else:
        grade = "F"
    return grade


# 테스트
print("=== 성적 계산기 (버그 있는 버전) ===")
test_scores = [95, 85, 75, 65, 55]

for score in test_scores:
    grade = calculate_grade(score)
    print(f"  {score}점 → {grade}학점")

print("\n⚠️ 모든 60점 이상 점수가 A학점으로 나옵니다!")
