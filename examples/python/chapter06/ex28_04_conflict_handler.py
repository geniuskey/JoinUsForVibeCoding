"""
예제 28-4: 충돌 처리
- 양방향 동기화 시 발생하는 충돌을 감지하고 해결합니다.
- 충돌 해결 전략: 최신 파일 우선, 크기 우선, 백업 후 덮어쓰기
- 충돌 이력을 JSON으로 기록합니다.
"""

import hashlib
import json
import os
import shutil
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class ConflictStrategy(Enum):
    """충돌 해결 전략"""
    NEWER_WINS = "newer_wins"           # 최신 수정 파일 우선
    LARGER_WINS = "larger_wins"         # 더 큰 파일 우선
    SOURCE_WINS = "source_wins"         # 항상 소스 우선
    TARGET_WINS = "target_wins"         # 항상 대상 우선
    BACKUP_BOTH = "backup_both"         # 양쪽 모두 백업 후 소스 적용


@dataclass
class ConflictInfo:
    """충돌 정보를 담는 데이터 클래스"""
    relative_path: str
    source_modified: float
    target_modified: float
    source_size: int
    target_size: int
    source_hash: str
    target_hash: str
    resolution: str = ""
    resolved_by: str = ""

    def to_dict(self) -> dict:
        """JSON 직렬화를 위한 딕셔너리 변환"""
        return {
            "파일": self.relative_path,
            "소스_수정시간": datetime.fromtimestamp(self.source_modified).isoformat(),
            "대상_수정시간": datetime.fromtimestamp(self.target_modified).isoformat(),
            "소스_크기": self.source_size,
            "대상_크기": self.target_size,
            "해결_방법": self.resolution,
            "적용_기준": self.resolved_by,
        }


def file_hash(path: str) -> str:
    """파일 해시를 계산합니다."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def detect_conflicts(source_dir: str, target_dir: str, last_sync_hashes: dict = None) -> list:
    """
    양방향 동기화 시 충돌을 감지합니다.

    양쪽 모두 변경된 파일이 충돌입니다.
    last_sync_hashes: 마지막 동기화 시점의 해시 딕셔너리.
    이 값이 None이면 양쪽 해시가 다른 모든 공통 파일을 충돌로 간주합니다.
    """
    conflicts = []
    src_base = Path(source_dir)
    tgt_base = Path(target_dir)

    # 양쪽 파일 목록
    src_files = {str(p.relative_to(src_base)) for p in src_base.rglob("*") if p.is_file()}
    tgt_files = {str(p.relative_to(tgt_base)) for p in tgt_base.rglob("*") if p.is_file()}

    # 공통 파일 중 해시가 다른 것을 찾음
    for rel_path in sorted(src_files & tgt_files):
        src_full = os.path.join(source_dir, rel_path)
        tgt_full = os.path.join(target_dir, rel_path)

        src_hash = file_hash(src_full)
        tgt_hash = file_hash(tgt_full)

        # 해시가 동일하면 충돌 아님
        if src_hash == tgt_hash:
            continue

        # last_sync_hashes가 있으면, 양쪽 모두 변경되었는지 확인
        if last_sync_hashes and rel_path in last_sync_hashes:
            base_hash = last_sync_hashes[rel_path]
            src_changed = (src_hash != base_hash)
            tgt_changed = (tgt_hash != base_hash)
            # 한쪽만 변경: 충돌 아님 (변경된 쪽을 그대로 적용하면 됨)
            if not (src_changed and tgt_changed):
                continue

        src_stat = os.stat(src_full)
        tgt_stat = os.stat(tgt_full)

        conflicts.append(ConflictInfo(
            relative_path=rel_path,
            source_modified=src_stat.st_mtime,
            target_modified=tgt_stat.st_mtime,
            source_size=src_stat.st_size,
            target_size=tgt_stat.st_size,
            source_hash=src_hash,
            target_hash=tgt_hash,
        ))

    return conflicts


def resolve_conflict(
    conflict: ConflictInfo,
    source_dir: str,
    target_dir: str,
    strategy: ConflictStrategy,
    backup_dir: str = None,
) -> ConflictInfo:
    """
    주어진 전략에 따라 충돌을 해결합니다.

    Args:
        conflict: 충돌 정보
        source_dir: 소스 디렉토리
        target_dir: 대상 디렉토리
        strategy: 충돌 해결 전략
        backup_dir: 백업 디렉토리 (BACKUP_BOTH 전략 시 필요)

    Returns:
        해결 정보가 업데이트된 ConflictInfo
    """
    src_path = os.path.join(source_dir, conflict.relative_path)
    tgt_path = os.path.join(target_dir, conflict.relative_path)

    if strategy == ConflictStrategy.NEWER_WINS:
        # 최신 파일이 우선
        if conflict.source_modified >= conflict.target_modified:
            shutil.copy2(src_path, tgt_path)
            conflict.resolution = "소스 파일 적용 (더 최신)"
            conflict.resolved_by = "newer_wins → source"
        else:
            shutil.copy2(tgt_path, src_path)
            conflict.resolution = "대상 파일 적용 (더 최신)"
            conflict.resolved_by = "newer_wins → target"

    elif strategy == ConflictStrategy.LARGER_WINS:
        # 더 큰 파일이 우선 (더 많은 내용을 담고 있을 가능성)
        if conflict.source_size >= conflict.target_size:
            shutil.copy2(src_path, tgt_path)
            conflict.resolution = "소스 파일 적용 (더 큰 파일)"
            conflict.resolved_by = "larger_wins → source"
        else:
            shutil.copy2(tgt_path, src_path)
            conflict.resolution = "대상 파일 적용 (더 큰 파일)"
            conflict.resolved_by = "larger_wins → target"

    elif strategy == ConflictStrategy.SOURCE_WINS:
        # 항상 소스 우선
        shutil.copy2(src_path, tgt_path)
        conflict.resolution = "소스 파일 적용 (소스 우선 정책)"
        conflict.resolved_by = "source_wins"

    elif strategy == ConflictStrategy.TARGET_WINS:
        # 항상 대상 우선
        shutil.copy2(tgt_path, src_path)
        conflict.resolution = "대상 파일 적용 (대상 우선 정책)"
        conflict.resolved_by = "target_wins"

    elif strategy == ConflictStrategy.BACKUP_BOTH:
        # 양쪽 모두 백업 후 소스 적용
        if backup_dir is None:
            backup_dir = os.path.join(os.path.dirname(source_dir), "_conflict_backups")
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(conflict.relative_path)
        name, ext = os.path.splitext(base_name)

        # 소스 백업
        src_backup = os.path.join(backup_dir, f"{name}_source_{timestamp}{ext}")
        shutil.copy2(src_path, src_backup)

        # 대상 백업
        tgt_backup = os.path.join(backup_dir, f"{name}_target_{timestamp}{ext}")
        shutil.copy2(tgt_path, tgt_backup)

        # 소스 파일을 대상에 적용
        shutil.copy2(src_path, tgt_path)

        conflict.resolution = f"양쪽 백업 후 소스 적용 (백업: {backup_dir})"
        conflict.resolved_by = "backup_both → source applied"

    return conflict


def save_conflict_report(conflicts: list, report_path: str):
    """충돌 이력을 JSON 파일로 저장합니다."""
    report = {
        "생성시간": datetime.now().isoformat(),
        "총_충돌수": len(conflicts),
        "충돌_목록": [c.to_dict() for c in conflicts],
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print("=" * 60)
    print("  양방향 동기화 충돌 처리 데모")
    print("=" * 60)

    # 데모 디렉토리 준비
    base_dir = tempfile.mkdtemp(prefix="conflict_demo_", dir="/tmp")
    source_dir = os.path.join(base_dir, "source")
    target_dir = os.path.join(base_dir, "target")
    backup_dir = os.path.join(base_dir, "backups")
    os.makedirs(source_dir)
    os.makedirs(target_dir)

    print(f"\n[준비] 소스: {source_dir}")
    print(f"[준비] 대상: {target_dir}")

    # 양쪽에 공통 파일 생성 (마지막 동기화 시점 시뮬레이션)
    common_content = {
        "문서.txt": "원본 내용입니다.\n",
        "설정.json": '{"설정": "원본"}\n',
        os.path.join("코드", "메인.py"): "# 원본 코드\nprint('hello')\n",
    }

    # 마지막 동기화 시점의 해시 기록
    last_sync_hashes = {}

    for rel_path, content in common_content.items():
        for d in [source_dir, target_dir]:
            full = os.path.join(d, rel_path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
        # 해시 기록
        last_sync_hashes[rel_path] = file_hash(os.path.join(source_dir, rel_path))

    time.sleep(0.1)

    # 양쪽에서 서로 다르게 수정 (충돌 발생!)
    # 충돌 1: 문서.txt - 대상이 더 최신
    with open(os.path.join(source_dir, "문서.txt"), "w", encoding="utf-8") as f:
        f.write("소스에서 수정한 내용입니다.\n추가 라인.\n")
    time.sleep(0.2)
    with open(os.path.join(target_dir, "문서.txt"), "w", encoding="utf-8") as f:
        f.write("대상에서 수정한 내용입니다.\n")

    # 충돌 2: 설정.json - 소스가 더 최신
    with open(os.path.join(target_dir, "설정.json"), "w", encoding="utf-8") as f:
        f.write('{"설정": "대상에서 변경"}\n')
    time.sleep(0.2)
    with open(os.path.join(source_dir, "설정.json"), "w", encoding="utf-8") as f:
        f.write('{"설정": "소스에서 변경", "추가": true}\n')

    # 충돌 3: 코드/메인.py - 양쪽 다 수정
    with open(os.path.join(source_dir, "코드", "메인.py"), "w", encoding="utf-8") as f:
        f.write("# 소스에서 수정\nprint('소스 버전')\ndef func():\n    pass\n")
    with open(os.path.join(target_dir, "코드", "메인.py"), "w", encoding="utf-8") as f:
        f.write("# 대상에서 수정\nprint('대상 버전')\n")

    # --- 1. 충돌 감지 ---
    print("\n--- 1. 충돌 감지 ---")
    conflicts = detect_conflicts(source_dir, target_dir, last_sync_hashes)
    print(f"\n  감지된 충돌: {len(conflicts)}건\n")

    for i, c in enumerate(conflicts, 1):
        src_time = datetime.fromtimestamp(c.source_modified).strftime("%H:%M:%S")
        tgt_time = datetime.fromtimestamp(c.target_modified).strftime("%H:%M:%S")
        print(f"  충돌 {i}: {c.relative_path}")
        print(f"    소스 - 수정: {src_time}, 크기: {c.source_size}B, 해시: {c.source_hash[:16]}...")
        print(f"    대상 - 수정: {tgt_time}, 크기: {c.target_size}B, 해시: {c.target_hash[:16]}...")

    # --- 2. 다양한 전략으로 충돌 해결 ---
    print("\n--- 2. 전략별 충돌 해결 ---")

    strategies = [
        (ConflictStrategy.NEWER_WINS, "최신 파일 우선"),
        (ConflictStrategy.LARGER_WINS, "큰 파일 우선"),
        (ConflictStrategy.BACKUP_BOTH, "양쪽 백업 후 적용"),
    ]

    # 각 충돌에 서로 다른 전략 적용
    for i, (conflict, (strategy, desc)) in enumerate(zip(conflicts, strategies)):
        print(f"\n  충돌 {i + 1} ({conflict.relative_path}): {desc} 전략 적용")

        resolved = resolve_conflict(
            conflict, source_dir, target_dir, strategy, backup_dir
        )
        print(f"    결과: {resolved.resolution}")

    # --- 3. 충돌 보고서 저장 ---
    print("\n--- 3. 충돌 보고서 저장 ---")
    report_path = os.path.join(base_dir, "conflict_report.json")
    save_conflict_report(conflicts, report_path)

    with open(report_path, "r", encoding="utf-8") as f:
        report_content = json.load(f)

    print(f"\n  보고서 저장 위치: {report_path}")
    print(f"  총 충돌 수: {report_content['총_충돌수']}건")
    print(f"\n  보고서 내용:")
    print(json.dumps(report_content, ensure_ascii=False, indent=4))

    # --- 4. 백업 확인 ---
    print("\n--- 4. 백업 파일 확인 ---")
    if os.path.exists(backup_dir):
        backups = os.listdir(backup_dir)
        print(f"\n  백업 디렉토리: {backup_dir}")
        print(f"  백업 파일 수: {len(backups)}개")
        for bk in sorted(backups):
            size = os.path.getsize(os.path.join(backup_dir, bk))
            print(f"    - {bk} ({size} 바이트)")
    else:
        print("  백업 파일 없음")

    # 정리
    shutil.rmtree(base_dir)
    print(f"\n[정리] 데모 디렉토리 삭제 완료")
    print("\n" + "=" * 60)
