"""
예제 13-9: 논리 오류 — 성적 계산기의 잘못된 조건 (수정 완료)
=============================================================
수정: 조건문을 높은 점수부터 검사하도록 순서 변경
"""

# 수정된 코드: 높은 점수부터 차례대로 검사
def calculate_grade(score):
    """점수를 받아 학점을 반환 (올바른 버전)"""
    if score >= 90:       # ← 가장 높은 기준부터 확인!
        grade = "A"
    elif score >= 80:     # 90 미만이면서 80 이상
        grade = "B"
    elif score >= 70:     # 80 미만이면서 70 이상
        grade = "C"
    elif score >= 60:     # 70 미만이면서 60 이상
        grade = "D"
    else:                 # 60 미만
        grade = "F"
    return grade


# 테스트
print("=== 성적 계산기 (수정된 버전) ===")
test_scores = [95, 85, 75, 65, 55]

for score in test_scores:
    grade = calculate_grade(score)
    print(f"  {score}점 → {grade}학점")

print("\n올바른 결과:")
print("  95점 → A, 85점 → B, 75점 → C, 65점 → D, 55점 → F")
