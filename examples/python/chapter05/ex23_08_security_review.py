"""
예제 23-08: AI에게 보안 검토 요청 - 보안 체크리스트 자동화
- 코드의 보안 취약점을 자동으로 검사하는 체크리스트
- AI에게 보안 검토를 요청할 때 사용할 프롬프트 템플릿

이 예제는 교육 목적으로 보안 검토 자동화 방법을 보여줍니다.
"""

import ast
import os
import re
import textwrap
from pathlib import Path


# ============================================================
# ✅ 보안 체크리스트 자동 검사기
# ============================================================

class SecurityChecker:
    """
    ✅ Python 소스 코드의 보안 취약점을 검사하는 도구

    검사 항목:
    1. 하드코딩된 비밀 정보
    2. 안전하지 않은 함수 사용
    3. SQL 인젝션 위험
    4. 명령어 인젝션 위험
    5. 안전하지 않은 역직렬화
    6. 디버그 모드 설정
    """

    def __init__(self):
        self.findings = []

    def check_source(self, source_code: str, filename: str = "<code>") -> list:
        """소스 코드를 검사하고 발견 사항을 반환"""
        self.findings = []

        lines = source_code.split('\n')

        self._check_hardcoded_secrets(lines, filename)
        self._check_unsafe_functions(lines, filename)
        self._check_sql_injection(lines, filename)
        self._check_command_injection(lines, filename)
        self._check_unsafe_deserialization(lines, filename)
        self._check_debug_settings(lines, filename)
        self._check_weak_crypto(lines, filename)
        self._check_insecure_random(lines, filename)

        return self.findings

    def _add_finding(self, severity: str, category: str,
                     message: str, filename: str, line_num: int,
                     line_content: str, recommendation: str):
        """검사 결과 추가"""
        self.findings.append({
            "severity": severity,       # HIGH, MEDIUM, LOW
            "category": category,
            "message": message,
            "filename": filename,
            "line": line_num,
            "code": line_content.strip(),
            "recommendation": recommendation,
        })

    def _check_hardcoded_secrets(self, lines, filename):
        """하드코딩된 비밀 정보 검사"""
        secret_patterns = [
            (r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']',
             "하드코딩된 비밀번호"),
            (r'(?i)(api[_-]?key|apikey)\s*=\s*["\'][^"\']+["\']',
             "하드코딩된 API 키"),
            (r'(?i)(secret[_-]?key|jwt[_-]?secret)\s*=\s*["\'][^"\']+["\']',
             "하드코딩된 시크릿 키"),
            (r'(?i)(token)\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
             "하드코딩된 토큰"),
        ]

        for line_num, line in enumerate(lines, 1):
            # 주석이나 docstring 내부는 건너뛰기
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                continue

            for pattern, description in secret_patterns:
                if re.search(pattern, line):
                    self._add_finding(
                        "HIGH", "비밀 정보 하드코딩",
                        description,
                        filename, line_num, line,
                        "환경 변수(os.environ)를 사용하세요"
                    )

    def _check_unsafe_functions(self, lines, filename):
        """안전하지 않은 함수 사용 검사"""
        unsafe_functions = [
            (r'\beval\s*\(', "eval() 사용",
             "ast.literal_eval()을 사용하거나 eval()을 제거하세요"),
            (r'\bexec\s*\(', "exec() 사용",
             "exec()은 임의 코드 실행이 가능합니다. 제거하세요"),
            (r'\b__import__\s*\(', "__import__() 사용",
             "importlib.import_module()을 사용하세요"),
            (r'\binput\s*\(.*\)', "input() 사용",
             "입력값을 반드시 검증한 후 사용하세요"),
        ]

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#'):
                continue

            for pattern, description, recommendation in unsafe_functions:
                if re.search(pattern, line):
                    self._add_finding(
                        "MEDIUM", "안전하지 않은 함수",
                        description,
                        filename, line_num, line,
                        recommendation
                    )

    def _check_sql_injection(self, lines, filename):
        """SQL 인젝션 위험 검사"""
        sql_patterns = [
            r'(?i)execute\s*\(\s*f["\']',          # f-string SQL
            r'(?i)execute\s*\(\s*["\'].*%\s',       # % 포맷팅 SQL
            r'(?i)execute\s*\(\s*.*\.format\(',     # .format() SQL
            r'(?i)execute\s*\(\s*.*\+\s',           # 문자열 연결 SQL
        ]

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#'):
                continue

            for pattern in sql_patterns:
                if re.search(pattern, line):
                    self._add_finding(
                        "HIGH", "SQL 인젝션",
                        "SQL 쿼리에 문자열 포맷팅 사용",
                        filename, line_num, line,
                        "파라미터화 쿼리(?)를 사용하세요"
                    )
                    break

    def _check_command_injection(self, lines, filename):
        """명령어 인젝션 위험 검사"""
        cmd_patterns = [
            (r'os\.system\s*\(', "os.system() 사용",
             "subprocess.run()을 리스트 인자와 함께 사용하세요"),
            (r'subprocess\..*shell\s*=\s*True', "shell=True 사용",
             "shell=False(기본값)와 리스트 인자를 사용하세요"),
            (r'os\.popen\s*\(', "os.popen() 사용",
             "subprocess.run()을 사용하세요"),
        ]

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#'):
                continue

            for pattern, description, recommendation in cmd_patterns:
                if re.search(pattern, line):
                    self._add_finding(
                        "HIGH", "명령어 인젝션",
                        description,
                        filename, line_num, line,
                        recommendation
                    )

    def _check_unsafe_deserialization(self, lines, filename):
        """안전하지 않은 역직렬화 검사"""
        patterns = [
            (r'pickle\.loads?\s*\(', "pickle 역직렬화",
             "신뢰할 수 없는 데이터에 pickle을 사용하지 마세요. JSON을 사용하세요"),
            (r'yaml\.load\s*\((?!.*Loader)', "안전하지 않은 YAML 로드",
             "yaml.safe_load()를 사용하세요"),
        ]

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#'):
                continue

            for pattern, description, recommendation in patterns:
                if re.search(pattern, line):
                    self._add_finding(
                        "HIGH", "안전하지 않은 역직렬화",
                        description,
                        filename, line_num, line,
                        recommendation
                    )

    def _check_debug_settings(self, lines, filename):
        """디버그/개발 설정 검사"""
        patterns = [
            (r'(?i)debug\s*=\s*True', "디버그 모드 활성화",
             "운영 환경에서는 DEBUG=False로 설정하세요"),
            (r'(?i)verify\s*=\s*False', "SSL 검증 비활성화",
             "SSL 인증서 검증을 활성화하세요"),
        ]

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#'):
                continue

            for pattern, description, recommendation in patterns:
                if re.search(pattern, line):
                    self._add_finding(
                        "MEDIUM", "안전하지 않은 설정",
                        description,
                        filename, line_num, line,
                        recommendation
                    )

    def _check_weak_crypto(self, lines, filename):
        """취약한 암호화 사용 검사"""
        patterns = [
            (r'hashlib\.md5\s*\(', "MD5 해시 사용",
             "SHA-256 이상을 사용하세요. 비밀번호에는 PBKDF2를 사용하세요"),
            (r'hashlib\.sha1\s*\(', "SHA-1 해시 사용",
             "SHA-256 이상을 사용하세요"),
        ]

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#'):
                continue

            for pattern, description, recommendation in patterns:
                if re.search(pattern, line):
                    self._add_finding(
                        "MEDIUM", "취약한 암호화",
                        description,
                        filename, line_num, line,
                        recommendation
                    )

    def _check_insecure_random(self, lines, filename):
        """안전하지 않은 난수 생성 검사"""
        # 보안 컨텍스트에서 random 사용 확인
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#'):
                continue

            if re.search(r'random\.(choice|randint|random|randrange|sample)\s*\(', line):
                # 보안 관련 키워드와 함께 사용되는지 확인
                context_keywords = ['token', 'key', 'secret', 'password',
                                    'session', 'nonce', 'salt']
                nearby_text = ' '.join(
                    lines[max(0, line_num - 3):line_num + 1]
                ).lower()

                if any(kw in nearby_text for kw in context_keywords):
                    self._add_finding(
                        "HIGH", "안전하지 않은 난수",
                        "보안 컨텍스트에서 random 모듈 사용",
                        filename, line_num, line,
                        "secrets 모듈을 사용하세요"
                    )

    def generate_report(self) -> str:
        """검사 결과 보고서 생성"""
        if not self.findings:
            return "보안 검사 완료: 발견된 문제가 없습니다!"

        report_lines = []
        report_lines.append(f"보안 검사 결과: {len(self.findings)}개 문제 발견")
        report_lines.append("=" * 50)

        # 심각도별 분류
        by_severity = {"HIGH": [], "MEDIUM": [], "LOW": []}
        for f in self.findings:
            by_severity[f["severity"]].append(f)

        severity_labels = {
            "HIGH": "높음 (즉시 수정 필요)",
            "MEDIUM": "중간 (수정 권장)",
            "LOW": "낮음 (검토 권장)"
        }

        for severity in ["HIGH", "MEDIUM", "LOW"]:
            items = by_severity[severity]
            if not items:
                continue

            label = severity_labels[severity]
            report_lines.append(f"\n[{severity}] {label} - {len(items)}건")
            report_lines.append("-" * 40)

            for i, f in enumerate(items, 1):
                report_lines.append(
                    f"  {i}. [{f['category']}] {f['message']}")
                report_lines.append(
                    f"     파일: {f['filename']}:{f['line']}")
                report_lines.append(
                    f"     코드: {f['code']}")
                report_lines.append(
                    f"     권장: {f['recommendation']}")

        return '\n'.join(report_lines)


# ============================================================
# ✅ AI 보안 검토 프롬프트 템플릿
# ============================================================

def get_security_review_prompt(code: str) -> str:
    """
    ✅ AI에게 보안 검토를 요청할 때 사용할 프롬프트 생성
    """
    return textwrap.dedent(f"""
    다음 Python 코드의 보안을 검토해주세요.

    검토 항목:
    1. 입력 검증: 모든 외부 입력이 적절히 검증되는지
    2. SQL 인젝션: 파라미터화 쿼리를 사용하는지
    3. 명령어 인젝션: subprocess가 안전하게 사용되는지
    4. 경로 순회: 파일 경로가 안전하게 처리되는지
    5. 비밀 관리: 하드코딩된 비밀 정보가 없는지
    6. 암호화: 안전한 해시/암호화 알고리즘을 사용하는지
    7. 인증/권한: 적절한 접근 제어가 있는지
    8. 에러 처리: 민감한 정보가 에러 메시지에 노출되지 않는지
    9. 로깅: 비밀 정보가 로그에 기록되지 않는지
    10. 의존성: 알려진 취약점이 있는 라이브러리를 사용하지 않는지

    각 문제에 대해:
    - 위치 (줄 번호)
    - 위험 수준 (높음/중간/낮음)
    - 문제 설명
    - 수정 방법 (코드 포함)
    을 제공해주세요.

    코드:
    ```python
    {code}
    ```
    """).strip()


# ============================================================
# 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("예제 23-08: 보안 체크리스트 자동화")
    print("=" * 60)

    # 테스트용 취약한 코드
    vulnerable_code = '''
import os
import sqlite3
import hashlib
import random
import pickle

# 하드코딩된 비밀 정보
DB_PASSWORD = "SuperSecret123"
API_KEY = "sk-1234567890abcdef"

# 안전하지 않은 함수
user_input = input("이름을 입력하세요: ")
result = eval(user_input)

# SQL 인젝션
conn = sqlite3.connect("app.db")
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

# 명령어 인젝션
os.system(f"echo {user_input}")
import subprocess
subprocess.run(f"ls {user_input}", shell=True)

# 취약한 암호화
password_hash = hashlib.md5(b"password").hexdigest()
weak_hash = hashlib.sha1(b"data").hexdigest()

# 안전하지 않은 난수 (보안 토큰 생성)
token = ''.join(random.choice('abc123') for _ in range(32))

# 안전하지 않은 역직렬화
data = pickle.loads(user_data)

# 디버그 모드
DEBUG = True
'''

    # 보안 검사 실행
    print("\n--- 보안 검사 대상 코드 (취약한 예시) ---")
    for i, line in enumerate(vulnerable_code.strip().split('\n'), 1):
        print(f"  {i:3d} | {line}")

    print("\n--- 자동 보안 검사 실행 ---")
    checker = SecurityChecker()
    checker.check_source(vulnerable_code, "vulnerable_app.py")

    report = checker.generate_report()
    print(report)

    # 통계
    print(f"\n--- 검사 통계 ---")
    total = len(checker.findings)
    high = sum(1 for f in checker.findings if f["severity"] == "HIGH")
    medium = sum(1 for f in checker.findings if f["severity"] == "MEDIUM")
    low = sum(1 for f in checker.findings if f["severity"] == "LOW")
    print(f"  총 발견 건수: {total}")
    print(f"  높음(HIGH): {high}건")
    print(f"  중간(MEDIUM): {medium}건")
    print(f"  낮음(LOW): {low}건")

    # AI 보안 검토 프롬프트 예시
    print("\n\n--- AI 보안 검토 프롬프트 예시 ---")
    sample_code = '''
def login(username, password):
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE name='{username}'"
    result = conn.execute(query).fetchone()
    if result and result[2] == hashlib.md5(password.encode()).hexdigest():
        return {"token": ''.join(random.choice('abc') for _ in range(16))}
    return None
'''
    prompt = get_security_review_prompt(sample_code.strip())
    print(prompt[:600] + "...\n")

    print("\n" + "=" * 60)
    print("핵심 원칙:")
    print("  1. 코드 작성 후 보안 체크리스트를 반드시 확인하세요")
    print("  2. AI에게 보안 검토를 요청할 때 구체적인 항목을 명시하세요")
    print("  3. 자동 검사 도구를 CI/CD 파이프라인에 포함하세요")
    print("  4. 보안은 개발 마지막이 아닌 처음부터 고려하세요")
    print("")
    print("바이브 코딩 팁: AI에게 '이 코드의 보안 취약점을 찾아서")
    print("              수정 방법과 함께 알려줘'라고 요청하세요.")
    print("=" * 60)
