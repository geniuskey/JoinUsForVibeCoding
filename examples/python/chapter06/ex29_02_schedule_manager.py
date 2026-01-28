#!/usr/bin/env python3
"""
예제 29-02: 일정 관리
- JSON 파일 기반 일정 CRUD (생성, 조회, 수정, 삭제)
- 오늘 일정 및 이번 주 일정 표시
- 반복 일정 지원
- /tmp/ 디렉토리에 데이터 저장
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import uuid


# ── 설정 ─────────────────────────────────────────────────────────────────

SCHEDULE_FILE = Path("/tmp/personal_assistant_schedule.json")


# ── 일정 데이터 관리 클래스 ────────────────────────────────────────────────

class ScheduleManager:
    """JSON 파일 기반 일정 관리 클래스"""

    def __init__(self, filepath=SCHEDULE_FILE):
        """
        일정 관리자를 초기화합니다.

        Args:
            filepath: 일정 데이터를 저장할 JSON 파일 경로
        """
        self.filepath = Path(filepath)
        self.schedules = self._load()

    def _load(self):
        """JSON 파일에서 일정 데이터를 불러옵니다."""
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print("[경고] 일정 파일이 손상되어 새로 시작합니다.")
                return []
        return []

    def _save(self):
        """일정 데이터를 JSON 파일에 저장합니다."""
        # 부모 디렉토리 생성
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.schedules, f, ensure_ascii=False, indent=2)

    # ── CRUD 연산 ─────────────────────────────────────────────

    def add(self, title, date_str, time_str="", description="", category="일반", repeat="없음"):
        """
        새 일정을 추가합니다.

        Args:
            title: 일정 제목
            date_str: 날짜 (YYYY-MM-DD)
            time_str: 시간 (HH:MM, 선택)
            description: 상세 설명 (선택)
            category: 분류 (일반, 업무, 개인, 약속 등)
            repeat: 반복 설정 (없음, 매일, 매주, 매월)

        Returns:
            dict: 생성된 일정 정보
        """
        # 날짜 형식 검증
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print(f"[오류] 잘못된 날짜 형식입니다: {date_str} (YYYY-MM-DD 형식 필요)")
            return None

        # 시간 형식 검증 (입력된 경우)
        if time_str:
            try:
                datetime.strptime(time_str, "%H:%M")
            except ValueError:
                print(f"[오류] 잘못된 시간 형식입니다: {time_str} (HH:MM 형식 필요)")
                return None

        schedule = {
            "id": str(uuid.uuid4())[:8],  # 짧은 고유 ID
            "title": title,
            "date": date_str,
            "time": time_str,
            "description": description,
            "category": category,
            "repeat": repeat,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed": False,
        }

        self.schedules.append(schedule)
        self._save()
        print(f"[추가 완료] '{title}' 일정이 추가되었습니다. (ID: {schedule['id']})")
        return schedule

    def get(self, schedule_id):
        """ID로 특정 일정을 조회합니다."""
        for s in self.schedules:
            if s["id"] == schedule_id:
                return s
        return None

    def update(self, schedule_id, **kwargs):
        """
        일정을 수정합니다.

        Args:
            schedule_id: 수정할 일정 ID
            **kwargs: 수정할 필드와 값 (title, date, time, description 등)

        Returns:
            dict 또는 None: 수정된 일정 정보
        """
        for i, s in enumerate(self.schedules):
            if s["id"] == schedule_id:
                allowed_fields = {"title", "date", "time", "description", "category", "repeat", "completed"}
                for key, value in kwargs.items():
                    if key in allowed_fields:
                        self.schedules[i][key] = value
                self.schedules[i]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save()
                print(f"[수정 완료] ID '{schedule_id}' 일정이 수정되었습니다.")
                return self.schedules[i]

        print(f"[오류] ID '{schedule_id}'에 해당하는 일정을 찾을 수 없습니다.")
        return None

    def delete(self, schedule_id):
        """일정을 삭제합니다."""
        for i, s in enumerate(self.schedules):
            if s["id"] == schedule_id:
                removed = self.schedules.pop(i)
                self._save()
                print(f"[삭제 완료] '{removed['title']}' 일정이 삭제되었습니다.")
                return removed

        print(f"[오류] ID '{schedule_id}'에 해당하는 일정을 찾을 수 없습니다.")
        return None

    def complete(self, schedule_id):
        """일정을 완료 처리합니다."""
        return self.update(schedule_id, completed=True)

    # ── 조회 및 필터링 ────────────────────────────────────────

    def get_today(self):
        """오늘 일정을 조회합니다."""
        today = datetime.now().strftime("%Y-%m-%d")
        return [s for s in self.schedules if s["date"] == today]

    def get_this_week(self):
        """이번 주 일정을 조회합니다 (월~일)."""
        today = datetime.now()
        # 이번 주 월요일 계산
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)

        monday_str = monday.strftime("%Y-%m-%d")
        sunday_str = sunday.strftime("%Y-%m-%d")

        return [
            s for s in self.schedules
            if monday_str <= s["date"] <= sunday_str
        ]

    def get_by_category(self, category):
        """카테고리별 일정을 조회합니다."""
        return [s for s in self.schedules if s["category"] == category]

    def get_upcoming(self, days=7):
        """향후 N일간의 일정을 조회합니다."""
        today = datetime.now().strftime("%Y-%m-%d")
        future = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        return [
            s for s in self.schedules
            if today <= s["date"] <= future
        ]

    def search(self, keyword):
        """키워드로 일정을 검색합니다."""
        keyword_lower = keyword.lower()
        return [
            s for s in self.schedules
            if keyword_lower in s["title"].lower()
            or keyword_lower in s.get("description", "").lower()
        ]

    def list_all(self):
        """모든 일정을 날짜순으로 정렬하여 반환합니다."""
        return sorted(self.schedules, key=lambda s: (s["date"], s.get("time", "")))


# ── 출력 함수들 ──────────────────────────────────────────────────────────

def display_schedules(schedules, title="일정 목록"):
    """일정 목록을 보기 좋게 출력합니다."""
    print()
    print(f"  ── {title} ({'총 ' + str(len(schedules)) + '건'}) ──")

    if not schedules:
        print("  등록된 일정이 없습니다.")
        print()
        return

    # 날짜별로 그룹핑
    by_date = {}
    for s in sorted(schedules, key=lambda x: (x["date"], x.get("time", ""))):
        date = s["date"]
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(s)

    category_icons = {
        "업무": "[업무]",
        "개인": "[개인]",
        "약속": "[약속]",
        "운동": "[운동]",
        "공부": "[공부]",
        "일반": "[일반]",
    }

    for date, items in by_date.items():
        # 요일 계산
        dt = datetime.strptime(date, "%Y-%m-%d")
        day_names = ["월", "화", "수", "목", "금", "토", "일"]
        day_name = day_names[dt.weekday()]

        print(f"\n  [{date} ({day_name})]")
        for s in items:
            status = "V" if s["completed"] else " "
            icon = category_icons.get(s["category"], "[기타]")
            time_str = f" {s['time']}" if s["time"] else ""
            completed_mark = " (완료)" if s["completed"] else ""

            print(f"    [{status}] {icon}{time_str} {s['title']}{completed_mark}")
            print(f"        ID: {s['id']}", end="")
            if s.get("description"):
                print(f" | {s['description']}", end="")
            if s["repeat"] != "없음":
                print(f" | 반복: {s['repeat']}", end="")
            print()

    print()


def display_schedule_detail(schedule):
    """단일 일정의 상세 정보를 출력합니다."""
    if not schedule:
        print("  일정을 찾을 수 없습니다.")
        return

    print()
    print(f"  ── 일정 상세 ──")
    print(f"  ID:       {schedule['id']}")
    print(f"  제목:     {schedule['title']}")
    print(f"  날짜:     {schedule['date']}")
    print(f"  시간:     {schedule['time'] or '미정'}")
    print(f"  분류:     {schedule['category']}")
    print(f"  설명:     {schedule.get('description', '없음')}")
    print(f"  반복:     {schedule['repeat']}")
    print(f"  완료:     {'예' if schedule['completed'] else '아니오'}")
    print(f"  생성일:   {schedule['created_at']}")
    if "updated_at" in schedule:
        print(f"  수정일:   {schedule['updated_at']}")
    print()


# ── 메인 데모 ────────────────────────────────────────────────────────────

def main():
    """일정 관리 기능 데모를 실행합니다."""
    print("=" * 55)
    print("  개인 비서 - 일정 관리 모듈 데모")
    print("=" * 55)

    # 기존 데모 데이터 초기화
    if SCHEDULE_FILE.exists():
        os.remove(SCHEDULE_FILE)

    manager = ScheduleManager()

    # ── 1. 일정 추가 (Create) ──
    print("\n--- [1단계] 일정 추가 ---")
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    tomorrow_str = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    day_after_str = (today + timedelta(days=2)).strftime("%Y-%m-%d")
    next_week_str = (today + timedelta(days=5)).strftime("%Y-%m-%d")

    s1 = manager.add("팀 회의", today_str, "10:00",
                      "2분기 계획 논의", "업무")
    s2 = manager.add("점심 약속", today_str, "12:30",
                      "홍길동님과 강남역", "약속")
    s3 = manager.add("헬스장 운동", today_str, "18:00",
                      "상체 운동일", "운동", repeat="매주")
    s4 = manager.add("Python 스터디", tomorrow_str, "19:00",
                      "Chapter 5 발표 준비", "공부", repeat="매주")
    s5 = manager.add("치과 예약", day_after_str, "14:00",
                      "정기 검진", "개인")
    s6 = manager.add("프로젝트 마감", next_week_str, "17:00",
                      "바이브 코딩 프로젝트 v1.0", "업무")

    # ── 2. 일정 조회 (Read) ──
    print("\n--- [2단계] 일정 조회 ---")

    # 오늘 일정
    today_schedules = manager.get_today()
    display_schedules(today_schedules, f"오늘의 일정 ({today_str})")

    # 이번 주 일정
    week_schedules = manager.get_this_week()
    display_schedules(week_schedules, "이번 주 일정")

    # 특정 일정 상세
    if s1:
        print("--- 특정 일정 상세 조회 ---")
        detail = manager.get(s1["id"])
        display_schedule_detail(detail)

    # ── 3. 일정 수정 (Update) ──
    print("\n--- [3단계] 일정 수정 ---")
    if s2:
        manager.update(s2["id"], time="13:00", description="홍길동님과 역삼역으로 변경")
        updated = manager.get(s2["id"])
        display_schedule_detail(updated)

    # ── 4. 일정 완료 처리 ──
    print("\n--- [4단계] 일정 완료 처리 ---")
    if s1:
        manager.complete(s1["id"])

    # ── 5. 카테고리별 조회 ──
    print("\n--- [5단계] 카테고리별 조회 ---")
    work_schedules = manager.get_by_category("업무")
    display_schedules(work_schedules, "업무 일정")

    # ── 6. 키워드 검색 ──
    print("\n--- [6단계] 키워드 검색 ---")
    results = manager.search("스터디")
    display_schedules(results, "'스터디' 검색 결과")

    # ── 7. 일정 삭제 (Delete) ──
    print("\n--- [7단계] 일정 삭제 ---")
    if s5:
        manager.delete(s5["id"])

    # ── 8. 최종 전체 일정 ──
    print("\n--- [최종] 전체 일정 ---")
    all_schedules = manager.list_all()
    display_schedules(all_schedules, "전체 일정")

    # 저장 파일 정보
    print(f"  데이터 저장 위치: {SCHEDULE_FILE}")
    if SCHEDULE_FILE.exists():
        size = SCHEDULE_FILE.stat().st_size
        print(f"  파일 크기: {size} bytes")
    print()
    print("  일정 관리 모듈 데모가 완료되었습니다!")


if __name__ == "__main__":
    main()
