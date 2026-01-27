"""
예제 13-2: NameError — 변수 이름 오타 (수정 완료)
==================================================
수정: 오타가 난 변수명을 올바르게 수정
"""

# 수정된 코드: user_naem → user_name
user_name = "홍길동"
user_age = 25

print(f"이름: {user_name}")    # ← user_naem → user_name 수정!
print(f"나이: {user_age}세")
print(f"{user_name}님, 환영합니다!")
