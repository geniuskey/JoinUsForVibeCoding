#!/usr/bin/env python3
"""
예제 24-02: 코드 리뷰 체크리스트
- 자동 코드 품질 체크 도구
- ast 모듈과 정규식을 사용하여 Python 코드의 품질을 자동으로 검사
"""

import ast
import re
import textwrap
from dataclasses import dataclass, field
from enum import Enum


# ============================================================
# 1. 체크 결과 등급 정의
# ============================================================

class Severity(Enum):
    """검사 결과의 심각도"""
    INFO = "정보"
    WARNING = "경고"
    ERROR = "오류"


@dataclass
class CheckResult:
    """개별 검사 결과"""
    rule: str           # 규칙 이름
    severity: Severity  # 심각도
    message: str        # 메시지
    line: int = 0       # 관련 줄 번호 (0이면 전체)

    def __str__(self):
        loc = f" (줄 {self.line})" if self.line > 0 else ""
        return f"  [{self.severity.value}] {self.rule}: {self.message}{loc}"


@dataclass
class ReviewReport:
    """전체 리뷰 보고서"""
    filename: str
    results: list = field(default_factory=list)

    def add(self, result: CheckResult):
        self.results.append(result)

    @property
    def error_count(self):
        return sum(1 for r in self.results if r.severity == Severity.ERROR)

    @property
    def warning_count(self):
        return sum(1 for r in self.results if r.severity == Severity.WARNING)

    @property
    def info_count(self):
        return sum(1 for r in self.results if r.severity == Severity.INFO)

    @property
    def passed(self):
        return self.error_count == 0

    def summary(self) -> str:
        total = len(self.results)
        status = "통과" if self.passed else "실패"
        return (
            f"검사 결과: {status} | "
            f"총 {total}건 (오류: {self.error_count}, "
            f"경고: {self.warning_count}, 정보: {self.info_count})"
        )


# ============================================================
# 2. 코드 리뷰 체크 규칙들
# ============================================================

class CodeReviewChecker:
    """코드 리뷰 체크리스트를 실행하는 검사기"""

    def __init__(self, source_code: str, filename: str = "<입력>"):
        self.source = source_code
        self.lines = source_code.split("\n")
        self.filename = filename
        self.report = ReviewReport(filename=filename)
        self._tree = None

    def _parse_ast(self) -> bool:
        """소스 코드를 AST로 파싱"""
        try:
            self._tree = ast.parse(self.source)
            return True
        except SyntaxError as e:
            self.report.add(CheckResult(
                rule="구문 검사",
                severity=Severity.ERROR,
                message=f"구문 오류: {e.msg}",
                line=e.lineno or 0,
            ))
            return False

    def check_function_length(self, max_lines: int = 30):
        """함수 길이 검사: 너무 긴 함수는 분리 권장"""
        if not self._tree:
            return
        for node in ast.walk(self._tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # 함수의 시작 줄과 끝 줄 계산
                end_line = max(
                    getattr(child, 'end_lineno', node.lineno)
                    for child in ast.walk(node)
                    if hasattr(child, 'end_lineno')
                )
                length = end_line - node.lineno + 1
                if length > max_lines:
                    self.report.add(CheckResult(
                        rule="함수 길이",
                        severity=Severity.WARNING,
                        message=f"함수 '{node.name}'이(가) {length}줄로 너무 깁니다 "
                                f"(최대 {max_lines}줄 권장)",
                        line=node.lineno,
                    ))
                else:
                    self.report.add(CheckResult(
                        rule="함수 길이",
                        severity=Severity.INFO,
                        message=f"함수 '{node.name}': {length}줄 (적절)",
                        line=node.lineno,
                    ))

    def check_function_args(self, max_args: int = 5):
        """함수 매개변수 수 검사: 너무 많은 매개변수는 리팩토링 권장"""
        if not self._tree:
            return
        for node in ast.walk(self._tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = node.args
                # self/cls 제외한 매개변수 수
                total = len(args.args)
                if total > 0 and args.args[0].arg in ("self", "cls"):
                    total -= 1
                if total > max_args:
                    self.report.add(CheckResult(
                        rule="매개변수 수",
                        severity=Severity.WARNING,
                        message=f"함수 '{node.name}'의 매개변수가 {total}개로 "
                                f"너무 많습니다 (최대 {max_args}개 권장)",
                        line=node.lineno,
                    ))

    def check_docstrings(self):
        """docstring 존재 여부 검사"""
        if not self._tree:
            return
        for node in ast.walk(self._tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                if not docstring:
                    self.report.add(CheckResult(
                        rule="docstring",
                        severity=Severity.WARNING,
                        message=f"'{node.name}'에 docstring이 없습니다",
                        line=node.lineno,
                    ))

    def check_naming_convention(self):
        """네이밍 컨벤션 검사 (PEP 8 기반)"""
        if not self._tree:
            return
        for node in ast.walk(self._tree):
            # 함수명: snake_case 검사
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith("_") and not re.match(
                    r'^[a-z_][a-z0-9_]*$', node.name
                ):
                    self.report.add(CheckResult(
                        rule="네이밍 컨벤션",
                        severity=Severity.WARNING,
                        message=f"함수 '{node.name}'이(가) snake_case가 아닙니다",
                        line=node.lineno,
                    ))
            # 클래스명: PascalCase 검사
            elif isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    self.report.add(CheckResult(
                        rule="네이밍 컨벤션",
                        severity=Severity.WARNING,
                        message=f"클래스 '{node.name}'이(가) PascalCase가 아닙니다",
                        line=node.lineno,
                    ))

    def check_bare_except(self):
        """맨(bare) except 사용 검사"""
        if not self._tree:
            return
        for node in ast.walk(self._tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    self.report.add(CheckResult(
                        rule="예외 처리",
                        severity=Severity.ERROR,
                        message="맨(bare) except 사용 금지 - "
                                "구체적인 예외 타입을 명시하세요",
                        line=node.lineno,
                    ))

    def check_line_length(self, max_length: int = 100):
        """줄 길이 검사"""
        for i, line in enumerate(self.lines, 1):
            if len(line) > max_length:
                self.report.add(CheckResult(
                    rule="줄 길이",
                    severity=Severity.INFO,
                    message=f"줄 길이가 {len(line)}자로 "
                            f"최대 {max_length}자를 초과합니다",
                    line=i,
                ))

    def check_todo_comments(self):
        """TODO/FIXME 주석 검사"""
        pattern = re.compile(r'#\s*(TODO|FIXME|HACK|XXX)\b', re.IGNORECASE)
        for i, line in enumerate(self.lines, 1):
            match = pattern.search(line)
            if match:
                tag = match.group(1).upper()
                self.report.add(CheckResult(
                    rule="미완료 태그",
                    severity=Severity.INFO,
                    message=f"{tag} 주석이 발견되었습니다: {line.strip()}",
                    line=i,
                ))

    def run_all_checks(self) -> ReviewReport:
        """모든 검사 항목 실행"""
        if not self._parse_ast():
            return self.report

        self.check_function_length()
        self.check_function_args()
        self.check_docstrings()
        self.check_naming_convention()
        self.check_bare_except()
        self.check_line_length()
        self.check_todo_comments()

        return self.report


# ============================================================
# 3. 리뷰 보고서 출력
# ============================================================

def print_report(report: ReviewReport):
    """리뷰 보고서를 보기 좋게 출력"""
    print(f"\n{'=' * 60}")
    print(f"  코드 리뷰 보고서: {report.filename}")
    print(f"{'=' * 60}")

    if not report.results:
        print("  모든 검사를 통과했습니다!")
    else:
        # 심각도별 그룹핑
        for severity in [Severity.ERROR, Severity.WARNING, Severity.INFO]:
            items = [r for r in report.results if r.severity == severity]
            if items:
                print(f"\n  --- {severity.value} ({len(items)}건) ---")
                for item in items:
                    print(str(item))

    print(f"\n{'─' * 60}")
    print(f"  {report.summary()}")
    print(f"{'=' * 60}")


# ============================================================
# 메인: 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  예제 24-02: 코드 리뷰 체크리스트 자동 검사")
    print("=" * 60)

    # 검사할 샘플 코드 (의도적으로 여러 문제를 포함)
    sample_code = textwrap.dedent('''\
        # TODO: 이 코드 리팩토링 필요

        class user_data:
            def __init__(self, name, email, age, address, phone, company, role):
                self.name = name
                self.email = email
                self.age = age
                self.address = address
                self.phone = phone
                self.company = company
                self.role = role

            def processData(self, data):
                try:
                    result = data["value"] * 2
                    return result
                except:
                    return None

            def validate(self):
                if self.age < 0:
                    return False
                if "@" not in self.email:
                    return False
                return True

        def CalculateScore(items):
            total = 0
            for item in items:
                total += item
            avg = total / len(items)
            return avg
    ''')

    # 코드 리뷰 실행
    checker = CodeReviewChecker(sample_code, filename="sample_module.py")
    report = checker.run_all_checks()
    print_report(report)

    # 양호한 코드 예시
    print("\n\n")
    good_code = textwrap.dedent('''\
        class UserProfile:
            """사용자 프로필 정보를 관리하는 클래스"""

            def __init__(self, name: str, email: str):
                """사용자 프로필 초기화"""
                self.name = name
                self.email = email

            def validate_email(self) -> bool:
                """이메일 형식 검증"""
                return "@" in self.email and "." in self.email

        def calculate_average(numbers: list) -> float:
            """숫자 리스트의 평균을 계산"""
            if not numbers:
                raise ValueError("빈 리스트는 처리할 수 없습니다")
            return sum(numbers) / len(numbers)
    ''')

    checker2 = CodeReviewChecker(good_code, filename="good_module.py")
    report2 = checker2.run_all_checks()
    print_report(report2)

    print("\n모범 사례: 코드 리뷰 체크리스트를 자동화하면")
    print("일관된 코드 품질을 유지할 수 있습니다!")
