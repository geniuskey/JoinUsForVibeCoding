#!/usr/bin/env python3
"""
예제 24-04: 린터 체크
- ast 모듈을 활용한 간단한 코드 스타일 검사기 구현
- PEP 8 및 일반적인 코딩 규칙을 기반으로 한 린터
"""

import ast
import re
import textwrap
from dataclasses import dataclass, field


# ============================================================
# 1. 린트 규칙 정의
# ============================================================

@dataclass
class LintMessage:
    """린트 검사 결과 메시지"""
    code: str         # 규칙 코드 (예: E001)
    line: int         # 줄 번호
    column: int       # 열 번호
    message: str      # 설명 메시지
    category: str     # 카테고리

    def __str__(self):
        return f"  {self.code} (줄 {self.line}, 열 {self.column}): {self.message}"


# ============================================================
# 2. AST 기반 린터 검사 규칙들
# ============================================================

class ASTLintChecker(ast.NodeVisitor):
    """AST를 순회하며 코드 스타일을 검사하는 린터"""

    def __init__(self, source: str):
        self.source = source
        self.lines = source.split("\n")
        self.messages: list[LintMessage] = []

    def add_message(self, code: str, line: int, col: int,
                    message: str, category: str):
        """린트 메시지 추가"""
        self.messages.append(LintMessage(
            code=code, line=line, column=col,
            message=message, category=category
        ))

    # --- 네이밍 규칙 검사 ---

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """함수 정의 검사"""
        # N001: 함수명은 snake_case
        if not re.match(r'^_*[a-z][a-z0-9_]*$', node.name):
            # 매직 메서드(__xxx__)는 예외
            if not (node.name.startswith("__") and node.name.endswith("__")):
                self.add_message(
                    "N001", node.lineno, node.col_offset,
                    f"함수 '{node.name}'은(는) snake_case로 작성해야 합니다",
                    "네이밍"
                )

        # C001: 함수 복잡도 검사 (중첩 깊이)
        self._check_nesting_depth(node, max_depth=4)

        # D001: return 문이 없는 함수 검사 (None만 반환하는 경우 제외)
        has_return = any(
            isinstance(n, ast.Return) and n.value is not None
            for n in ast.walk(node)
        )
        # __init__이나 setter 등은 제외
        if not has_return and not node.name.startswith("__"):
            # 함수 본문이 pass만 있는 경우도 제외
            if not (len(node.body) == 1 and isinstance(node.body[0], ast.Pass)):
                self.add_message(
                    "D001", node.lineno, node.col_offset,
                    f"함수 '{node.name}'에 return 값이 없습니다 "
                    f"(의도적이면 무시)",
                    "설계"
                )

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """클래스 정의 검사"""
        # N002: 클래스명은 PascalCase
        if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
            self.add_message(
                "N002", node.lineno, node.col_offset,
                f"클래스 '{node.name}'은(는) PascalCase로 작성해야 합니다",
                "네이밍"
            )

        # S001: 빈 클래스 검사
        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self.add_message(
                "S001", node.lineno, node.col_offset,
                f"클래스 '{node.name}'이(가) 비어 있습니다 (pass만 존재)",
                "구조"
            )

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        """변수 할당 검사"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                name = target.id
                # N003: 상수는 UPPER_CASE
                # (모듈 최상위 레벨의 대문자 시작 변수)
                if hasattr(node, '_parent_is_module') and name[0].isupper():
                    if not re.match(r'^[A-Z][A-Z0-9_]*$', name):
                        self.add_message(
                            "N003", node.lineno, node.col_offset,
                            f"상수 '{name}'은(는) UPPER_CASE로 "
                            f"작성해야 합니다",
                            "네이밍"
                        )

        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        """예외 처리 검사"""
        # E001: bare except 금지
        if node.type is None:
            self.add_message(
                "E001", node.lineno, node.col_offset,
                "맨(bare) except 사용 금지 - 구체적인 예외 타입을 명시하세요",
                "예외 처리"
            )
        # E002: 너무 넓은 예외 처리
        elif isinstance(node.type, ast.Name) and node.type.id == "Exception":
            self.add_message(
                "E002", node.lineno, node.col_offset,
                "너무 넓은 예외 처리 (Exception) - "
                "구체적인 예외 타입 사용을 권장합니다",
                "예외 처리"
            )

        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare):
        """비교 연산 검사"""
        # C002: None과의 비교는 is/is not 사용
        for op, comparator in zip(node.ops, node.comparators):
            if isinstance(comparator, ast.Constant) and comparator.value is None:
                if isinstance(op, (ast.Eq, ast.NotEq)):
                    self.add_message(
                        "C002", node.lineno, node.col_offset,
                        "None 비교에는 == 대신 'is' 또는 'is not'을 사용하세요",
                        "코딩 스타일"
                    )

        self.generic_visit(node)

    def visit_Global(self, node: ast.Global):
        """global 문 검사"""
        # S002: global 사용 경고
        for name in node.names:
            self.add_message(
                "S002", node.lineno, node.col_offset,
                f"global 변수 '{name}' 사용 - "
                f"함수 매개변수나 클래스 사용을 권장합니다",
                "구조"
            )

        self.generic_visit(node)

    def _check_nesting_depth(self, node, max_depth: int, current_depth: int = 0):
        """코드 중첩 깊이 검사"""
        nesting_nodes = (
            ast.If, ast.For, ast.While, ast.With,
            ast.Try, ast.ExceptHandler,
        )
        for child in ast.iter_child_nodes(node):
            if isinstance(child, nesting_nodes):
                new_depth = current_depth + 1
                if new_depth > max_depth:
                    self.add_message(
                        "C001", child.lineno, child.col_offset,
                        f"코드 중첩 깊이가 {new_depth}단계로 "
                        f"너무 깊습니다 (최대 {max_depth}단계 권장)",
                        "복잡도"
                    )
                self._check_nesting_depth(child, max_depth, new_depth)
            else:
                self._check_nesting_depth(child, max_depth, current_depth)


# ============================================================
# 3. 줄 단위 린터 검사
# ============================================================

class LineLintChecker:
    """줄 단위로 코드 스타일을 검사하는 린터"""

    def __init__(self, source: str):
        self.lines = source.split("\n")
        self.messages: list[LintMessage] = []

    def add_message(self, code: str, line: int, col: int,
                    message: str, category: str):
        self.messages.append(LintMessage(
            code=code, line=line, column=col,
            message=message, category=category
        ))

    def check_line_length(self, max_length: int = 79):
        """L001: 줄 길이 검사"""
        for i, line in enumerate(self.lines, 1):
            if len(line) > max_length:
                self.add_message(
                    "L001", i, max_length + 1,
                    f"줄 길이 {len(line)}자 (최대 {max_length}자 초과)",
                    "레이아웃"
                )

    def check_trailing_whitespace(self):
        """L002: 후행 공백 검사"""
        for i, line in enumerate(self.lines, 1):
            if line != line.rstrip() and line.strip():
                self.add_message(
                    "L002", i, len(line.rstrip()) + 1,
                    "후행 공백이 있습니다",
                    "레이아웃"
                )

    def check_tab_usage(self):
        """L003: 탭 사용 검사"""
        for i, line in enumerate(self.lines, 1):
            if "\t" in line:
                col = line.index("\t") + 1
                self.add_message(
                    "L003", i, col,
                    "탭 문자 사용 - 스페이스 4칸을 권장합니다",
                    "레이아웃"
                )

    def check_print_statements(self):
        """W001: print 문 검사 (디버깅용 print가 남아 있을 수 있음)"""
        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()
            # 주석이나 문자열 내부가 아닌 print 호출 탐지
            if stripped.startswith("print(") and not stripped.startswith("#"):
                self.add_message(
                    "W001", i, line.index("print") + 1,
                    "print() 문이 있습니다 - "
                    "디버깅용이라면 제거를 권장합니다",
                    "경고"
                )

    def check_magic_numbers(self):
        """W002: 매직 넘버 검사"""
        pattern = re.compile(r'(?<!=\s)\b(\d{2,})\b(?!\s*[:\])}])')
        skip_patterns = re.compile(r'(range|len|import|#|"""|\'\'\')')

        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()
            if skip_patterns.search(stripped):
                continue
            if stripped.startswith("#"):
                continue

            matches = pattern.findall(stripped)
            for num in matches:
                if int(num) not in (0, 1, 2, 10, 100):
                    self.add_message(
                        "W002", i, 1,
                        f"매직 넘버 '{num}' 발견 - 상수로 정의하는 것을 권장합니다",
                        "경고"
                    )

    def run_all(self):
        """모든 줄 단위 검사 실행"""
        self.check_line_length()
        self.check_trailing_whitespace()
        self.check_tab_usage()
        self.check_print_statements()
        self.check_magic_numbers()
        return self.messages


# ============================================================
# 4. 통합 린터
# ============================================================

class PythonLinter:
    """AST + 줄 단위 검사를 통합한 Python 린터"""

    def __init__(self, source: str, filename: str = "<입력>"):
        self.source = source
        self.filename = filename

    def run(self) -> list[LintMessage]:
        """모든 린트 검사 실행"""
        all_messages = []

        # 1. AST 기반 검사
        try:
            ast_checker = ASTLintChecker(self.source)
            tree = ast.parse(self.source)
            ast_checker.visit(tree)
            all_messages.extend(ast_checker.messages)
        except SyntaxError as e:
            all_messages.append(LintMessage(
                code="F001", line=e.lineno or 0, column=e.offset or 0,
                message=f"구문 오류: {e.msg}", category="치명적"
            ))
            return all_messages  # 구문 오류 시 추가 검사 불가

        # 2. 줄 단위 검사
        line_checker = LineLintChecker(self.source)
        line_checker.run_all()
        all_messages.extend(line_checker.messages)

        # 줄 번호 순으로 정렬
        all_messages.sort(key=lambda m: (m.line, m.column))
        return all_messages

    def print_report(self):
        """린트 결과를 보기 좋게 출력"""
        messages = self.run()

        print(f"\n{'=' * 60}")
        print(f"  린트 검사 결과: {self.filename}")
        print(f"{'=' * 60}")

        if not messages:
            print("\n  모든 검사를 통과했습니다! 깨끗한 코드입니다.")
        else:
            # 카테고리별 그룹핑
            categories = {}
            for msg in messages:
                categories.setdefault(msg.category, []).append(msg)

            for category, msgs in categories.items():
                print(f"\n  [{category}] ({len(msgs)}건)")
                for msg in msgs:
                    print(str(msg))

        total = len(messages)
        print(f"\n{'─' * 60}")
        print(f"  총 {total}건의 린트 메시지가 발견되었습니다.")

        # 규칙별 통계
        if messages:
            stats = {}
            for msg in messages:
                stats[msg.code] = stats.get(msg.code, 0) + 1
            print(f"\n  [규칙별 통계]")
            for code, count in sorted(stats.items()):
                print(f"    {code}: {count}건")

        print(f"{'=' * 60}")


# ============================================================
# 메인: 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  예제 24-04: 코드 린터 체크")
    print("=" * 60)

    # 문제가 있는 샘플 코드
    problematic_code = textwrap.dedent('''\
        import os
        import sys

        MAX_RETRY = 3

        class data_handler:
            """데이터 처리 클래스"""

            def __init__(self, data):
                self.data = data

            def ProcessData(self):
                result = []
                for item in self.data:
                    if item > 0:
                        if item < 1000:
                            if item % 2 == 0:
                                if item != 42:
                                    for i in range(365):
                                        result.append(item * i)
                return result

            def check_value(self, val):
                if val == None:
                    return False
                try:
                    return int(val) > 0
                except:
                    return False

        global_counter = 0

        def UpdateCounter():
            global global_counter
            global_counter += 1
            print(f"카운터: {global_counter}")
            return global_counter
    ''')

    # 린트 검사 실행
    linter = PythonLinter(problematic_code, "data_handler.py")
    linter.print_report()

    # 깨끗한 코드 검사
    print("\n\n")

    clean_code = textwrap.dedent('''\
        """깨끗한 코드 예시 모듈"""

        MAX_RETRY = 3
        DEFAULT_TIMEOUT = 30


        class DataHandler:
            """데이터를 안전하게 처리하는 클래스"""

            def __init__(self, data: list):
                """DataHandler 초기화"""
                self.data = data

            def process_data(self) -> list:
                """데이터를 필터링하고 처리"""
                return [
                    item * 2
                    for item in self.data
                    if self._is_valid(item)
                ]

            def _is_valid(self, item) -> bool:
                """항목의 유효성 검사"""
                return isinstance(item, (int, float)) and item > 0

        def calculate_average(numbers: list) -> float:
            """숫자 리스트의 평균을 계산"""
            if not numbers:
                raise ValueError("빈 리스트")
            return sum(numbers) / len(numbers)
    ''')

    linter2 = PythonLinter(clean_code, "clean_handler.py")
    linter2.print_report()

    print("\n모범 사례: 린터를 프로젝트에 통합하여")
    print("코드 품질을 자동으로 관리하세요!")
