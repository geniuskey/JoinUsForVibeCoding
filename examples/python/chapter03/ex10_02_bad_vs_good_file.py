"""
예제 10-2: 나쁜 프롬프트 vs 좋은 프롬프트 — 파일 처리
====================================================
나쁜 프롬프트: "파일 처리 해줘"
좋은 프롬프트: "텍스트 파일을 읽어 각 줄의 단어 수를 세고,
              총 단어 수와 줄별 통계를 출력하는 함수를 작성해줘.
              파일이 없으면 친절한 에러 메시지를 보여줘."
"""

import os
import tempfile

# --- 나쁜 프롬프트로 생성된 코드 ---
# 프롬프트: "파일 처리 해줘"

def bad_file_process(filename):
    """모호한 요청: 파일을 읽기만 함"""
    with open(filename) as f:
        return f.read()


# --- 좋은 프롬프트로 생성된 코드 ---
# 프롬프트: "텍스트 파일을 읽어 각 줄의 단어 수를 세고,
#           총 단어 수와 줄별 통계를 출력하는 함수를 작성해줘.
#           파일이 없으면 친절한 에러 메시지를 보여줘."

def analyze_text_file(filepath):
    """
    텍스트 파일의 줄별 단어 수를 분석합니다.

    Args:
        filepath: 분석할 텍스트 파일 경로
    Returns:
        dict: 줄별 단어 수와 총 단어 수가 담긴 딕셔너리
    """
    if not os.path.exists(filepath):
        print(f"[오류] 파일을 찾을 수 없습니다: {filepath}")
        print("  파일 경로를 확인해주세요.")
        return None

    stats = {"lines": [], "total_words": 0}

    with open(filepath, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            word_count = len(line.split())
            stats["lines"].append({
                "line_number": line_num,
                "word_count": word_count,
                "preview": line.strip()[:40]
            })
            stats["total_words"] += word_count

    # 결과 출력
    print(f"파일: {filepath}")
    print(f"{'줄 번호':>8} | {'단어 수':>7} | 내용 미리보기")
    print("-" * 55)
    for info in stats["lines"]:
        print(f"{info['line_number']:>8} | {info['word_count']:>7} | {info['preview']}")
    print("-" * 55)
    print(f"{'총 줄 수':>8} : {len(stats['lines'])}")
    print(f"{'총 단어 수':>8} : {stats['total_words']}")

    return stats


# ── 실행 ──
if __name__ == "__main__":
    # 임시 샘플 파일 생성
    sample_text = """바이브 코딩은 AI와 함께 프로그래밍하는 새로운 방식입니다.
프롬프트를 잘 작성하면 더 좋은 결과를 얻을 수 있습니다.
구체적이고 명확한 요청이 핵심입니다.
함께 배워봅시다!"""

    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                      delete=False, encoding="utf-8")
    tmp.write(sample_text)
    tmp.close()

    print("=" * 55)
    print("[나쁜 프롬프트 결과]")
    print(bad_file_process(tmp.name)[:60] + "...")
    print("→ 단순히 읽기만 함. 분석이나 에러 처리 없음\n")

    print("=" * 55)
    print("[좋은 프롬프트 결과]")
    analyze_text_file(tmp.name)

    print()
    print("=" * 55)
    print("[존재하지 않는 파일 처리]")
    analyze_text_file("없는파일.txt")

    os.unlink(tmp.name)
