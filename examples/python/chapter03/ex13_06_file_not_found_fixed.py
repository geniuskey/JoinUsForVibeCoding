"""
예제 13-6: FileNotFoundError — 잘못된 파일 경로 (수정 완료)
============================================================
수정: os.path.exists()로 파일 존재 확인 + try/except 예외 처리
"""

import os

filename = "학생명단.txt"

# 방법 1: os.path.exists()로 사전 확인
print("=== 방법 1: 파일 존재 여부 사전 확인 ===")
if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        print(f"파일 내용:\n{content}")
else:
    print(f"'{filename}' 파일을 찾을 수 없습니다.")
    print(f"현재 디렉토리: {os.getcwd()}")
    print(f"현재 디렉토리의 파일 목록:")
    for f in os.listdir("."):
        print(f"  - {f}")

# 방법 2: try/except로 예외 처리 (더 파이썬다운 방법!)
print("\n=== 방법 2: try/except 예외 처리 ===")
try:
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        print(f"파일 내용:\n{content}")
except FileNotFoundError:
    print(f"오류: '{filename}' 파일이 존재하지 않습니다.")
    print("해결 방법:")
    print("  1. 파일 이름이 정확한지 확인하세요.")
    print("  2. 파일이 올바른 디렉토리에 있는지 확인하세요.")
    print("  3. 파일 경로를 절대 경로로 지정해 보세요.")
except PermissionError:
    print(f"오류: '{filename}' 파일에 대한 읽기 권한이 없습니다.")
