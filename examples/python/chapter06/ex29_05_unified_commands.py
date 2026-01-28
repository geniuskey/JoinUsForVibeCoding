#!/usr/bin/env python3
"""
예제 29-05: 명령어 통합
- argparse 서브커맨드로 날씨, 일정, 메모, 알림 기능을 하나의 CLI로 통합
- 각 모듈의 주요 기능을 커맨드라인에서 바로 사용 가능
- 독립 실행 시 데모 모드로 동작
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


# ── 데이터 디렉토리 설정 ──────────────────────────────────────────────────

DATA_DIR = Path("/tmp/personal_assistant")
SCHEDULE_FILE = DATA_DIR / "schedules.json"
MEMO_DIR = DATA_DIR / "memos"
CONFIG_FILE = DATA_DIR / "config.ini"


def ensure_data_dir():
    """데이터 디렉토리를 확인하고 생성합니다."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    MEMO_DIR.mkdir(parents=True, exist_ok=True)


# ══════════════════════════════════════════════════════════════════════════
# 날씨 관련 명령어
# ══════════════════════════════════════════════════════════════════════════

def cmd_weather(args):
    """날씨 정보를 표시합니다."""
    import random

    city = args.city
    conditions = [
        ("맑음", "☀️", 22, 15),
        ("구름 조금", "⛅", 20, 13),
        ("흐림", "☁️", 18, 11),
        ("비", "🌧️", 15, 10),
    ]

    random.seed(hash(city + datetime.now().strftime("%Y-%m-%d")))
    name, icon, high, low = random.choice(conditions)
    humidity = random.randint(40, 80)
    wind = round(random.uniform(1.0, 10.0), 1)

    print(f"\n  {icon} {city} 날씨 ({datetime.now().strftime('%Y-%m-%d')})")
    print(f"  상태: {name}")
    print(f"  기온: {low}~{high}°C")
    print(f"  습도: {humidity}%  |  풍속: {wind} m/s")

    if args.weekly:
        print(f"\n  ── 주간 예보 ──")
        days = ["월", "화", "수", "목", "금", "토", "일"]
        today_idx = datetime.now().weekday()
        for i in range(7):
            day = days[(today_idx + i) % 7]
            cond = random.choice(conditions)
            print(f"  {day}: {cond[1]} {cond[0]} ({cond[3]}~{cond[2]}°C)")
    print()


# ══════════════════════════════════════════════════════════════════════════
# 일정 관련 명령어
# ══════════════════════════════════════════════════════════════════════════

def _load_schedules():
    """일정 파일을 불러옵니다."""
    if SCHEDULE_FILE.exists():
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_schedules(schedules):
    """일정을 파일에 저장합니다."""
    ensure_data_dir()
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(schedules, f, ensure_ascii=False, indent=2)


def cmd_schedule_add(args):
    """새 일정을 추가합니다."""
    schedules = _load_schedules()
    new_id = max([s.get("id", 0) for s in schedules], default=0) + 1

    schedule = {
        "id": new_id,
        "title": args.title,
        "date": args.date,
        "time": args.time or "",
        "category": args.category,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed": False,
    }

    schedules.append(schedule)
    _save_schedules(schedules)
    print(f"  [추가 완료] #{new_id} '{args.title}' ({args.date})")


def cmd_schedule_list(args):
    """일정 목록을 표시합니다."""
    schedules = _load_schedules()

    if not schedules:
        print("  등록된 일정이 없습니다.")
        return

    # 필터링
    if args.today:
        today = datetime.now().strftime("%Y-%m-%d")
        schedules = [s for s in schedules if s["date"] == today]
    elif args.week:
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        schedules = [
            s for s in schedules
            if monday.strftime("%Y-%m-%d") <= s["date"] <= sunday.strftime("%Y-%m-%d")
        ]

    schedules.sort(key=lambda s: (s["date"], s.get("time", "")))

    print(f"\n  ── 일정 목록 ({len(schedules)}건) ──")
    for s in schedules:
        status = "V" if s.get("completed") else " "
        time_str = f" {s['time']}" if s.get("time") else ""
        print(f"  [{status}] #{s['id']} {s['date']}{time_str} "
              f"[{s.get('category', '일반')}] {s['title']}")
    print()


def cmd_schedule_done(args):
    """일정을 완료 처리합니다."""
    schedules = _load_schedules()
    for s in schedules:
        if s["id"] == args.id:
            s["completed"] = True
            _save_schedules(schedules)
            print(f"  [완료] #{args.id} '{s['title']}'")
            return
    print(f"  [오류] 일정 #{args.id}을(를) 찾을 수 없습니다.")


def cmd_schedule_delete(args):
    """일정을 삭제합니다."""
    schedules = _load_schedules()
    original_len = len(schedules)
    schedules = [s for s in schedules if s["id"] != args.id]

    if len(schedules) < original_len:
        _save_schedules(schedules)
        print(f"  [삭제 완료] 일정 #{args.id}")
    else:
        print(f"  [오류] 일정 #{args.id}을(를) 찾을 수 없습니다.")


# ══════════════════════════════════════════════════════════════════════════
# 메모 관련 명령어
# ══════════════════════════════════════════════════════════════════════════

def _load_memo_index():
    """메모 인덱스를 불러옵니다."""
    index_file = MEMO_DIR / "_index.json"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"memos": [], "next_id": 1}


def _save_memo_index(index):
    """메모 인덱스를 저장합니다."""
    ensure_data_dir()
    index_file = MEMO_DIR / "_index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def cmd_memo_add(args):
    """새 메모를 작성합니다."""
    index = _load_memo_index()
    memo_id = index["next_id"]
    index["next_id"] += 1

    content = args.content
    tags = args.tags.split(",") if args.tags else []

    # 파일 생성
    safe_title = args.title.replace(" ", "_")[:20]
    filename = f"memo_{memo_id:04d}_{safe_title}.txt"
    filepath = MEMO_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"제목: {args.title}\n")
        f.write(f"작성일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        if tags:
            f.write(f"태그: {', '.join('#' + t for t in tags)}\n")
        f.write("-" * 40 + "\n")
        f.write(content + "\n")

    meta = {
        "id": memo_id,
        "title": args.title,
        "filename": filename,
        "tags": tags,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "char_count": len(content),
    }
    index["memos"].append(meta)
    _save_memo_index(index)

    print(f"  [메모 저장] #{memo_id} '{args.title}' ({len(content)}자)")


def cmd_memo_list(args):
    """메모 목록을 표시합니다."""
    index = _load_memo_index()
    memos = index.get("memos", [])

    if not memos:
        print("  저장된 메모가 없습니다.")
        return

    print(f"\n  ── 메모 목록 ({len(memos)}건) ──")
    for m in memos:
        tags = " ".join(f"#{t}" for t in m.get("tags", []))
        print(f"  #{m['id']:>3} | {m['title']} | {m['created_at'][:10]} | {tags}")
    print()


def cmd_memo_read(args):
    """메모 내용을 읽습니다."""
    index = _load_memo_index()
    for m in index.get("memos", []):
        if m["id"] == args.id:
            filepath = MEMO_DIR / m["filename"]
            if filepath.exists():
                print(f"\n  {'=' * 40}")
                with open(filepath, "r", encoding="utf-8") as f:
                    for line in f:
                        print(f"  {line}", end="")
                print(f"\n  {'=' * 40}")
            else:
                print(f"  [오류] 파일이 존재하지 않습니다: {filepath}")
            return
    print(f"  [오류] 메모 #{args.id}을(를) 찾을 수 없습니다.")


def cmd_memo_search(args):
    """메모를 검색합니다."""
    index = _load_memo_index()
    keyword = args.keyword.lower()
    results = []

    for m in index.get("memos", []):
        if keyword in m["title"].lower():
            results.append(m)
            continue
        filepath = MEMO_DIR / m["filename"]
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                if keyword in f.read().lower():
                    results.append(m)

    print(f"\n  ── '{args.keyword}' 검색 결과 ({len(results)}건) ──")
    for m in results:
        print(f"  #{m['id']:>3} | {m['title']} | {m['created_at'][:10]}")
    print()


def cmd_memo_delete(args):
    """메모를 삭제합니다."""
    index = _load_memo_index()
    for i, m in enumerate(index.get("memos", [])):
        if m["id"] == args.id:
            filepath = MEMO_DIR / m["filename"]
            if filepath.exists():
                os.remove(filepath)
            index["memos"].pop(i)
            _save_memo_index(index)
            print(f"  [삭제 완료] 메모 #{args.id} '{m['title']}'")
            return
    print(f"  [오류] 메모 #{args.id}을(를) 찾을 수 없습니다.")


# ══════════════════════════════════════════════════════════════════════════
# 알림 관련 명령어
# ══════════════════════════════════════════════════════════════════════════

def cmd_timer(args):
    """카운트다운 타이머를 시작합니다."""
    import time as time_module

    seconds = args.seconds
    message = args.message

    print(f"\n  타이머 시작: {seconds}초")
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        print(f"  남은 시간: {mins:02d}:{secs:02d}", end="\r")
        time_module.sleep(1)

    print(f"  {'':30}", end="\r")
    print(f"  [타이머 완료] {message}")
    print()


# ══════════════════════════════════════════════════════════════════════════
# 유틸리티 명령어
# ══════════════════════════════════════════════════════════════════════════

def cmd_status(args):
    """개인 비서의 현재 상태를 요약합니다."""
    ensure_data_dir()

    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║       개인 비서 상태 요약             ║")
    print("  ╚══════════════════════════════════════╝")
    print(f"  현재 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 오늘 일정
    schedules = _load_schedules()
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_schedules = [s for s in schedules if s["date"] == today_str]
    pending = [s for s in today_schedules if not s.get("completed")]
    print(f"  [일정] 오늘: {len(today_schedules)}건 "
          f"(미완료: {len(pending)}건)")

    for s in pending:
        time_str = f" {s['time']}" if s.get('time') else ""
        print(f"    - {time_str} {s['title']}")

    # 메모 수
    index = _load_memo_index()
    memo_count = len(index.get("memos", []))
    print(f"  [메모] 저장됨: {memo_count}건")

    # 데이터 디렉토리 크기
    total_size = 0
    for f in DATA_DIR.rglob("*"):
        if f.is_file():
            total_size += f.stat().st_size
    print(f"  [저장소] {DATA_DIR}")
    print(f"           크기: {total_size:,} bytes")
    print()


# ══════════════════════════════════════════════════════════════════════════
# CLI 파서 구성
# ══════════════════════════════════════════════════════════════════════════

def build_parser():
    """argparse 파서를 구성합니다."""
    parser = argparse.ArgumentParser(
        prog="assistant",
        description="개인 비서 CLI - 일정, 메모, 날씨, 알림을 한 곳에서 관리하세요!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  %(prog)s weather --city 서울              # 서울 날씨 확인
  %(prog)s schedule add "회의" --date 2025-03-15 --time 10:00
  %(prog)s schedule list --today            # 오늘 일정 보기
  %(prog)s memo add "아이디어" --content "새 프로젝트 구상"
  %(prog)s memo search --keyword "프로젝트"  # 메모 검색
  %(prog)s timer 300 --message "휴식 시간!" # 5분 타이머
  %(prog)s status                           # 현재 상태 요약
        """
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="사용 가능한 명령어",
        description="아래 명령어 중 하나를 선택하세요"
    )

    # ── weather 서브커맨드 ──
    weather_parser = subparsers.add_parser(
        "weather", help="날씨 정보 확인",
        aliases=["w"]
    )
    weather_parser.add_argument(
        "--city", "-c", default="서울",
        help="도시 이름 (기본: 서울)"
    )
    weather_parser.add_argument(
        "--weekly", "-w", action="store_true",
        help="주간 예보 표시"
    )
    weather_parser.set_defaults(func=cmd_weather)

    # ── schedule 서브커맨드 ──
    schedule_parser = subparsers.add_parser(
        "schedule", help="일정 관리",
        aliases=["s"]
    )
    schedule_sub = schedule_parser.add_subparsers(dest="schedule_cmd")

    # schedule add
    s_add = schedule_sub.add_parser("add", help="일정 추가")
    s_add.add_argument("title", help="일정 제목")
    s_add.add_argument("--date", "-d", required=True, help="날짜 (YYYY-MM-DD)")
    s_add.add_argument("--time", "-t", default="", help="시간 (HH:MM)")
    s_add.add_argument("--category", "-c", default="일반",
                       choices=["일반", "업무", "개인", "약속", "운동", "공부"],
                       help="카테고리")
    s_add.set_defaults(func=cmd_schedule_add)

    # schedule list
    s_list = schedule_sub.add_parser("list", help="일정 목록")
    s_list.add_argument("--today", action="store_true", help="오늘 일정만")
    s_list.add_argument("--week", action="store_true", help="이번 주 일정만")
    s_list.set_defaults(func=cmd_schedule_list)

    # schedule done
    s_done = schedule_sub.add_parser("done", help="일정 완료 처리")
    s_done.add_argument("id", type=int, help="일정 ID")
    s_done.set_defaults(func=cmd_schedule_done)

    # schedule delete
    s_del = schedule_sub.add_parser("delete", help="일정 삭제")
    s_del.add_argument("id", type=int, help="일정 ID")
    s_del.set_defaults(func=cmd_schedule_delete)

    # ── memo 서브커맨드 ──
    memo_parser = subparsers.add_parser(
        "memo", help="메모 관리",
        aliases=["m"]
    )
    memo_sub = memo_parser.add_subparsers(dest="memo_cmd")

    # memo add
    m_add = memo_sub.add_parser("add", help="메모 작성")
    m_add.add_argument("title", help="메모 제목")
    m_add.add_argument("--content", "-c", required=True, help="메모 내용")
    m_add.add_argument("--tags", "-t", default="", help="태그 (콤마 구분)")
    m_add.set_defaults(func=cmd_memo_add)

    # memo list
    m_list = memo_sub.add_parser("list", help="메모 목록")
    m_list.set_defaults(func=cmd_memo_list)

    # memo read
    m_read = memo_sub.add_parser("read", help="메모 읽기")
    m_read.add_argument("id", type=int, help="메모 ID")
    m_read.set_defaults(func=cmd_memo_read)

    # memo search
    m_search = memo_sub.add_parser("search", help="메모 검색")
    m_search.add_argument("--keyword", "-k", required=True, help="검색 키워드")
    m_search.set_defaults(func=cmd_memo_search)

    # memo delete
    m_del = memo_sub.add_parser("delete", help="메모 삭제")
    m_del.add_argument("id", type=int, help="메모 ID")
    m_del.set_defaults(func=cmd_memo_delete)

    # ── timer 서브커맨드 ──
    timer_parser = subparsers.add_parser(
        "timer", help="카운트다운 타이머",
        aliases=["t"]
    )
    timer_parser.add_argument(
        "seconds", type=int,
        help="타이머 시간 (초)"
    )
    timer_parser.add_argument(
        "--message", "-m", default="타이머 종료!",
        help="완료 메시지"
    )
    timer_parser.set_defaults(func=cmd_timer)

    # ── status 서브커맨드 ──
    status_parser = subparsers.add_parser(
        "status", help="상태 요약"
    )
    status_parser.set_defaults(func=cmd_status)

    return parser


# ══════════════════════════════════════════════════════════════════════════
# 데모 모드
# ══════════════════════════════════════════════════════════════════════════

def run_demo():
    """인수 없이 실행 시 데모 모드를 실행합니다."""
    import shutil

    print("=" * 55)
    print("  개인 비서 CLI - 통합 명령어 데모")
    print("=" * 55)

    # 기존 데모 데이터 초기화
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    ensure_data_dir()

    parser = build_parser()

    # 데모 시나리오: 하루 동안의 개인 비서 활용
    demo_commands = [
        ("1. 날씨 확인", ["weather", "--city", "서울"]),
        ("2. 주간 날씨 확인", ["weather", "--city", "서울", "--weekly"]),
        ("3. 오늘 일정 추가 - 팀 회의",
         ["schedule", "add", "팀 회의",
          "--date", datetime.now().strftime("%Y-%m-%d"),
          "--time", "10:00", "--category", "업무"]),
        ("4. 오늘 일정 추가 - 점심 약속",
         ["schedule", "add", "점심 약속",
          "--date", datetime.now().strftime("%Y-%m-%d"),
          "--time", "12:30", "--category", "약속"]),
        ("5. 내일 일정 추가 - 스터디",
         ["schedule", "add", "Python 스터디",
          "--date", (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
          "--time", "19:00", "--category", "공부"]),
        ("6. 오늘 일정 보기", ["schedule", "list", "--today"]),
        ("7. 전체 일정 보기", ["schedule", "list"]),
        ("8. 메모 추가 - 아이디어",
         ["memo", "add", "프로젝트 아이디어",
          "--content", "바이브 코딩으로 개인 비서 앱 만들기",
          "--tags", "프로젝트,아이디어"]),
        ("9. 메모 추가 - 학습 노트",
         ["memo", "add", "학습 노트",
          "--content", "argparse로 CLI 서브커맨드 구현 완료",
          "--tags", "학습,파이썬"]),
        ("10. 메모 목록 보기", ["memo", "list"]),
        ("11. 메모 검색", ["memo", "search", "--keyword", "프로젝트"]),
        ("12. 메모 읽기", ["memo", "read", "1"]),
        ("13. 일정 완료 처리", ["schedule", "done", "1"]),
        ("14. 상태 요약", ["status"]),
    ]

    for step_name, cmd_args in demo_commands:
        print(f"\n{'─' * 55}")
        print(f"  >>> assistant {' '.join(cmd_args)}")
        print(f"  [{step_name}]")
        print(f"{'─' * 55}")

        args = parser.parse_args(cmd_args)
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()

    print(f"\n{'=' * 55}")
    print("  통합 명령어 데모가 완료되었습니다!")
    print()
    print("  실제 사용법:")
    print("    python ex29_05_unified_commands.py weather --city 부산")
    print("    python ex29_05_unified_commands.py schedule list --today")
    print("    python ex29_05_unified_commands.py memo add '메모' -c '내용'")
    print("    python ex29_05_unified_commands.py timer 60 -m '1분 완료!'")
    print("    python ex29_05_unified_commands.py status")
    print("    python ex29_05_unified_commands.py --help")
    print(f"{'=' * 55}")


# ══════════════════════════════════════════════════════════════════════════
# 메인 실행
# ══════════════════════════════════════════════════════════════════════════

def main():
    """메인 진입점: 인수가 있으면 CLI 모드, 없으면 데모 모드로 실행합니다."""
    # 커맨드라인 인수가 없으면 데모 모드
    if len(sys.argv) == 1:
        run_demo()
        return

    ensure_data_dir()
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
