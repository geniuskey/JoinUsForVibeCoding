# examples/python/chapter01/04_02_explain_code.py
# AI에게 코드 설명을 요청하고 더 쉬운 버전을 받는 예제

# === 복잡한 버전 (리스트 컴프리헨션) ===
print("=== 복잡한 버전 ===")
data = [
    {"name": "김철수", "score": 85},
    {"name": "이영희", "score": 92},
    {"name": "박민수", "score": 78},
    {"name": "정수진", "score": 95},
    {"name": "최동현", "score": 60},
]

# 한 줄로 작성된 복잡한 리스트 컴프리헨션
result = sorted([d["name"] for d in data if d["score"] >= 80], key=lambda x: x)
print(f"80점 이상 학생 (정렬): {result}")

print()

# === AI가 알려준 쉬운 버전 ===
print("=== AI가 설명해준 쉬운 버전 ===")

# 1단계: 80점 이상인 학생 필터링
passing_students = []
for student in data:
    if student["score"] >= 80:
        passing_students.append(student["name"])

# 2단계: 이름순으로 정렬
passing_students.sort()

# 3단계: 결과 출력
print(f"80점 이상 학생 (정렬): {passing_students}")

# 결과가 동일한지 확인
print(f"\n두 결과가 같은가? {result == passing_students}")
