"""
예제 12-8: PEP8 스타일 적용 요청
==================================
PEP8 포맷팅 규칙을 적용하여 코드를 정리하는 예제입니다.

프롬프트: "이 코드를 PEP8 스타일로 포맷팅해줘"
→ 공백, 줄 바꿈, import 순서 등 PEP8 규칙을 일괄 적용합니다.
"""


# ====================================================================
# 개선 전: PEP8 위반이 가득한 코드
# ====================================================================
# (주석으로 위반 사항을 표시)

import json     # 표준 라이브러리
import os
import sys
import math

BEFORE_CODE = '''
import json,os,sys                         # ← import를 콤마로 묶음 (위반)
import math
MAX_RETRY=3                                # ← 연산자 주위 공백 없음 (위반)
default_timeout = 30;                      # ← 세미콜론 사용 (위반)
def connect_to_server( host,port,timeout=default_timeout ):  # ← 괄호 안 공백 (위반)
    url=f"http://{host}:{port}"            # ← 공백 없음 (위반)
    for i in range(MAX_RETRY) :            # ← 콜론 앞 공백 (위반)
        print(f"시도 {i+1}/{MAX_RETRY}...")
        if timeout>0 :                     # ← 연산자/콜론 공백 (위반)
            print( f"타임아웃: {timeout}초" )  # ← 괄호 안 공백 (위반)
            return {"url":url,"status":"connected","attempts":i+1}
    return {"url":url,"status":"failed","attempts":MAX_RETRY}
result=connect_to_server( "localhost",8080 )  # ← 여러 위반
print(json.dumps( result,indent=2,ensure_ascii=False ))
'''


# ====================================================================
# 개선 후: PEP8 규칙이 적용된 코드
# ====================================================================

MAX_RETRY = 3                                  # 상수: UPPER_SNAKE_CASE + 공백
DEFAULT_TIMEOUT = 30                           # 상수로 승격 + 세미콜론 제거


def connect_to_server(host, port, timeout=DEFAULT_TIMEOUT):
    """서버에 연결을 시도합니다."""               # docstring 추가
    url = f"http://{host}:{port}"              # 연산자 주위 공백
    for i in range(MAX_RETRY):                 # 콜론 앞 공백 없음
        print(f"시도 {i + 1}/{MAX_RETRY}...")  # 연산자 주위 공백
        if timeout > 0:                        # 연산자 주위 공백
            print(f"타임아웃: {timeout}초")     # 괄호 안 불필요한 공백 제거
            return {
                "url": url,                    # 딕셔너리 콜론 뒤 공백
                "status": "connected",
                "attempts": i + 1,
            }
    return {
        "url": url,
        "status": "failed",
        "attempts": MAX_RETRY,
    }


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 55)
    print("[예제 12-8] PEP8 스타일 적용 요청")
    print("=" * 55)

    print("\n[개선 전 코드]")
    print("-" * 55)
    for line in BEFORE_CODE.strip().split('\n'):
        print(f"  {line}")

    print()
    print("[개선 후 코드 실행 결과]")
    print("-" * 55)
    result = connect_to_server("localhost", 8080)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print()
    print("[PEP8 주요 포맷팅 규칙]")
    print("-" * 55)
    rules = [
        ("import 분리", "import json,os,sys", "import json\\nimport os\\nimport sys"),
        ("연산자 공백", "MAX_RETRY=3", "MAX_RETRY = 3"),
        ("세미콜론 금지", "timeout = 30;", "timeout = 30"),
        ("괄호 안 공백", "func( a, b )", "func(a, b)"),
        ("콜론 앞 공백", "if x > 0 :", "if x > 0:"),
        ("딕셔너리 공백", '{"key":"val"}', '{"key": "val"}'),
        ("줄 길이", "79자 이하 권장", "긴 줄은 괄호로 분리"),
    ]
    for i, (rule, wrong, correct) in enumerate(rules, 1):
        print(f"  {i}. {rule}")
        print(f"     잘못: {wrong}")
        print(f"     올바: {correct}")
        print()

    print("Tip: Python 프로젝트에서는 black, ruff 같은 자동 포맷터를")
    print("     사용하면 PEP8을 자동으로 적용할 수 있습니다.")
    print("     AI에게 'PEP8으로 포맷팅해줘'라고 요청하는 것도 좋은 방법입니다.")
