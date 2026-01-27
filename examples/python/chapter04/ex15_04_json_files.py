"""
예제 15-04: JSON 파일 읽기/쓰기
json 모듈을 사용하여 JSON 파일을 다루는 방법을 배웁니다.
"""
import json
import tempfile
import os

temp_dir = tempfile.mkdtemp()

# --- JSON 파일 쓰기 ---
print("=" * 50)
print("1단계: JSON 파일 쓰기")
print("=" * 50)
json_path = os.path.join(temp_dir, "config.json")

config = {
    "앱_이름": "바이브 코딩 도우미",
    "버전": "2.1.0",
    "설정": {
        "테마": "다크",
        "언어": "한국어",
        "자동저장": True,
        "글꼴_크기": 14
    },
    "최근_파일": [
        "project_a.py",
        "project_b.py",
        "notes.md"
    ],
    "단축키": {
        "저장": "Ctrl+S",
        "실행": "F5",
        "검색": "Ctrl+F"
    }
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("config.json 파일이 생성되었습니다.")
print()

# --- JSON 파일 읽기 ---
print("=" * 50)
print("2단계: JSON 파일 읽기")
print("=" * 50)
with open(json_path, "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(f"  앱 이름: {loaded['앱_이름']}")
print(f"  버전: {loaded['버전']}")
print(f"  테마: {loaded['설정']['테마']}")
print(f"  언어: {loaded['설정']['언어']}")
print(f"  자동저장: {loaded['설정']['자동저장']}")
print(f"  최근 파일: {', '.join(loaded['최근_파일'])}")

# --- Python 객체를 JSON 문자열로 변환 ---
print()
print("=" * 50)
print("3단계: json.dumps()로 문자열 변환")
print("=" * 50)
user_data = {
    "이름": "김바이브",
    "나이": 25,
    "취미": ["코딩", "독서", "등산"],
    "개발자": True
}

# 보기 좋게 출력
json_str = json.dumps(user_data, ensure_ascii=False, indent=2)
print("포맷된 JSON:")
print(json_str)

# 한 줄로 출력
json_compact = json.dumps(user_data, ensure_ascii=False, separators=(",", ":"))
print(f"\n압축 JSON: {json_compact}")

# --- JSON 문자열을 Python 객체로 변환 ---
print()
print("=" * 50)
print("4단계: json.loads()로 문자열 파싱")
print("=" * 50)
json_input = '{"도시": "서울", "인구": 9700000, "수도": true}'
parsed = json.loads(json_input)
print(f"  원본 문자열: {json_input}")
print(f"  파싱 결과: {parsed}")
print(f"  도시: {parsed['도시']}, 인구: {parsed['인구']:,}명")

# --- 여러 레코드를 JSON 배열로 저장 ---
print()
print("=" * 50)
print("5단계: 리스트 데이터 JSON 저장 및 읽기")
print("=" * 50)
json_path2 = os.path.join(temp_dir, "tasks.json")

tasks = [
    {"id": 1, "제목": "파이썬 공부", "완료": True, "우선순위": "높음"},
    {"id": 2, "제목": "프로젝트 기획", "완료": False, "우선순위": "높음"},
    {"id": 3, "제목": "블로그 작성", "완료": False, "우선순위": "보통"},
    {"id": 4, "제목": "운동하기", "완료": True, "우선순위": "낮음"},
]

with open(json_path2, "w", encoding="utf-8") as f:
    json.dump(tasks, f, ensure_ascii=False, indent=2)

with open(json_path2, "r", encoding="utf-8") as f:
    loaded_tasks = json.load(f)

print(f"  총 {len(loaded_tasks)}개의 할 일:")
for task in loaded_tasks:
    status = "V" if task["완료"] else " "
    print(f"  [{status}] {task['제목']} (우선순위: {task['우선순위']})")

completed = sum(1 for t in loaded_tasks if t["완료"])
print(f"\n  완료: {completed}/{len(loaded_tasks)}")

# 정리
os.remove(json_path)
os.remove(json_path2)
os.rmdir(temp_dir)
print()
print("JSON 파일 처리 예제를 성공적으로 완료했습니다!")
