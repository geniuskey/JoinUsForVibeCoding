# examples/python/chapter01/ex01_03_file_reader.py
# 바이브 코딩으로 만든 파일 읽기 프로그램
# AI에게 "텍스트 파일을 읽어서 줄 수와 단어 수를 알려주는 프로그램을 만들어줘"라고 요청

import os

def analyze_file(filepath):
    """파일을 읽어 기본 통계를 출력합니다."""
    if not os.path.exists(filepath):
        print(f"파일을 찾을 수 없습니다: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    words = content.split()
    chars = len(content)

    print(f"=== 파일 분석 결과 ===")
    print(f"파일명: {filepath}")
    print(f"줄 수: {len(lines)}줄")
    print(f"단어 수: {len(words)}개")
    print(f"글자 수: {chars}자")

# 데모용: 임시 파일을 생성하고 분석합니다
demo_text = """바이브 코딩은 새로운 프로그래밍 방식입니다.
AI에게 원하는 것을 말하면 코드가 생성됩니다.
누구나 프로그래밍을 할 수 있는 시대가 왔습니다."""

demo_path = "demo_sample.txt"
with open(demo_path, 'w', encoding='utf-8') as f:
    f.write(demo_text)

analyze_file(demo_path)

# 데모 파일 정리
os.remove(demo_path)
print("\n(데모 파일이 정리되었습니다)")
