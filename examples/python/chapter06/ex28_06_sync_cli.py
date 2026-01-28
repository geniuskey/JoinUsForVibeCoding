"""
예제 28-6: 파일 동기화 CLI 인터페이스
- argparse를 사용하여 명령줄에서 파일 동기화 도구를 사용합니다.
- scan(스캔), sync(동기화), compare(비교) 서브커맨드를 제공합니다.
- 실행 예: python ex28_06_sync_cli.py sync /source /target --delete --verbose
"""

import argparse
import hashlib
import json
import logging
import os
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path


# ========== 핵심 유틸리티 함수 ==========

def file_hash(path: str) -> str:
    """파일의 SHA256 해시를 계산합니다."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_directory(directory: str) -> dict:
    """디렉토리 내 모든 파일의 {상대경로: 해시} 딕셔너리를 반환합니다."""
    result = {}
    base = Path(directory)
    if not base.exists():
        return result
    for p in sorted(base.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(base))
            result[rel] = file_hash(str(p))
    return result


def setup_logger(verbose: bool = False, log_file: str = None) -> logging.Logger:
    """로거를 설정하고 반환합니다."""
    logger = logging.getLogger("sync_cli")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # 콘솔 핸들러
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if verbose else logging.INFO)
    ch.setFormatter(logging.Formatter("  [%(levelname)-7s] %(message)s"))
    logger.addHandler(ch)

    # 파일 핸들러
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)-7s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        logger.addHandler(fh)

    return logger


# ========== 서브커맨드 구현 ==========

def cmd_scan(args):
    """scan 서브커맨드: 디렉토리를 스캔하여 파일 목록과 해시를 출력합니다."""
    logger = setup_logger(args.verbose)
    directory = os.path.abspath(args.directory)

    if not os.path.isdir(directory):
        logger.error(f"디렉토리가 존재하지 않습니다: {directory}")
        return 1

    logger.info(f"디렉토리 스캔: {directory}")
    files = scan_directory(directory)

    total_size = 0
    for rel_path, hash_value in files.items():
        full_path = os.path.join(directory, rel_path)
        size = os.path.getsize(full_path)
        total_size += size
        if args.verbose:
            logger.debug(f"  {rel_path} ({size}B) → {hash_value[:16]}...")
        else:
            logger.info(f"  {rel_path} ({size}B)")

    logger.info(f"총 {len(files)}개 파일, {total_size:,} 바이트")

    # JSON 출력 옵션
    if args.output:
        output_data = {
            "디렉토리": directory,
            "스캔시간": datetime.now().isoformat(),
            "파일수": len(files),
            "파일목록": files,
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        logger.info(f"스캔 결과 저장: {args.output}")

    return 0


def cmd_compare(args):
    """compare 서브커맨드: 두 디렉토리를 비교합니다."""
    logger = setup_logger(args.verbose)
    source = os.path.abspath(args.source)
    target = os.path.abspath(args.target)

    if not os.path.isdir(source):
        logger.error(f"소스 디렉토리가 존재하지 않습니다: {source}")
        return 1
    if not os.path.isdir(target):
        logger.error(f"대상 디렉토리가 존재하지 않습니다: {target}")
        return 1

    logger.info(f"소스: {source}")
    logger.info(f"대상: {target}")
    logger.info("")

    src_files = scan_directory(source)
    tgt_files = scan_directory(target)

    src_paths = set(src_files.keys())
    tgt_paths = set(tgt_files.keys())

    added = sorted(src_paths - tgt_paths)
    deleted = sorted(tgt_paths - src_paths)
    common = sorted(src_paths & tgt_paths)
    modified = [p for p in common if src_files[p] != tgt_files[p]]
    unchanged = [p for p in common if src_files[p] == tgt_files[p]]

    if added:
        logger.info(f"추가 필요 ({len(added)}개):")
        for p in added:
            logger.info(f"  + {p}")
    if modified:
        logger.info(f"수정 필요 ({len(modified)}개):")
        for p in modified:
            logger.info(f"  ~ {p}")
    if deleted:
        logger.info(f"삭제 대상 ({len(deleted)}개):")
        for p in deleted:
            logger.info(f"  - {p}")
    if unchanged:
        logger.info(f"변경 없음 ({len(unchanged)}개):")
        for p in unchanged:
            logger.debug(f"  = {p}")

    logger.info("")
    logger.info(f"요약: 추가 {len(added)} | 수정 {len(modified)} | "
                f"삭제 {len(deleted)} | 동일 {len(unchanged)}")

    return 0


def cmd_sync(args):
    """sync 서브커맨드: 소스를 기준으로 대상을 동기화합니다."""
    log_file = args.log_file if hasattr(args, "log_file") else None
    logger = setup_logger(args.verbose, log_file)
    source = os.path.abspath(args.source)
    target = os.path.abspath(args.target)

    if not os.path.isdir(source):
        logger.error(f"소스 디렉토리가 존재하지 않습니다: {source}")
        return 1

    # 대상 디렉토리가 없으면 생성
    os.makedirs(target, exist_ok=True)

    logger.info("=" * 50)
    logger.info("파일 동기화 시작")
    logger.info(f"  소스: {source}")
    logger.info(f"  대상: {target}")
    logger.info(f"  삭제 모드: {'활성' if args.delete else '비활성'}")
    logger.info(f"  시뮬레이션: {'예' if args.dry_run else '아니오'}")
    logger.info("")

    src_files = scan_directory(source)
    tgt_files = scan_directory(target)

    stats = {"복사": 0, "삭제": 0, "건너뜀": 0, "오류": 0}

    # 추가/수정 파일 복사
    for rel_path, src_hash in sorted(src_files.items()):
        src_full = os.path.join(source, rel_path)
        tgt_full = os.path.join(target, rel_path)

        if rel_path not in tgt_files:
            action = "추가"
        elif src_hash != tgt_files[rel_path]:
            action = "수정"
        else:
            stats["건너뜀"] += 1
            logger.debug(f"[건너뜀] {rel_path}")
            continue

        try:
            if not args.dry_run:
                os.makedirs(os.path.dirname(tgt_full), exist_ok=True)
                shutil.copy2(src_full, tgt_full)
            stats["복사"] += 1
            prefix = "[시뮬레이션] " if args.dry_run else ""
            logger.info(f"{prefix}[{action}] {rel_path}")
        except Exception as e:
            stats["오류"] += 1
            logger.error(f"[오류] {rel_path}: {e}")

    # 삭제
    if args.delete:
        for rel_path in sorted(set(tgt_files.keys()) - set(src_files.keys())):
            tgt_full = os.path.join(target, rel_path)
            try:
                if not args.dry_run:
                    os.remove(tgt_full)
                stats["삭제"] += 1
                prefix = "[시뮬레이션] " if args.dry_run else ""
                logger.info(f"{prefix}[삭제] {rel_path}")
            except Exception as e:
                stats["오류"] += 1
                logger.error(f"[오류] {rel_path}: {e}")

    logger.info("")
    logger.info("동기화 완료")
    logger.info(f"  복사: {stats['복사']} | 삭제: {stats['삭제']} | "
                f"건너뜀: {stats['건너뜀']} | 오류: {stats['오류']}")
    logger.info("=" * 50)

    return 0


# ========== CLI 파서 구성 ==========

def create_parser() -> argparse.ArgumentParser:
    """명령줄 인자 파서를 생성합니다."""
    parser = argparse.ArgumentParser(
        prog="file_sync",
        description="파일 동기화 도구 - 바이브 코딩으로 만든 CLI 도구",
        epilog="예제: %(prog)s sync ./source ./target --delete --verbose",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s 1.0.0"
    )

    # 서브커맨드 설정
    subparsers = parser.add_subparsers(
        title="명령어",
        description="사용 가능한 명령어",
        dest="command",
    )

    # --- scan 서브커맨드 ---
    scan_parser = subparsers.add_parser(
        "scan",
        help="디렉토리를 스캔하여 파일 목록을 출력합니다",
        description="지정한 디렉토리의 모든 파일과 해시를 출력합니다.",
    )
    scan_parser.add_argument("directory", help="스캔할 디렉토리 경로")
    scan_parser.add_argument(
        "-o", "--output", help="스캔 결과를 JSON 파일로 저장"
    )
    scan_parser.add_argument(
        "-v", "--verbose", action="store_true", help="상세 출력 (해시값 포함)"
    )
    scan_parser.set_defaults(func=cmd_scan)

    # --- compare 서브커맨드 ---
    compare_parser = subparsers.add_parser(
        "compare",
        help="두 디렉토리를 비교합니다",
        description="소스와 대상 디렉토리를 비교하여 차이점을 보여줍니다.",
    )
    compare_parser.add_argument("source", help="소스(원본) 디렉토리")
    compare_parser.add_argument("target", help="대상(사본) 디렉토리")
    compare_parser.add_argument(
        "-v", "--verbose", action="store_true", help="상세 출력"
    )
    compare_parser.set_defaults(func=cmd_compare)

    # --- sync 서브커맨드 ---
    sync_parser = subparsers.add_parser(
        "sync",
        help="소스 디렉토리를 기준으로 대상을 동기화합니다",
        description="소스 → 대상 방향으로 파일을 동기화합니다.",
    )
    sync_parser.add_argument("source", help="소스(원본) 디렉토리")
    sync_parser.add_argument("target", help="대상(사본) 디렉토리")
    sync_parser.add_argument(
        "-d", "--delete", action="store_true",
        help="소스에 없는 대상 파일을 삭제합니다"
    )
    sync_parser.add_argument(
        "-n", "--dry-run", action="store_true",
        help="실제 작업 없이 시뮬레이션만 수행합니다"
    )
    sync_parser.add_argument(
        "-v", "--verbose", action="store_true", help="상세 출력"
    )
    sync_parser.add_argument(
        "--log-file", help="로그 파일 경로"
    )
    sync_parser.set_defaults(func=cmd_sync)

    return parser


def run_demo():
    """데모 모드: 임시 디렉토리를 만들어 각 서브커맨드를 시연합니다."""
    print("=" * 60)
    print("  파일 동기화 CLI 도구 데모")
    print("=" * 60)

    # 데모 디렉토리 준비
    base_dir = tempfile.mkdtemp(prefix="cli_demo_", dir="/tmp")
    source_dir = os.path.join(base_dir, "source")
    target_dir = os.path.join(base_dir, "target")
    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(source_dir)
    os.makedirs(target_dir)

    print(f"\n[준비] 데모 디렉토리: {base_dir}")

    # 소스 파일 생성
    files = {
        "README.md": "# 동기화 프로젝트\n",
        "config.json": '{"version": "1.0"}\n',
        os.path.join("src", "main.py"): "print('메인')\n",
        os.path.join("src", "utils.py"): "def helper(): pass\n",
        os.path.join("docs", "guide.md"): "# 가이드\n",
    }

    for rel, content in files.items():
        path = os.path.join(source_dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    # 대상 기존 파일
    target_files = {
        "README.md": "# 구버전\n",
        os.path.join("src", "main.py"): "print('메인')\n",  # 동일
        "old_data.txt": "삭제될 파일\n",
    }

    for rel, content in target_files.items():
        path = os.path.join(target_dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    parser = create_parser()

    # --- 데모 1: scan 명령어 ---
    print("\n" + "-" * 60)
    print("  데모 1: scan 명령어")
    print(f"  $ file_sync scan {source_dir} --verbose")
    print("-" * 60 + "\n")

    args = parser.parse_args(["scan", source_dir, "--verbose"])
    args.func(args)

    # --- 데모 2: compare 명령어 ---
    print("\n" + "-" * 60)
    print("  데모 2: compare 명령어")
    print(f"  $ file_sync compare {source_dir} {target_dir}")
    print("-" * 60 + "\n")

    args = parser.parse_args(["compare", source_dir, target_dir])
    args.func(args)

    # --- 데모 3: sync --dry-run ---
    print("\n" + "-" * 60)
    print("  데모 3: sync --dry-run (시뮬레이션)")
    print(f"  $ file_sync sync {source_dir} {target_dir} --delete --dry-run")
    print("-" * 60 + "\n")

    args = parser.parse_args([
        "sync", source_dir, target_dir, "--delete", "--dry-run", "--verbose"
    ])
    args.func(args)

    # --- 데모 4: sync (실제 동기화) ---
    print("\n" + "-" * 60)
    print("  데모 4: sync (실제 동기화)")
    log_file = os.path.join(log_dir, "sync.log")
    print(f"  $ file_sync sync {source_dir} {target_dir} --delete --log-file {log_file}")
    print("-" * 60 + "\n")

    args = parser.parse_args([
        "sync", source_dir, target_dir, "--delete",
        "--verbose", "--log-file", log_file
    ])
    args.func(args)

    # --- 데모 5: 도움말 출력 ---
    print("\n" + "-" * 60)
    print("  데모 5: 도움말 (--help)")
    print("-" * 60 + "\n")
    parser.print_help()

    # 정리
    shutil.rmtree(base_dir)
    print(f"\n[정리] 데모 디렉토리 삭제 완료")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # 인자가 없으면 데모 모드 실행
    if len(sys.argv) == 1:
        run_demo()
    else:
        parser = create_parser()
        args = parser.parse_args()
        if hasattr(args, "func"):
            exit_code = args.func(args)
            sys.exit(exit_code or 0)
        else:
            parser.print_help()
            sys.exit(1)
