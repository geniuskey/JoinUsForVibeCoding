#!/usr/bin/env python3
"""
예제 24-05: docstring 작성 도구
- ast 모듈로 함수/클래스의 docstring 존재 여부를 검사
- docstring이 없는 경우 자동 템플릿 생성
- Google 스타일 docstring 형식 적용
"""

import ast
import textwrap
from dataclasses import dataclass, field


# ============================================================
# 1. 코드 요소 정보 추출
# ============================================================

@dataclass
class FunctionInfo:
    """함수/메서드 정보"""
    name: str
    lineno: int
    args: list = field(default_factory=list)       # 매개변수 이름 목록
    arg_types: dict = field(default_factory=dict)   # 매개변수 타입 힌트
    return_type: str = ""                           # 반환 타입 힌트
    has_docstring: bool = False
    existing_docstring: str = ""
    has_return: bool = False                        # return 문 존재 여부
    raises: list = field(default_factory=list)      # raise되는 예외 목록
    is_method: bool = False
    decorators: list = field(default_factory=list)


@dataclass
class ClassInfo:
    """클래스 정보"""
    name: str
    lineno: int
    has_docstring: bool = False
    existing_docstring: str = ""
    bases: list = field(default_factory=list)       # 상속 클래스
    methods: list = field(default_factory=list)     # 메서드 정보 리스트


# ============================================================
# 2. Docstring 검사기
# ============================================================

class DocstringInspector(ast.NodeVisitor):
    """AST를 순회하며 docstring 정보를 수집"""

    def __init__(self, source: str):
        self.source = source
        self.functions: list[FunctionInfo] = []
        self.classes: list[ClassInfo] = []
        self._current_class = None

    def inspect(self):
        """소스 코드를 분석하여 모든 함수/클래스 정보 수집"""
        tree = ast.parse(self.source)
        self.visit(tree)
        return self

    def visit_ClassDef(self, node: ast.ClassDef):
        """클래스 정의 방문"""
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(f"{ast.dump(base)}")

        cls_info = ClassInfo(
            name=node.name,
            lineno=node.lineno,
            has_docstring=ast.get_docstring(node) is not None,
            existing_docstring=ast.get_docstring(node) or "",
            bases=bases,
        )

        # 클래스 내부의 메서드 처리
        prev_class = self._current_class
        self._current_class = cls_info

        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._process_function(item, is_method=True)

        self._current_class = prev_class
        self.classes.append(cls_info)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """최상위 함수 정의 방문"""
        self._process_function(node, is_method=False)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """최상위 비동기 함수 정의 방문"""
        self._process_function(node, is_method=False)

    def _process_function(self, node, is_method: bool):
        """함수/메서드 정보 추출"""
        # 매개변수 추출 (self/cls 제외)
        args = []
        arg_types = {}
        for arg in node.args.args:
            if arg.arg in ("self", "cls"):
                continue
            args.append(arg.arg)
            # 타입 어노테이션 추출
            if arg.annotation:
                arg_types[arg.arg] = self._get_annotation_str(arg.annotation)

        # 반환 타입 추출
        return_type = ""
        if node.returns:
            return_type = self._get_annotation_str(node.returns)

        # return 문 존재 여부
        has_return = any(
            isinstance(n, ast.Return) and n.value is not None
            for n in ast.walk(node)
        )

        # raise되는 예외 추출
        raises = []
        for n in ast.walk(node):
            if isinstance(n, ast.Raise) and n.exc:
                if isinstance(n.exc, ast.Call):
                    if isinstance(n.exc.func, ast.Name):
                        raises.append(n.exc.func.id)
                elif isinstance(n.exc, ast.Name):
                    raises.append(n.exc.id)

        # 데코레이터 추출
        decorators = []
        for dec in node.decorator_list:
            if isinstance(dec, ast.Name):
                decorators.append(dec.id)
            elif isinstance(dec, ast.Attribute):
                decorators.append(f"{dec.attr}")

        func_info = FunctionInfo(
            name=node.name,
            lineno=node.lineno,
            args=args,
            arg_types=arg_types,
            return_type=return_type,
            has_docstring=ast.get_docstring(node) is not None,
            existing_docstring=ast.get_docstring(node) or "",
            has_return=has_return,
            raises=list(set(raises)),
            is_method=is_method,
            decorators=decorators,
        )

        self.functions.append(func_info)
        if self._current_class is not None:
            self._current_class.methods.append(func_info)

    def _get_annotation_str(self, annotation) -> str:
        """타입 어노테이션을 문자열로 변환"""
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Constant):
            return str(annotation.value)
        elif isinstance(annotation, ast.Attribute):
            return annotation.attr
        elif isinstance(annotation, ast.Subscript):
            if isinstance(annotation.value, ast.Name):
                return f"{annotation.value.id}[...]"
        return "Any"


# ============================================================
# 3. Docstring 템플릿 생성기
# ============================================================

class DocstringGenerator:
    """Google 스타일 docstring 템플릿 생성기"""

    def generate_function_docstring(self, func: FunctionInfo) -> str:
        """함수/메서드용 docstring 생성"""
        parts = []

        # 요약 줄
        if func.is_method and func.name == "__init__":
            parts.append(f'    """{func.name.strip("_")} 초기화')
        elif func.name.startswith("_"):
            parts.append(f'    """내부 헬퍼: {func.name.lstrip("_")} 처리')
        else:
            parts.append(f'    """{func.name}에 대한 설명을 작성하세요')

        # Args 섹션
        if func.args:
            parts.append("")
            parts.append("    Args:")
            for arg in func.args:
                type_hint = func.arg_types.get(arg, "")
                type_str = f" ({type_hint})" if type_hint else ""
                parts.append(f"        {arg}{type_str}: {arg}에 대한 설명")

        # Returns 섹션
        if func.has_return:
            parts.append("")
            parts.append("    Returns:")
            if func.return_type:
                parts.append(f"        {func.return_type}: 반환값에 대한 설명")
            else:
                parts.append("        반환값에 대한 설명")

        # Raises 섹션
        if func.raises:
            parts.append("")
            parts.append("    Raises:")
            for exc in func.raises:
                parts.append(f"        {exc}: 예외 발생 조건 설명")

        parts.append('    """')
        return "\n".join(parts)

    def generate_class_docstring(self, cls: ClassInfo) -> str:
        """클래스용 docstring 생성"""
        parts = []

        # 요약 줄
        parts.append(f'    """{cls.name}에 대한 설명을 작성하세요')

        # 상속 정보
        if cls.bases:
            parts.append("")
            parts.append(f"    상속: {', '.join(cls.bases)}")

        # Attributes 섹션 (메서드에서 self.xxx를 추출)
        init_method = None
        for m in cls.methods:
            if m.name == "__init__":
                init_method = m
                break

        if init_method and init_method.args:
            parts.append("")
            parts.append("    Attributes:")
            for arg in init_method.args:
                type_hint = init_method.arg_types.get(arg, "")
                type_str = f" ({type_hint})" if type_hint else ""
                parts.append(f"        {arg}{type_str}: {arg}에 대한 설명")

        parts.append('    """')
        return "\n".join(parts)


# ============================================================
# 4. Docstring 검사 보고서
# ============================================================

def analyze_docstrings(source: str, filename: str = "<입력>"):
    """소스 코드의 docstring 상태를 분석하고 보고서 출력"""
    inspector = DocstringInspector(source)
    inspector.inspect()
    generator = DocstringGenerator()

    print(f"\n{'=' * 60}")
    print(f"  Docstring 분석 보고서: {filename}")
    print(f"{'=' * 60}")

    # 통계
    total_funcs = len(inspector.functions)
    funcs_with_doc = sum(1 for f in inspector.functions if f.has_docstring)
    total_classes = len(inspector.classes)
    classes_with_doc = sum(1 for c in inspector.classes if c.has_docstring)

    print(f"\n  [통계]")
    print(f"  - 함수/메서드: {funcs_with_doc}/{total_funcs}개 docstring 있음")
    print(f"  - 클래스: {classes_with_doc}/{total_classes}개 docstring 있음")

    if total_funcs > 0:
        coverage = (funcs_with_doc + classes_with_doc) / (total_funcs + total_classes) * 100
        print(f"  - docstring 커버리지: {coverage:.1f}%")

    # docstring이 없는 항목 나열
    missing = []
    for func in inspector.functions:
        if not func.has_docstring:
            kind = "메서드" if func.is_method else "함수"
            missing.append((kind, func.name, func.lineno))

    for cls in inspector.classes:
        if not cls.has_docstring:
            missing.append(("클래스", cls.name, cls.lineno))

    if missing:
        print(f"\n  [docstring 누락 항목] ({len(missing)}건)")
        for kind, name, line in missing:
            print(f"    - {kind} '{name}' (줄 {line})")

    # 자동 생성 템플릿 제시
    print(f"\n  [자동 생성 docstring 템플릿]")
    print(f"  {'─' * 50}")

    generated_any = False

    for cls in inspector.classes:
        if not cls.has_docstring:
            generated_any = True
            print(f"\n  클래스 '{cls.name}' (줄 {cls.lineno}):")
            print(generator.generate_class_docstring(cls))

    for func in inspector.functions:
        if not func.has_docstring:
            generated_any = True
            kind = "메서드" if func.is_method else "함수"
            print(f"\n  {kind} '{func.name}' (줄 {func.lineno}):")
            print(generator.generate_function_docstring(func))

    if not generated_any:
        print("  모든 항목에 docstring이 있습니다!")

    print(f"\n{'=' * 60}")


# ============================================================
# 메인: 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  예제 24-05: Docstring 검사 및 자동 생성 도구")
    print("=" * 60)

    # docstring이 일부 누락된 샘플 코드
    sample_code = textwrap.dedent('''\
        class UserManager:
            """사용자 관리 클래스"""

            def __init__(self, db_path: str, max_users: int = 100):
                """UserManager 초기화"""
                self.db_path = db_path
                self.max_users = max_users
                self.users = []

            def add_user(self, name: str, email: str) -> bool:
                if len(self.users) >= self.max_users:
                    raise OverflowError("최대 사용자 수 초과")
                self.users.append({"name": name, "email": email})
                return True

            def find_user(self, name: str) -> dict:
                for user in self.users:
                    if user["name"] == name:
                        return user
                raise KeyError(f"사용자 '{name}'을 찾을 수 없습니다")

            def _validate_email(self, email: str) -> bool:
                return "@" in email and "." in email

        class ReportGenerator:
            def __init__(self, data: list):
                self.data = data

            def generate_summary(self) -> str:
                total = len(self.data)
                return f"총 {total}건의 데이터"

            def export_csv(self, filepath: str) -> None:
                raise NotImplementedError("아직 구현되지 않았습니다")

        def calculate_statistics(numbers: list) -> dict:
            if not numbers:
                raise ValueError("빈 리스트입니다")
            return {
                "count": len(numbers),
                "sum": sum(numbers),
                "average": sum(numbers) / len(numbers),
                "min": min(numbers),
                "max": max(numbers),
            }

        def format_currency(amount: float, currency: str = "KRW") -> str:
            """금액을 통화 형식으로 포맷팅"""
            if currency == "KRW":
                return f"{amount:,.0f}원"
            return f"${amount:,.2f}"
    ''')

    analyze_docstrings(sample_code, "user_manager.py")

    # 모든 docstring이 있는 코드 검사
    print("\n")

    good_code = textwrap.dedent('''\
        class Calculator:
            """기본 산술 연산을 수행하는 계산기 클래스"""

            def add(self, a: float, b: float) -> float:
                """두 수를 더합니다"""
                return a + b

            def divide(self, a: float, b: float) -> float:
                """두 수를 나눕니다"""
                if b == 0:
                    raise ZeroDivisionError("0으로 나눌 수 없습니다")
                return a / b
    ''')

    analyze_docstrings(good_code, "calculator.py")

    print("\n모범 사례: 모든 공개 함수와 클래스에 docstring을 작성하면")
    print("코드의 가독성과 유지보수성이 크게 향상됩니다!")
