"""
예제 13-5: KeyError — 존재하지 않는 딕셔너리 키
=================================================
흔한 오류: 딕셔너리에 없는 키로 접근하려는 경우
"""

# 버그가 있는 코드: 존재하지 않는 키 접근
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
print(f"학번: {student['학번']}")       # ← KeyError! '학번' 키가 없음
print(f"이메일: {student['email']}")    # ← KeyError! 'email' 키가 없음
