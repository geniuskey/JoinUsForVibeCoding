"""
예제 13-5: KeyError — 존재하지 않는 딕셔너리 키 (수정 완료)
============================================================
수정: .get() 메서드 또는 in 키워드로 키 존재 여부 확인
"""

# 수정된 코드: 안전한 딕셔너리 접근
student = {
    "이름": "김철수",
    "나이": 20,
    "학과": "컴퓨터공학",
    "학년": 2
}

print("=== 학생 정보 ===")
print(f"이름: {student['이름']}")
print(f"나이: {student['나이']}")
print(f"학과: {student['학과']}")
print(f"학년: {student['학년']}")

# 방법 1: .get()으로 기본값 지정
print(f"학번: {student.get('학번', '미등록')}")        # ← 키가 없으면 '미등록' 반환
print(f"이메일: {student.get('email', '미등록')}")     # ← 키가 없으면 '미등록' 반환

# 방법 2: in 키워드로 키 존재 여부 확인
print("\n=== 키 존재 여부 확인 ===")
for key in ["이름", "학번", "email", "학과"]:
    if key in student:
        print(f"  {key}: {student[key]}")
    else:
        print(f"  {key}: (정보 없음)")
