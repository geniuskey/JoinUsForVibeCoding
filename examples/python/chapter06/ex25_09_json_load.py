"""
예제 25-09: JSON 로드 기능
- JSON 파일에서 할일 데이터를 불러옵니다.
- 파일이 없거나 손상된 경우의 에러 처리를 포함합니다.
- 버전 호환성 검사 및 데이터 유효성 검증을 수행합니다.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Todo:
    id: int
    title: str
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: str | None = None
    due_date: str | None = None
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """딕셔너리로 변환합니다."""
        data = asdict(self)
        data["priority"] = self.priority.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """딕셔너리에서 Todo 객체를 생성합니다."""
        # priority 문자열을 Enum으로 변환
        data = data.copy()  # 원본 딕셔너리를 수정하지 않음
        data["priority"] = Priority(data.get("priority", "medium"))
        return cls(**data)

    def __str__(self) -> str:
        status = "[완료]" if self.completed else "[미완료]"
        return f"#{self.id} {status} {self.title}"


class LoadError:
    """로드 에러 정보를 담는 클래스"""
    def __init__(self, error_type: str, message: str) -> None:
        self.error_type = error_type
        self.message = message

    def __str__(self) -> str:
        return f"[{self.error_type}] {self.message}"


class TodoStorage:
    """할일 데이터를 JSON 파일에서 불러오는 클래스"""

    SUPPORTED_VERSIONS = ["1.0"]

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save(self, todos: list[Todo]) -> None:
        """할일 목록을 JSON 파일로 저장합니다."""
        data = {
            "metadata": {
                "version": "1.0",
                "saved_at": datetime.now().isoformat(),
                "total_count": len(todos),
                "completed_count": sum(1 for t in todos if t.completed),
                "app": "CLI 할일 관리 앱",
            },
            "todos": [todo.to_dict() for todo in todos],
        }
        dir_path = os.path.dirname(self.file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self) -> tuple[list[Todo], list[LoadError]]:
        """
        JSON 파일에서 할일 목록을 불러옵니다.

        Returns:
            (할일 목록, 에러 목록) 튜플
            - 에러가 있어도 가능한 데이터는 최대한 복원합니다.
        """
        errors: list[LoadError] = []
        todos: list[Todo] = []

        # 1. 파일 존재 여부 확인
        if not os.path.exists(self.file_path):
            errors.append(LoadError(
                "FILE_NOT_FOUND",
                f"파일을 찾을 수 없습니다: {self.file_path}"
            ))
            return todos, errors

        # 2. 파일 읽기
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()
        except PermissionError:
            errors.append(LoadError(
                "PERMISSION_ERROR",
                f"파일 읽기 권한이 없습니다: {self.file_path}"
            ))
            return todos, errors
        except OSError as e:
            errors.append(LoadError(
                "IO_ERROR",
                f"파일 읽기 오류: {e}"
            ))
            return todos, errors

        # 3. JSON 파싱
        try:
            data = json.loads(raw_content)
        except json.JSONDecodeError as e:
            errors.append(LoadError(
                "JSON_PARSE_ERROR",
                f"JSON 파싱 실패 (줄 {e.lineno}, 열 {e.colno}): {e.msg}"
            ))
            return todos, errors

        # 4. 데이터 구조 검증
        if not isinstance(data, dict):
            errors.append(LoadError(
                "INVALID_STRUCTURE",
                "최상위 데이터가 딕셔너리가 아닙니다."
            ))
            return todos, errors

        # 5. 버전 검사
        metadata = data.get("metadata", {})
        version = metadata.get("version", "unknown")
        if version not in self.SUPPORTED_VERSIONS:
            errors.append(LoadError(
                "VERSION_MISMATCH",
                f"지원하지 않는 버전입니다: {version} "
                f"(지원 버전: {', '.join(self.SUPPORTED_VERSIONS)})"
            ))
            # 버전이 다르더라도 최대한 로드 시도

        # 6. 할일 데이터 로드
        todo_list = data.get("todos", [])
        if not isinstance(todo_list, list):
            errors.append(LoadError(
                "INVALID_TODOS",
                "'todos' 필드가 리스트가 아닙니다."
            ))
            return todos, errors

        # 7. 각 할일 항목 변환
        for i, item in enumerate(todo_list):
            try:
                if not isinstance(item, dict):
                    errors.append(LoadError(
                        "INVALID_ITEM",
                        f"항목 {i+1}: 딕셔너리가 아닙니다 (건너뜀)"
                    ))
                    continue

                # 필수 필드 확인
                if "id" not in item or "title" not in item:
                    errors.append(LoadError(
                        "MISSING_FIELD",
                        f"항목 {i+1}: 필수 필드(id, title) 누락 (건너뜀)"
                    ))
                    continue

                todo = Todo.from_dict(item)
                todos.append(todo)

            except (ValueError, TypeError) as e:
                errors.append(LoadError(
                    "CONVERSION_ERROR",
                    f"항목 {i+1}: 변환 실패 - {e} (건너뜀)"
                ))

        return todos, errors

    def load_metadata(self) -> dict | None:
        """메타데이터만 불러옵니다 (빠른 조회용)."""
        if not os.path.exists(self.file_path):
            return None

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("metadata", {})
        except (json.JSONDecodeError, OSError):
            return None


def create_demo_json(file_path: str, scenario: str = "normal") -> None:
    """데모용 JSON 파일을 생성합니다."""
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    if scenario == "normal":
        # 정상적인 JSON 파일
        storage = TodoStorage(file_path)
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        todos = [
            Todo(id=1, title="우유 사기", priority=Priority.LOW,
                 completed=True, completed_at=datetime.now().isoformat(),
                 tags=["장보기"]),
            Todo(id=2, title="보고서 작성", priority=Priority.HIGH,
                 due_date=tomorrow, tags=["업무"]),
            Todo(id=3, title="운동하기", priority=Priority.MEDIUM,
                 tags=["건강"]),
        ]
        storage.save(todos)

    elif scenario == "corrupted":
        # 손상된 JSON 파일
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('{"metadata": {"version": "1.0"}, "todos": [{"id": 1, INVALID')

    elif scenario == "partial":
        # 일부 항목이 잘못된 JSON 파일
        data = {
            "metadata": {"version": "1.0", "saved_at": datetime.now().isoformat()},
            "todos": [
                {"id": 1, "title": "정상 항목", "priority": "medium", "completed": False,
                 "created_at": datetime.now().isoformat(), "completed_at": None,
                 "due_date": None, "tags": []},
                {"id": 2},  # title 누락
                "잘못된 형식",  # 딕셔너리가 아님
                {"id": 4, "title": "복구된 항목", "priority": "high", "completed": False,
                 "created_at": datetime.now().isoformat(), "completed_at": None,
                 "due_date": None, "tags": ["복구"]},
            ],
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print("=" * 55)
    print("CLI 할일 관리 앱 - JSON 로드 기능 데모")
    print("=" * 55)
    print()

    base_dir = "/tmp/todo-cli-load-demo"

    # 1. 정상 파일 로드
    print("--- 1. 정상 JSON 파일 로드 ---")
    normal_path = os.path.join(base_dir, "normal.json")
    create_demo_json(normal_path, "normal")

    storage = TodoStorage(normal_path)

    # 메타데이터 먼저 확인
    meta = storage.load_metadata()
    if meta:
        print(f"  메타데이터:")
        print(f"    버전: {meta.get('version', 'N/A')}")
        print(f"    저장 시각: {meta.get('saved_at', 'N/A')}")
        print(f"    전체 항목: {meta.get('total_count', 'N/A')}개")

    todos, errors = storage.load()
    print(f"  로드 결과: {len(todos)}개 할일, {len(errors)}개 에러")
    for todo in todos:
        print(f"    {todo}")
    print()

    # 2. 존재하지 않는 파일 로드
    print("--- 2. 존재하지 않는 파일 로드 ---")
    missing_storage = TodoStorage(os.path.join(base_dir, "nonexistent.json"))
    todos, errors = missing_storage.load()
    print(f"  로드 결과: {len(todos)}개 할일, {len(errors)}개 에러")
    for err in errors:
        print(f"    {err}")
    print()

    # 3. 손상된 파일 로드
    print("--- 3. 손상된 JSON 파일 로드 ---")
    corrupted_path = os.path.join(base_dir, "corrupted.json")
    create_demo_json(corrupted_path, "corrupted")

    corrupted_storage = TodoStorage(corrupted_path)
    todos, errors = corrupted_storage.load()
    print(f"  로드 결과: {len(todos)}개 할일, {len(errors)}개 에러")
    for err in errors:
        print(f"    {err}")
    print()

    # 4. 부분 손상 파일 로드 (최대한 복구)
    print("--- 4. 부분 손상 파일 로드 (최대한 복구) ---")
    partial_path = os.path.join(base_dir, "partial.json")
    create_demo_json(partial_path, "partial")

    partial_storage = TodoStorage(partial_path)
    todos, errors = partial_storage.load()
    print(f"  로드 결과: {len(todos)}개 할일 복구, {len(errors)}개 에러")
    print(f"  복구된 할일:")
    for todo in todos:
        print(f"    {todo}")
    print(f"  발생한 에러:")
    for err in errors:
        print(f"    {err}")
    print()

    # 5. 저장 후 다시 로드 (왕복 테스트)
    print("--- 5. 저장 후 로드 왕복 테스트 ---")
    roundtrip_path = os.path.join(base_dir, "roundtrip.json")
    roundtrip_storage = TodoStorage(roundtrip_path)

    original_todos = [
        Todo(id=1, title="왕복 테스트 1", priority=Priority.HIGH, tags=["테스트"]),
        Todo(id=2, title="왕복 테스트 2", priority=Priority.LOW, completed=True,
             completed_at=datetime.now().isoformat()),
    ]
    roundtrip_storage.save(original_todos)

    loaded_todos, errors = roundtrip_storage.load()
    print(f"  원본 항목 수: {len(original_todos)}")
    print(f"  로드 항목 수: {len(loaded_todos)}")

    # 데이터 일치 확인
    all_match = True
    for orig, loaded in zip(original_todos, loaded_todos):
        if orig.id != loaded.id or orig.title != loaded.title:
            all_match = False
            break
    print(f"  데이터 일치: {'예' if all_match else '아니오'}")
    print()

    # 정리
    import shutil
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
        print(f"임시 디렉토리 정리 완료: {base_dir}")
