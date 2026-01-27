"""
예제 15-02: 텍스트 파일 쓰기
쓰기 모드(w)와 추가 모드(a)의 차이를 알아봅니다.
"""
import tempfile
import os

temp_dir = tempfile.mkdtemp()
file_path = os.path.join(temp_dir, "output.txt")

# --- 쓰기 모드 (w): 새로 작성 ---
print("=" * 50)
print("1단계: 쓰기 모드(w)로 파일 생성")
print("=" * 50)
with open(file_path, "w", encoding="utf-8") as f:
    f.write("첫 번째 줄을 작성합니다.\n")
    f.write("두 번째 줄을 작성합니다.\n")
    f.write("세 번째 줄을 작성합니다.\n")

with open(file_path, "r", encoding="utf-8") as f:
    print("[현재 파일 내용]")
    print(f.read())

# --- 쓰기 모드 (w): 기존 내용 덮어쓰기 ---
print("=" * 50)
print("2단계: 쓰기 모드(w)로 다시 열면 기존 내용이 사라집니다")
print("=" * 50)
with open(file_path, "w", encoding="utf-8") as f:
    f.write("완전히 새로운 내용으로 교체되었습니다.\n")

with open(file_path, "r", encoding="utf-8") as f:
    print("[현재 파일 내용]")
    print(f.read())

# --- 추가 모드 (a): 기존 내용 뒤에 추가 ---
print("=" * 50)
print("3단계: 추가 모드(a)로 내용 덧붙이기")
print("=" * 50)
with open(file_path, "a", encoding="utf-8") as f:
    f.write("추가된 첫 번째 줄입니다.\n")
    f.write("추가된 두 번째 줄입니다.\n")

with open(file_path, "r", encoding="utf-8") as f:
    print("[현재 파일 내용]")
    print(f.read())

# --- writelines()로 여러 줄 한번에 쓰기 ---
print("=" * 50)
print("4단계: writelines()로 리스트 한번에 쓰기")
print("=" * 50)
lines = ["가\n", "나\n", "다\n", "라\n", "마\n"]
with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

with open(file_path, "r", encoding="utf-8") as f:
    print("[현재 파일 내용]")
    print(f.read())

# --- 모드 요약 ---
print("=" * 50)
print("파일 열기 모드 요약")
print("=" * 50)
modes = [
    ("r", "읽기 전용 (파일이 없으면 오류)"),
    ("w", "쓰기 전용 (파일이 없으면 생성, 있으면 덮어쓰기)"),
    ("a", "추가 전용 (파일이 없으면 생성, 있으면 끝에 추가)"),
    ("r+", "읽기+쓰기 (파일이 없으면 오류)"),
    ("w+", "쓰기+읽기 (파일이 없으면 생성, 있으면 덮어쓰기)"),
    ("a+", "추가+읽기 (파일이 없으면 생성, 있으면 끝에 추가)"),
]
for mode, desc in modes:
    print(f"  '{mode}' : {desc}")

# 정리
os.remove(file_path)
os.rmdir(temp_dir)
print()
print("파일 쓰기 예제를 성공적으로 완료했습니다!")
