"""
예제 28-5: 동기화 로그 기록
- logging 모듈을 사용하여 동기화 작업을 체계적으로 기록합니다.
- 콘솔 출력과 파일 로그를 동시에 관리합니다.
- 로그 레벨별 필터링과 포맷 커스터마이징을 보여줍니다.
"""

import hashlib
import logging
import os
import shutil
import tempfile
import time
from datetime import datetime
from pathlib import Path


class SyncLogger:
    """
    동기화 작업 전용 로거 클래스

    - 콘솔: INFO 이상 레벨을 간결하게 출력
    - 파일: DEBUG 이상 레벨을 상세하게 기록
    - 통계 추적: 작업별 카운터 관리
    """

    def __init__(self, name: str = "file_sync", log_dir: str = None):
        """
        로거를 초기화합니다.

        Args:
            name: 로거 이름
            log_dir: 로그 파일을 저장할 디렉토리 (None이면 현재 디렉토리)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        # 기존 핸들러 제거 (중복 방지)
        self.logger.handlers.clear()

        # 통계 카운터
        self.stats = {
            "복사": 0,
            "삭제": 0,
            "건너뜀": 0,
            "충돌": 0,
            "오류": 0,
        }
        self.start_time = None

        # 콘솔 핸들러 설정 (INFO 이상)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            "  [%(levelname)-7s] %(message)s"
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

        # 파일 핸들러 설정 (DEBUG 이상)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"sync_{timestamp}.log")
            self.log_file = log_file

            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                "%(asctime)s [%(levelname)-7s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
        else:
            self.log_file = None

    def start_sync(self, source: str, target: str):
        """동기화 시작을 기록합니다."""
        self.start_time = time.time()
        self.logger.info("=" * 50)
        self.logger.info("동기화 작업 시작")
        self.logger.info(f"  소스: {source}")
        self.logger.info(f"  대상: {target}")
        self.logger.debug(f"시작 시간: {datetime.now().isoformat()}")

    def end_sync(self):
        """동기화 완료를 기록합니다."""
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.logger.info("-" * 50)
        self.logger.info("동기화 작업 완료")
        self.logger.info(f"  소요 시간: {elapsed:.2f}초")
        self.logger.info(f"  복사: {self.stats['복사']}건 | "
                         f"삭제: {self.stats['삭제']}건 | "
                         f"건너뜀: {self.stats['건너뜀']}건")
        if self.stats["충돌"] > 0:
            self.logger.warning(f"  충돌: {self.stats['충돌']}건")
        if self.stats["오류"] > 0:
            self.logger.error(f"  오류: {self.stats['오류']}건")
        self.logger.info("=" * 50)

    def log_copy(self, rel_path: str, action: str = "복사"):
        """파일 복사를 기록합니다."""
        self.stats["복사"] += 1
        self.logger.info(f"[{action}] {rel_path}")
        self.logger.debug(f"  작업: {action}, 파일: {rel_path}")

    def log_delete(self, rel_path: str):
        """파일 삭제를 기록합니다."""
        self.stats["삭제"] += 1
        self.logger.info(f"[삭제] {rel_path}")
        self.logger.debug(f"  작업: 삭제, 파일: {rel_path}")

    def log_skip(self, rel_path: str, reason: str = "동일"):
        """파일 건너뛰기를 기록합니다."""
        self.stats["건너뜀"] += 1
        self.logger.debug(f"[건너뜀] {rel_path} (사유: {reason})")

    def log_conflict(self, rel_path: str, resolution: str):
        """충돌 해결을 기록합니다."""
        self.stats["충돌"] += 1
        self.logger.warning(f"[충돌] {rel_path} → {resolution}")

    def log_error(self, rel_path: str, error: str):
        """오류를 기록합니다."""
        self.stats["오류"] += 1
        self.logger.error(f"[오류] {rel_path}: {error}")

    def log_scan(self, directory: str, file_count: int):
        """디렉토리 스캔 결과를 기록합니다."""
        self.logger.info(f"[스캔] {directory} ({file_count}개 파일)")
        self.logger.debug(f"  스캔 완료: {directory}, 파일 수: {file_count}")


def file_hash(path: str) -> str:
    """파일 해시를 계산합니다."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sync_with_logging(source_dir: str, target_dir: str, sync_logger: SyncLogger):
    """
    로깅을 포함한 동기화를 수행합니다.

    Args:
        source_dir: 소스 디렉토리
        target_dir: 대상 디렉토리
        sync_logger: SyncLogger 인스턴스
    """
    sync_logger.start_sync(source_dir, target_dir)

    # 소스 스캔
    src_base = Path(source_dir)
    src_files = {}
    for p in sorted(src_base.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(src_base))
            src_files[rel] = file_hash(str(p))
    sync_logger.log_scan(source_dir, len(src_files))

    # 대상 스캔
    tgt_base = Path(target_dir)
    tgt_files = {}
    for p in sorted(tgt_base.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(tgt_base))
            tgt_files[rel] = file_hash(str(p))
    sync_logger.log_scan(target_dir, len(tgt_files))

    # 추가/수정 파일 복사
    for rel_path, src_hash in sorted(src_files.items()):
        src_full = os.path.join(source_dir, rel_path)
        tgt_full = os.path.join(target_dir, rel_path)

        if rel_path not in tgt_files:
            # 새 파일 추가
            try:
                os.makedirs(os.path.dirname(tgt_full), exist_ok=True)
                shutil.copy2(src_full, tgt_full)
                sync_logger.log_copy(rel_path, "추가")
            except Exception as e:
                sync_logger.log_error(rel_path, str(e))
        elif src_hash != tgt_files[rel_path]:
            # 수정된 파일 업데이트
            try:
                shutil.copy2(src_full, tgt_full)
                sync_logger.log_copy(rel_path, "수정")
            except Exception as e:
                sync_logger.log_error(rel_path, str(e))
        else:
            # 동일한 파일
            sync_logger.log_skip(rel_path, "해시 동일")

    # 소스에 없는 파일 삭제
    for rel_path in sorted(set(tgt_files.keys()) - set(src_files.keys())):
        tgt_full = os.path.join(target_dir, rel_path)
        try:
            os.remove(tgt_full)
            sync_logger.log_delete(rel_path)
        except Exception as e:
            sync_logger.log_error(rel_path, str(e))

    sync_logger.end_sync()


if __name__ == "__main__":
    print("=" * 60)
    print("  동기화 로그 기록 도구 데모")
    print("=" * 60)

    # 데모 디렉토리 준비
    base_dir = tempfile.mkdtemp(prefix="log_demo_", dir="/tmp")
    source_dir = os.path.join(base_dir, "source")
    target_dir = os.path.join(base_dir, "target")
    log_dir = os.path.join(base_dir, "logs")

    os.makedirs(source_dir)
    os.makedirs(target_dir)

    print(f"\n[준비] 소스: {source_dir}")
    print(f"[준비] 대상: {target_dir}")
    print(f"[준비] 로그: {log_dir}")

    # 소스 파일 생성
    source_files = {
        "README.md": "# 프로젝트\n바이브 코딩 동기화 도구\n",
        "config.json": '{"version": "2.0"}\n',
        os.path.join("src", "app.py"): "print('앱 실행')\n",
        os.path.join("src", "utils.py"): "def helper(): pass\n",
        os.path.join("src", "new_module.py"): "# 새 모듈\n",
    }

    for rel_path, content in source_files.items():
        full_path = os.path.join(source_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    # 대상에 일부 기존 파일
    target_existing = {
        "README.md": "# 구버전\n",                            # 수정 대상
        os.path.join("src", "app.py"): "print('앱 실행')\n",  # 동일
        "deprecated.txt": "삭제 대상 파일\n",                   # 삭제 대상
    }

    for rel_path, content in target_existing.items():
        full_path = os.path.join(target_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    # --- 로깅 포함 동기화 실행 ---
    print("\n--- 동기화 실행 (로그 기록 활성화) ---\n")

    logger = SyncLogger(name="demo_sync", log_dir=log_dir)
    sync_with_logging(source_dir, target_dir, logger)

    # --- 로그 파일 내용 확인 ---
    print("\n--- 로그 파일 내용 ---")

    if logger.log_file and os.path.exists(logger.log_file):
        print(f"\n  로그 파일: {logger.log_file}\n")
        with open(logger.log_file, "r", encoding="utf-8") as f:
            content = f.read()
        # 로그 내용 출력 (들여쓰기)
        for line in content.strip().split("\n"):
            print(f"  | {line}")
    else:
        print("  로그 파일이 생성되지 않았습니다.")

    # --- 통계 요약 ---
    print("\n--- 최종 통계 ---")
    print(f"\n  작업 통계:")
    for key, value in logger.stats.items():
        bar = "#" * value
        print(f"    {key:6s}: {value:3d} {bar}")

    # --- 로깅 레벨 설명 ---
    print("\n--- 로그 레벨 안내 ---")
    print("""
  로그 레벨 체계:
    DEBUG   - 상세 디버그 정보 (건너뛴 파일 등)
    INFO    - 일반 작업 정보 (복사, 삭제 등)
    WARNING - 주의 필요 사항 (충돌 발생 등)
    ERROR   - 오류 발생 (파일 접근 실패 등)

  * 콘솔에는 INFO 이상만 표시됩니다.
  * 로그 파일에는 DEBUG 이상 모두 기록됩니다.
""")

    # 정리
    shutil.rmtree(base_dir)
    print(f"[정리] 데모 디렉토리 삭제 완료")
    print("\n" + "=" * 60)
