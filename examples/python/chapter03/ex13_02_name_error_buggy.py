"""
예제 13-2: NameError — 변수 이름 오타
======================================
흔한 오류: 변수명 철자가 다른 경우
"""

# 버그가 있는 코드: 변수명 오타 (user_name vs user_naem)
user_name = "홍길동"
user_age = 25

# 'user_naem'은 정의되지 않은 변수 (올바른 이름: user_name)
print(f"이름: {user_naem}")
print(f"나이: {user_age}세")
print(f"{user_name}님, 환영합니다!")
