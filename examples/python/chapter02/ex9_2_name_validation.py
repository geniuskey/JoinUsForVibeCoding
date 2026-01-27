# examples/python/chapter02/ex9_2_name_validation.py
# 예제 9-2: 사용자 이름 입력받기 개선 (빈 이름 처리)

name = input("이름을 입력하세요: ").strip()

if not name:
    name = "익명"

print(f"환영합니다, {name}님! 바이브 코딩의 세계에 오신 것을 축하합니다!")
