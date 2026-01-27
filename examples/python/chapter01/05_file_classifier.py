# examples/python/chapter01/05_file_classifier.py
# 예제 5-2: 10분 만에 만드는 유틸리티
# 프롬프트: "폴더 안의 파일들을 확장자별로 분류해서 보여주는 프로그램을 만들어줘"

import os
import sys
from collections import Counter

def classify_files(directory):
    """지정된 디렉토리의 파일들을 확장자별로 분류합니다."""

    if not os.path.isdir(directory):
        print(f"오류: '{directory}'는 유효한 디렉토리가 아닙니다.")
        return

    # 확장자별 파일 수 세기
    extensions = Counter()
    total_files = 0

    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isfile(full_path):
            total_files += 1
            _, ext = os.path.splitext(item)
            if ext:
                extensions[ext.lower()] += 1
            else:
                extensions["(확장자 없음)"] += 1

    # 결과 출력
    print(f"\n{'=' * 45}")
    print(f"  폴더: {os.path.abspath(directory)}")
    print(f"  총 파일 수: {total_files}개")
    print(f"{'=' * 45}")

    if total_files == 0:
        print("  파일이 없습니다.")
        return

    print(f"\n  {'확장자':<15} {'파일 수':>8}  {'비율':>6}")
    print(f"  {'-' * 35}")

    # 파일 수 기준 내림차순 정렬
    for ext, count in extensions.most_common():
        ratio = count / total_files * 100
        bar = "#" * int(ratio / 5)  # 간단한 막대 그래프
        print(f"  {ext:<15} {count:>5}개   {ratio:>5.1f}%  {bar}")

    print()

# 실행
if __name__ == "__main__":
    # 인자가 있으면 해당 디렉토리, 없으면 현재 디렉토리
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    classify_files(target)
