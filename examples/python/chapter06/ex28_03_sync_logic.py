"""
예제 28-3: 동기화 로직
- 소스 디렉토리의 내용을 대상 디렉토리로 동기화합니다.
- 단방향 동기화: 소스를 기준으로 대상을 맞춥니다.
- 추가/수정/삭제 작업을 수행하고 결과를 보고합니다.
"""

import hashlib
import os
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path


def file_hash(file_path: str) -> str:
    """파일의 SHA256 해시를 계산합니다."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


@dataclass
class SyncResult:
    """동기화 결과를 담는 데이터 클래스"""
    copied: list = field(default_factory=list)     # 복사된(추가/수정) 파일
    deleted: list = field(default_factory=list)     # 삭제된 파일
    skipped: list = field(default_factory=list)     # 건너뛴(동일) 파일
    errors: list = field(default_factory=list)      # 오류 발생 파일

    def summary(self) -> str:
        lines = [
            f"  복사됨: {len(self.copied)}개",
            f"  삭제됨: {len(self.deleted)}개",
            f"  건너뜀: {len(self.skipped)}개",
            f"  오류:   {len(self.errors)}개",
        ]
        return "\n".join(lines)


def scan_files(directory: str) -> dict:
    """디렉토리 내 모든 파일의 {상대경로: 해시} 딕셔너리를 반환합니다."""
    result = {}
    base = Path(directory)
    for file_path in sorted(base.rglob("*")):
        if file_path.is_file():
            rel = str(file_path.relative_to(base))
            result[rel] = file_hash(str(file_path))
    return result


def sync_directories(
    source_dir: str,
    target_dir: str,
    delete_extra: bool = True,
    dry_run: bool = False,
) -> SyncResult:
    """
    소스 디렉토리를 기준으로 대상 디렉토리를 동기화합니다.

    Args:
        source_dir: 소스(원본) 디렉토리
        target_dir: 대상(사본) 디렉토리
        delete_extra: True이면 소스에 없는 대상 파일을 삭제
        dry_run: True이면 실제 작업 없이 시뮬레이션만 수행

    Returns:
        SyncResult 객체
    """
    result = SyncResult()

    source_files = scan_files(source_dir)
    target_files = scan_files(target_dir)

    source_paths = set(source_files.keys())
    target_paths = set(target_files.keys())

    # 1단계: 추가/수정 파일 복사 (소스 → 대상)
    for rel_path in sorted(source_paths):
        src_full = os.path.join(source_dir, rel_path)
        tgt_full = os.path.join(target_dir, rel_path)

        if rel_path not in target_files:
            # 새 파일 추가
            action = "추가"
        elif source_files[rel_path] != target_files[rel_path]:
            # 내용이 변경된 파일 업데이트
            action = "수정"
        else:
            # 동일한 파일 건너뛰기
            result.skipped.append(rel_path)
            continue

        try:
            if not dry_run:
                # 대상 디렉토리 생성 (필요시)
                os.makedirs(os.path.dirname(tgt_full), exist_ok=True)
                # 파일 복사 (메타데이터 포함)
                shutil.copy2(src_full, tgt_full)
            result.copied.append((rel_path, action))
        except Exception as e:
            result.errors.append((rel_path, str(e)))

    # 2단계: 소스에 없는 파일 삭제 (옵션)
    if delete_extra:
        for rel_path in sorted(target_paths - source_paths):
            tgt_full = os.path.join(target_dir, rel_path)
            try:
                if not dry_run:
                    os.remove(tgt_full)
                result.deleted.append(rel_path)
            except Exception as e:
                result.errors.append((rel_path, str(e)))

        # 빈 디렉토리 정리
        if not dry_run:
            _cleanup_empty_dirs(target_dir)

    return result


def _cleanup_empty_dirs(directory: str):
    """빈 하위 디렉토리를 재귀적으로 삭제합니다."""
    for root, dirs, files in os.walk(directory, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
            except OSError:
                pass


def print_sync_details(result: SyncResult, dry_run: bool = False):
    """동기화 결과를 상세하게 출력합니다."""
    prefix = "[시뮬레이션] " if dry_run else ""

    if result.copied:
        print(f"\n  {prefix}복사된 파일:")
        for path, action in result.copied:
            symbol = "+" if action == "추가" else "~"
            print(f"    {symbol} [{action}] {path}")

    if result.deleted:
        print(f"\n  {prefix}삭제된 파일:")
        for path in result.deleted:
            print(f"    - [삭제] {path}")

    if result.skipped:
        print(f"\n  {prefix}건너뛴 파일:")
        for path in result.skipped:
            print(f"    = [동일] {path}")

    if result.errors:
        print(f"\n  {prefix}오류 발생:")
        for path, error in result.errors:
            print(f"    ! [오류] {path}: {error}")


if __name__ == "__main__":
    print("=" * 60)
    print("  디렉토리 동기화 도구 데모")
    print("=" * 60)

    # 데모 디렉토리 준비
    base_dir = tempfile.mkdtemp(prefix="sync_demo_", dir="/tmp")
    source_dir = os.path.join(base_dir, "source")
    target_dir = os.path.join(base_dir, "target")
    os.makedirs(source_dir)
    os.makedirs(target_dir)

    print(f"\n[준비] 소스: {source_dir}")
    print(f"[준비] 대상: {target_dir}")

    # 소스 디렉토리에 파일 생성
    source_files = {
        "README.md": "# 동기화 프로젝트\n바이브 코딩으로 만든 파일 동기화 도구\n",
        "config.json": '{"version": "1.0"}\n',
        os.path.join("src", "app.py"): "# 메인 애플리케이션\nprint('Hello')\n",
        os.path.join("src", "utils.py"): "# 유틸리티 함수\ndef greet():\n    return '안녕!'\n",
        os.path.join("data", "sample.txt"): "샘플 데이터 파일\n",
    }

    for rel_path, content in source_files.items():
        full_path = os.path.join(source_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    # 대상 디렉토리에 일부 파일 미리 생성 (비동기 상태 시뮬레이션)
    target_existing = {
        "README.md": "# 구버전 README\n",  # 내용이 다른 파일
        os.path.join("src", "app.py"): "# 메인 애플리케이션\nprint('Hello')\n",  # 동일한 파일
        "old_file.txt": "삭제 대상 파일\n",  # 소스에 없는 파일
    }

    for rel_path, content in target_existing.items():
        full_path = os.path.join(target_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    # --- 시나리오 1: 시뮬레이션(dry-run) ---
    print("\n--- 시나리오 1: 시뮬레이션 (dry-run) ---")
    print("  * 실제 파일 변경 없이 어떤 작업이 수행될지 미리 확인합니다.\n")

    dry_result = sync_directories(source_dir, target_dir, dry_run=True)
    print(dry_result.summary())
    print_sync_details(dry_result, dry_run=True)

    # 대상 디렉토리 확인 (변경 없어야 함)
    target_before = scan_files(target_dir)
    print(f"\n  대상 디렉토리 파일 수 (변경 전): {len(target_before)}개")

    # --- 시나리오 2: 실제 동기화 (삭제 포함) ---
    print("\n--- 시나리오 2: 실제 동기화 실행 ---")
    print("  * 소스 → 대상 방향으로 완전 동기화를 수행합니다.\n")

    sync_result = sync_directories(source_dir, target_dir, delete_extra=True)
    print(sync_result.summary())
    print_sync_details(sync_result)

    # 동기화 후 대상 디렉토리 확인
    target_after = scan_files(target_dir)
    print(f"\n  대상 디렉토리 파일 수 (동기화 후): {len(target_after)}개")

    # --- 시나리오 3: 다시 동기화 (변경 없음 확인) ---
    print("\n--- 시나리오 3: 재동기화 (변경 없음 확인) ---")
    print("  * 이미 동기화된 상태에서 다시 실행하면 모든 파일을 건너뜁니다.\n")

    re_sync_result = sync_directories(source_dir, target_dir)
    print(re_sync_result.summary())

    # --- 시나리오 4: 삭제 없이 동기화 ---
    print("\n--- 시나리오 4: 삭제 없이 동기화 ---")
    print("  * delete_extra=False 옵션으로 소스에 없는 파일을 유지합니다.\n")

    # 대상에 추가 파일 생성
    extra_file = os.path.join(target_dir, "local_notes.txt")
    with open(extra_file, "w", encoding="utf-8") as f:
        f.write("대상에만 있는 로컬 메모\n")

    keep_result = sync_directories(source_dir, target_dir, delete_extra=False)
    print(keep_result.summary())
    print(f"\n  'local_notes.txt' 파일 존재 여부: {os.path.exists(extra_file)}")

    # 정리
    shutil.rmtree(base_dir)
    print(f"\n[정리] 데모 디렉토리 삭제 완료")
    print("\n" + "=" * 60)
