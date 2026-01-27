"""
예제 15-01: 텍스트 파일 읽기
다양한 방법으로 텍스트 파일을 읽는 방법을 배웁니다.
"""
import tempfile
import os

# --- 샘플 데이터 생성 ---
sample_text = """안녕하세요, 바이브 코딩!
파이썬으로 파일을 다루는 법을 배워봅시다.
첫 번째 줄입니다.
두 번째 줄입니다.
세 번째 줄입니다.
파일 처리는 프로그래밍의 기본입니다."""

temp_dir = tempfile.mkdtemp()
file_path = os.path.join(temp_dir, "sample.txt")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(sample_text)

print("=" * 50)
print("방법 1: read() - 전체 내용을 한 번에 읽기")
print("=" * 50)
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

print()
print("=" * 50)
print("방법 2: readline() - 한 줄씩 읽기")
print("=" * 50)
with open(file_path, "r", encoding="utf-8") as f:
    line = f.readline()
    line_num = 1
    while line:
        print(f"[{line_num}줄] {line}", end="")
        line = f.readline()
        line_num += 1
    print()  # 마지막 줄바꿈

print()
print("=" * 50)
print("방법 3: readlines() - 모든 줄을 리스트로 읽기")
print("=" * 50)
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    print(f"총 {len(lines)}줄이 있습니다.")
    for i, line in enumerate(lines):
        print(f"  lines[{i}] = {line.strip()!r}")

print()
print("=" * 50)
print("방법 4: for 루프로 한 줄씩 읽기 (권장)")
print("=" * 50)
with open(file_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        print(f"  {i}: {line.strip()}")

# 정리
os.remove(file_path)
os.rmdir(temp_dir)
print()
print("모든 읽기 방법을 성공적으로 실행했습니다!")
