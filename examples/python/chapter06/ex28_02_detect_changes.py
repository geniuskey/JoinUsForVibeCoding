"""
예제 28-2: 변경 파일 감지
- 두 디렉토리를 비교하여 추가/수정/삭제된 파일을 감지합니다.
- 파일 해시와 수정 시간을 기준으로 변경 여부를 판단합니다.
- 동기화 전에 어떤 작업이 필요한지 파악하는 핵심 단계입니다.
"""

import hashlib
import os
import shutil
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path


def file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """파일의 SHA256 해시를 계산합니다."""
    hasher = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


@dataclass
class FileInfo:
    """파일의 메타데이터를 담는 데이터 클래스"""
    relative_path: str       # 기준 디렉토리로부터의 상대 경로
    size: int                # 파일 크기 (바이트)
    modified_time: float     # 마지막 수정 시간 (타임스탬프)
    hash_value: str          # SHA256 해시값


@dataclass
class ChangeReport:
    """두 디렉토리 비교 결과를 담는 데이터 클래스"""
    added: list = field(default_factory=list)      # 소스에만 존재하는 파일
    modified: list = field(default_factory=list)    # 양쪽 모두 존재하나 내용이 다른 파일
    deleted: list = field(default_factory=list)     # 대상에만 존재하는 파일
    unchanged: list = field(default_factory=list)   # 동일한 파일

    def summary(self) -> str:
        """변경 사항 요약 문자열을 반환합니다."""
        lines = []
        lines.append(f"  추가된 파일: {len(self.added)}개")
        lines.append(f"  수정된 파일: {len(self.modified)}개")
        lines.append(f"  삭제된 파일: {len(self.deleted)}개")
        lines.append(f"  변경 없음:   {len(self.unchanged)}개")
        return "\n".join(lines)

    @property
    def has_changes(self) -> bool:
        """변경 사항이 있는지 여부"""
        return bool(self.added or self.modified or self.deleted)


def scan_directory(directory: str) -> dict:
    """
    디렉토리를 스캔하여 모든 파일의 정보를 수집합니다.

    Args:
        directory: 스캔할 디렉토리 경로

    Returns:
        {상대경로: FileInfo} 형태의 딕셔너리
    """
    file_map = {}
    base_path = Path(directory)

    for file_path in sorted(base_path.rglob("*")):
        if file_path.is_file():
            rel_path = str(file_path.relative_to(base_path))
            stat = file_path.stat()
            file_map[rel_path] = FileInfo(
                relative_path=rel_path,
                size=stat.st_size,
                modified_time=stat.st_mtime,
                hash_value=file_hash(str(file_path)),
            )

    return file_map


def detect_changes(source_dir: str, target_dir: str) -> ChangeReport:
    """
    소스 디렉토리와 대상 디렉토리를 비교하여 변경 사항을 감지합니다.

    Args:
        source_dir: 소스(원본) 디렉토리
        target_dir: 대상(사본) 디렉토리

    Returns:
        ChangeReport 객체
    """
    report = ChangeReport()

    # 양쪽 디렉토리 스캔
    source_files = scan_directory(source_dir)
    target_files = scan_directory(target_dir)

    source_paths = set(source_files.keys())
    target_paths = set(target_files.keys())

    # 1. 추가된 파일: 소스에만 존재
    for path in sorted(source_paths - target_paths):
        report.added.append(source_files[path])

    # 2. 삭제된 파일: 대상에만 존재
    for path in sorted(target_paths - source_paths):
        report.deleted.append(target_files[path])

    # 3. 양쪽 모두 존재하는 파일: 해시 비교로 수정 여부 판단
    for path in sorted(source_paths & target_paths):
        src_info = source_files[path]
        tgt_info = target_files[path]

        if src_info.hash_value != tgt_info.hash_value:
            report.modified.append(src_info)
        else:
            report.unchanged.append(src_info)

    return report


def print_change_details(report: ChangeReport):
    """변경 사항의 세부 내용을 출력합니다."""
    if report.added:
        print("\n  [+] 추가된 파일:")
        for info in report.added:
            print(f"      + {info.relative_path} ({info.size} 바이트)")

    if report.modified:
        print("\n  [~] 수정된 파일:")
        for info in report.modified:
            print(f"      ~ {info.relative_path} ({info.size} 바이트)")

    if report.deleted:
        print("\n  [-] 삭제된 파일:")
        for info in report.deleted:
            print(f"      - {info.relative_path}")

    if report.unchanged:
        print("\n  [=] 변경 없는 파일:")
        for info in report.unchanged:
            print(f"      = {info.relative_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("  변경 파일 감지 도구 데모")
    print("=" * 60)

    # 임시 디렉토리 생성: 소스와 대상
    base_dir = tempfile.mkdtemp(prefix="detect_demo_", dir="/tmp")
    source_dir = os.path.join(base_dir, "source")
    target_dir = os.path.join(base_dir, "target")
    os.makedirs(source_dir)
    os.makedirs(target_dir)

    print(f"\n[준비] 소스 디렉토리: {source_dir}")
    print(f"[준비] 대상 디렉토리: {target_dir}")

    # --- 초기 파일 생성 (소스와 대상 모두 동일) ---
    common_files = {
        "README.md": "# 프로젝트 설명\n이것은 동기화 테스트입니다.\n",
        "config.json": '{"version": "1.0", "name": "sync-demo"}\n',
        os.path.join("src", "main.py"): "print('메인 프로그램')\n",
        os.path.join("src", "utils.py"): "def helper():\n    pass\n",
        os.path.join("docs", "guide.txt"): "사용자 가이드 내용\n",
    }

    for rel_path, content in common_files.items():
        for base in [source_dir, target_dir]:
            full_path = os.path.join(base, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

    # --- 시나리오 1: 변경 없는 상태 ---
    print("\n--- 시나리오 1: 초기 상태 (변경 없음) ---")
    report1 = detect_changes(source_dir, target_dir)
    print(report1.summary())
    print(f"  변경 필요: {'예' if report1.has_changes else '아니오'}")

    # --- 시나리오 2: 소스에 파일 추가 ---
    print("\n--- 시나리오 2: 소스에 새 파일 추가 ---")
    new_file = os.path.join(source_dir, "src", "new_feature.py")
    with open(new_file, "w", encoding="utf-8") as f:
        f.write("# 새로운 기능\ndef new_feature():\n    return '바이브 코딩!'\n")

    report2 = detect_changes(source_dir, target_dir)
    print(report2.summary())
    print_change_details(report2)

    # --- 시나리오 3: 소스의 파일 수정 ---
    print("\n--- 시나리오 3: 소스의 기존 파일 수정 ---")
    time.sleep(0.1)  # 수정 시간 차이를 위해 잠시 대기
    modified_file = os.path.join(source_dir, "config.json")
    with open(modified_file, "w", encoding="utf-8") as f:
        f.write('{"version": "2.0", "name": "sync-demo", "updated": true}\n')

    report3 = detect_changes(source_dir, target_dir)
    print(report3.summary())
    print_change_details(report3)

    # --- 시나리오 4: 대상에만 있는 파일 (소스에서 삭제된 효과) ---
    print("\n--- 시나리오 4: 소스에서 파일 삭제 ---")
    os.remove(os.path.join(source_dir, "docs", "guide.txt"))

    report4 = detect_changes(source_dir, target_dir)
    print(report4.summary())
    print_change_details(report4)

    # --- 최종 요약 ---
    print("\n--- 최종 상태 요약 ---")
    print(f"  소스 파일: {len(scan_directory(source_dir))}개")
    print(f"  대상 파일: {len(scan_directory(target_dir))}개")
    print(f"  동기화 필요: {'예' if report4.has_changes else '아니오'}")

    # 정리
    shutil.rmtree(base_dir)
    print(f"\n[정리] 데모 디렉토리 삭제 완료")
    print("\n" + "=" * 60)
