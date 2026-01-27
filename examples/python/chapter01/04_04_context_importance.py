# examples/python/chapter01/04_04_context_importance.py
# 컨텍스트 제공 여부에 따른 AI 결과물 차이 데모

print("=" * 50)
print("버전 1: 컨텍스트 없이 요청한 결과")
print("  요청: '데이터를 처리하는 코드 만들어줘'")
print("=" * 50)

# 컨텍스트 없이 요청하면 AI가 추측해서 만든 일반적인 코드
data_v1 = [1, 2, 3, 4, 5]

def process_data_v1(data):
    """일반적인 데이터 처리 (컨텍스트 없이 생성됨)"""
    result = []
    for item in data:
        result.append(item * 2)
    return result

result_v1 = process_data_v1(data_v1)
print(f"입력: {data_v1}")
print(f"출력: {result_v1}")
print("-> AI가 '데이터 처리'를 단순 변환으로 해석함")

print()
print("=" * 50)
print("버전 2: 컨텍스트를 제공하고 요청한 결과")
print("  요청: '학생 시험 점수 리스트에서 과목별 평균을")
print("         구하고, 평균 이상인 학생을 찾아줘'")
print("=" * 50)

# 컨텍스트를 제공하면 목적에 맞는 정확한 코드가 생성됨
students = [
    {"name": "김철수", "math": 85, "english": 72},
    {"name": "이영희", "math": 92, "english": 88},
    {"name": "박민수", "math": 78, "english": 95},
    {"name": "정수진", "math": 65, "english": 80},
]

def process_scores(students):
    """학생 점수 분석 (컨텍스트 제공 후 생성됨)"""
    # 과목별 평균 계산
    math_avg = sum(s["math"] for s in students) / len(students)
    eng_avg = sum(s["english"] for s in students) / len(students)

    print(f"수학 평균: {math_avg:.1f}점")
    print(f"영어 평균: {eng_avg:.1f}점")
    print()

    # 평균 이상인 학생 찾기
    print("수학 평균 이상 학생:")
    for s in students:
        if s["math"] >= math_avg:
            print(f"  - {s['name']}: {s['math']}점")

    print("영어 평균 이상 학생:")
    for s in students:
        if s["english"] >= eng_avg:
            print(f"  - {s['name']}: {s['english']}점")

process_scores(students)
print()
print("-> 컨텍스트를 제공하면 목적에 맞는 코드가 생성됨!")
