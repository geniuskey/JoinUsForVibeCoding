#!/usr/bin/env python3
"""
예제 24-03: 자동 포맷팅 설정
- ast 모듈로 코드 구조 분석
- textwrap으로 코드 포맷팅
- Python 코드의 자동 정리 및 포맷팅 도구
"""

import ast
import textwrap
import re
from io import StringIO


# ============================================================
# 1. 코드 구조 분석기
# ============================================================

class CodeAnalyzer:
    """AST를 사용하여 Python 코드의 구조를 분석"""

    def __init__(self, source: str):
        self.source = source
        self.tree = ast.parse(source)
        self.lines = source.split("\n")

    def get_structure(self) -> dict:
        """코드의 전체 구조를 딕셔너리로 반환"""
        structure = {
            "imports": [],
            "constants": [],
            "classes": [],
            "functions": [],
            "global_code": [],
        }

        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                structure["imports"].append(self._describe_import(node))
            elif isinstance(node, ast.ClassDef):
                structure["classes"].append(self._describe_class(node))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                structure["functions"].append(self._describe_function(node))
            elif isinstance(node, ast.Assign):
                # 대문자 변수는 상수로 분류
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        structure["constants"].append(target.id)
                    else:
                        structure["global_code"].append(f"줄 {node.lineno}")
            elif isinstance(node, (ast.Expr, ast.If)):
                structure["global_code"].append(f"줄 {node.lineno}")

        return structure

    def _describe_import(self, node) -> str:
        """import 문을 문자열로 설명"""
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
            return f"import {', '.join(names)}"
        elif isinstance(node, ast.ImportFrom):
            names = [alias.name for alias in node.names]
            return f"from {node.module} import {', '.join(names)}"
        return ""

    def _describe_class(self, node: ast.ClassDef) -> dict:
        """클래스 정보를 딕셔너리로 반환"""
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(item.name)
        return {
            "이름": node.name,
            "줄": node.lineno,
            "메서드": methods,
            "docstring": ast.get_docstring(node) or "(없음)",
        }

    def _describe_function(self, node) -> dict:
        """함수 정보를 딕셔너리로 반환"""
        args = [arg.arg for arg in node.args.args]
        return {
            "이름": node.name,
            "줄": node.lineno,
            "매개변수": args,
            "docstring": ast.get_docstring(node) or "(없음)",
        }


# ============================================================
# 2. 코드 포맷터
# ============================================================

class CodeFormatter:
    """Python 코드를 자동으로 포맷팅하는 도구"""

    def __init__(self):
        # 포맷팅 설정
        self.indent_size = 4
        self.max_line_length = 79
        self.blank_lines_after_import = 2
        self.blank_lines_between_functions = 2
        self.blank_lines_between_methods = 1

    def format_source(self, source: str) -> str:
        """소스 코드 전체를 포맷팅"""
        lines = source.split("\n")
        formatted_lines = []

        for i, line in enumerate(lines):
            # 후행 공백 제거
            line = line.rstrip()

            # 탭을 스페이스로 변환
            line = line.expandtabs(self.indent_size)

            formatted_lines.append(line)

        result = "\n".join(formatted_lines)

        # 연속 빈 줄을 최대 2줄로 제한
        result = re.sub(r'\n{4,}', '\n\n\n', result)

        # 파일 끝에 빈 줄 하나 보장
        result = result.rstrip() + "\n"

        return result

    def format_imports(self, source: str) -> str:
        """import 문을 정리 (표준 라이브러리 / 서드파티 / 로컬 순서)"""
        tree = ast.parse(source)
        lines = source.split("\n")

        import_lines = []
        other_lines = []
        import_end = 0

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_end = max(import_end, node.end_lineno or node.lineno)
                # import 문 원본 추출
                start = node.lineno - 1
                end = (node.end_lineno or node.lineno)
                import_text = "\n".join(lines[start:end])
                import_lines.append(import_text)

        # import 문을 알파벳 순으로 정렬
        stdlib_imports = []
        from_imports = []

        for imp in import_lines:
            if imp.startswith("from"):
                from_imports.append(imp)
            else:
                stdlib_imports.append(imp)

        stdlib_imports.sort()
        from_imports.sort()

        # 나머지 코드
        remaining = "\n".join(lines[import_end:]).lstrip("\n")

        # 재조합
        parts = []
        if stdlib_imports:
            parts.append("\n".join(stdlib_imports))
        if from_imports:
            parts.append("\n".join(from_imports))

        result = "\n\n".join(parts)
        if remaining:
            result += "\n\n\n" + remaining

        return result

    def check_formatting(self, source: str) -> list:
        """포맷팅 문제를 검사하여 목록으로 반환"""
        issues = []
        lines = source.split("\n")

        for i, line in enumerate(lines, 1):
            # 후행 공백 검사
            if line != line.rstrip():
                issues.append(f"줄 {i}: 후행 공백 발견")

            # 탭 사용 검사
            if "\t" in line:
                issues.append(f"줄 {i}: 탭 문자 사용 (스페이스 권장)")

            # 줄 길이 검사
            if len(line) > self.max_line_length:
                issues.append(
                    f"줄 {i}: 줄 길이 {len(line)}자 "
                    f"(최대 {self.max_line_length}자 초과)"
                )

            # 연산자 주위 공백 검사 (간단 버전)
            if re.search(r'[^\s=!<>]=(?!=)', line) and not line.strip().startswith('#'):
                # 문자열 리터럴 내부 제외하기 위한 간단한 필터
                stripped = re.sub(r'["\'].*?["\']', '""', line)
                if re.search(r'[a-zA-Z0-9]=[a-zA-Z0-9]', stripped):
                    # 키워드 인자는 제외
                    if not re.search(r'\(.*=.*\)', stripped):
                        issues.append(f"줄 {i}: '=' 주위에 공백 필요")

        return issues


# ============================================================
# 3. 포맷팅 보고서 생성
# ============================================================

def generate_format_report(source: str, filename: str = "<입력>"):
    """코드 분석 및 포맷팅 보고서 생성"""
    analyzer = CodeAnalyzer(source)
    formatter = CodeFormatter()

    print(f"\n{'=' * 60}")
    print(f"  코드 구조 분석 보고서: {filename}")
    print(f"{'=' * 60}")

    # 구조 분석
    structure = analyzer.get_structure()

    print(f"\n  [코드 구조]")
    print(f"  - Import 문: {len(structure['imports'])}개")
    for imp in structure["imports"]:
        print(f"    - {imp}")

    print(f"  - 상수: {len(structure['constants'])}개")
    for const in structure["constants"]:
        print(f"    - {const}")

    print(f"  - 클래스: {len(structure['classes'])}개")
    for cls in structure["classes"]:
        print(f"    - {cls['이름']} (메서드: {', '.join(cls['메서드'])})")

    print(f"  - 함수: {len(structure['functions'])}개")
    for func in structure["functions"]:
        params = ", ".join(func["매개변수"])
        print(f"    - {func['이름']}({params})")

    # 포맷팅 검사
    issues = formatter.check_formatting(source)
    print(f"\n  [포맷팅 검사 결과]")
    if issues:
        print(f"  발견된 문제: {len(issues)}건")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print(f"  포맷팅 문제 없음!")

    return structure, issues


# ============================================================
# 메인: 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  예제 24-03: 자동 포맷팅 설정 도구")
    print("=" * 60)

    # 포맷팅 문제가 있는 샘플 코드
    messy_code = textwrap.dedent('''\
\tfrom os import path
\timport sys
\timport json
\tfrom collections import OrderedDict
\timport os

\tMAX_SIZE = 100
\tDEFAULT_NAME = "기본"

\tclass DataProcessor:
\t\tdef __init__(self, data):
\t\t\tself.data=data
\t\t\tself.result = None

\t\tdef process(self):
\t\t\tfor item in self.data:
\t\t\t\tself.result = item * 2
\t\t\treturn self.result

\tdef helper_function(x, y):
\t\treturn x+y

\tdef another_function():
\t\tprint("이것은 매우 매우 매우 매우 매우 매우 매우 매우 매우 긴 줄로 작성된 코드입니다. 이렇게 길면 안됩니다.")
    ''')

    # 1. 코드 구조 분석 및 포맷팅 검사
    structure, issues = generate_format_report(messy_code, "messy_example.py")

    # 2. 자동 포맷팅 적용
    formatter = CodeFormatter()

    print(f"\n{'=' * 60}")
    print(f"  자동 포맷팅 적용")
    print(f"{'=' * 60}")

    formatted = formatter.format_source(messy_code)
    print("\n  [포맷팅 후 코드]")
    print("  " + "-" * 40)
    for i, line in enumerate(formatted.split("\n"), 1):
        print(f"  {i:3d} | {line}")

    # 3. Import 정렬
    print(f"\n{'=' * 60}")
    print(f"  Import 정렬 데모")
    print(f"{'=' * 60}")

    import_code = textwrap.dedent('''\
        from collections import OrderedDict
        import sys
        import json
        import os
        from os import path
    ''')

    sorted_imports = formatter.format_imports(import_code)
    print("\n  [정렬 전]")
    for line in import_code.strip().split("\n"):
        print(f"    {line}")
    print("\n  [정렬 후]")
    for line in sorted_imports.strip().split("\n"):
        print(f"    {line}")

    # 4. 포맷팅 설정 요약
    print(f"\n{'=' * 60}")
    print(f"  포맷팅 설정 요약")
    print(f"{'=' * 60}")
    print(f"  - 들여쓰기: 스페이스 {formatter.indent_size}칸")
    print(f"  - 최대 줄 길이: {formatter.max_line_length}자")
    print(f"  - import 후 빈 줄: {formatter.blank_lines_after_import}줄")
    print(f"  - 함수 간 빈 줄: {formatter.blank_lines_between_functions}줄")
    print(f"  - 메서드 간 빈 줄: {formatter.blank_lines_between_methods}줄")

    print(f"\n모범 사례: 프로젝트 시작 시 포맷팅 규칙을 설정하고")
    print(f"자동 포맷팅 도구를 통해 일관된 코드 스타일을 유지하세요!")
