"""
예제 25-08: JSON 저장 기능
- 할일 데이터를 JSON 파일로 저장합니다.
- 사람이 읽기 쉬운 포맷으로 저장합니다 (들여쓰기, 한글 유지).
- 저장 시 메타데이터(저장 시각, 버전 등)도 함께 기록합니다.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path


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
        """딕셔너리로 변환합니다 (JSON 저장용)."""
        data = asdict(self)
        data["priority"] = self.priority.value  # Enum을 문자열로
        return data

    def __str__(self) -> str:
        status = "[완료]" if self.completed else "[미완료]"
        return f"#{self.id} {status} {self.title}"


class TodoStorage:
    """할일 데이터를 JSON 파일로 저장하는 클래스"""

    # JSON 파일 포맷 버전 (향후 마이그레이션용)
    FORMAT_VERSION = "1.0"

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save(self, todos: list[Todo]) -> dict:
        """
        할일 목록을 JSON 파일로 저장합니다.

        Args:
            todos: 저장할 할일 목록

        Returns:
            저장 결과 정보를 담은 딕셔너리
        """
        # 저장할 데이터 구성
        data = {
            "metadata": {
                "version": self.FORMAT_VERSION,
                "saved_at": datetime.now().isoformat(),
                "total_count": len(todos),
                "completed_count": sum(1 for t in todos if t.completed),
                "app": "CLI 할일 관리 앱",
            },
            "todos": [todo.to_dict() for todo in todos],
        }

        # 디렉토리 생성 (없으면)
        dir_path = os.path.dirname(self.file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        # JSON 파일로 저장
        # ensure_ascii=False: 한글이 이스케이프 되지 않도록 설정
        # indent=2: 사람이 읽기 쉬운 형태로 저장
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 저장 결과 정보
        file_size = os.path.getsize(self.file_path)
        result = {
            "file_path": self.file_path,
            "file_size": file_size,
            "file_size_str": format_file_size(file_size),
            "todo_count": len(todos),
            "saved_at": data["metadata"]["saved_at"],
        }

        return result

    def save_backup(self, todos: list[Todo]) -> str | None:
        """
        백업 파일을 생성합니다.
        기존 파일이 있으면 .bak 확장자로 복사합니다.
        """
        if not os.path.exists(self.file_path):
            return None

        # 백업 파일명 생성 (타임스탬프 포함)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base, ext = os.path.splitext(self.file_path)
        backup_path = f"{base}_backup_{timestamp}{ext}"

        # 기존 파일 읽기
        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 백업 파일 쓰기
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(content)

        return backup_path


def format_file_size(size_bytes: int) -> str:
    """파일 크기를 사람이 읽기 쉬운 형태로 변환합니다."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


if __name__ == "__main__":
    print("=" * 55)
    print("CLI 할일 관리 앱 - JSON 저장 기능 데모")
    print("=" * 55)
    print()

    # /tmp 디렉토리에 저장 (프로젝트 디렉토리 보호)
    save_dir = "/tmp/todo-cli-data"
    save_path = os.path.join(save_dir, "todos.json")
    storage = TodoStorage(save_path)

    # 데모 데이터 생성
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    todos = [
        Todo(id=1, title="우유 사기", priority=Priority.LOW,
             completed=True, completed_at=datetime.now().isoformat(),
             tags=["장보기"]),
        Todo(id=2, title="보고서 작성", priority=Priority.HIGH,
             due_date=tomorrow, tags=["업무", "급함"]),
        Todo(id=3, title="운동하기", priority=Priority.MEDIUM,
             tags=["건강", "루틴"]),
        Todo(id=4, title="이메일 답장", priority=Priority.HIGH,
             due_date=tomorrow, tags=["업무"]),
        Todo(id=5, title="책 읽기", priority=Priority.LOW,
             due_date=next_week),
    ]

    # 1. 할일 목록 확인
    print("--- 저장할 할일 목록 ---")
    for todo in todos:
        print(f"  {todo}")
    print()

    # 2. JSON 저장
    print("--- 1. JSON 파일로 저장 ---")
    result = storage.save(todos)
    print(f"  저장 경로: {result['file_path']}")
    print(f"  파일 크기: {result['file_size_str']}")
    print(f"  저장 항목: {result['todo_count']}개")
    print(f"  저장 시각: {result['saved_at']}")
    print()

    # 3. 저장된 파일 내용 확인
    print("--- 2. 저장된 JSON 내용 ---")
    with open(save_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(content)
    print()

    # 4. 백업 저장
    print("--- 3. 백업 파일 생성 ---")
    backup_path = storage.save_backup(todos)
    if backup_path:
        print(f"  백업 경로: {backup_path}")
        backup_size = os.path.getsize(backup_path)
        print(f"  백업 크기: {format_file_size(backup_size)}")
    else:
        print("  백업할 기존 파일이 없습니다.")
    print()

    # 5. 수정 후 재저장
    print("--- 4. 데이터 수정 후 재저장 ---")
    todos[2].completed = True
    todos[2].completed_at = datetime.now().isoformat()
    todos.append(
        Todo(id=6, title="빨래 개기", priority=Priority.MEDIUM, tags=["집안일"])
    )

    result2 = storage.save(todos)
    print(f"  수정 후 저장: {result2['todo_count']}개 항목")
    print(f"  파일 크기: {result2['file_size_str']}")
    print()

    # 정리
    print("--- 정리 ---")
    # /tmp이므로 시스템이 자동 정리하지만, 명시적으로 삭제
    import shutil
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
        print(f"  임시 디렉토리 삭제: {save_dir}")
    print()
    print("JSON 저장 데모 완료!")
