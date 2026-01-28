#!/usr/bin/env python3
"""
예제 29-04: 알림 기능
- sched 모듈을 사용한 시간 기반 알림
- 데모용 짧은 타이머 (1~5초)
- 반복 알림 지원
- JSON 기반 알림 저장/불러오기
"""

import sched
import time
import json
import threading
from datetime import datetime, timedelta
from pathlib import Path


# ── 설정 ─────────────────────────────────────────────────────────────────

REMINDER_FILE = Path("/tmp/personal_assistant_reminders.json")


# ── 알림 관리 클래스 ─────────────────────────────────────────────────────

class ReminderManager:
    """sched 모듈 기반 알림 관리 클래스"""

    def __init__(self, filepath=REMINDER_FILE):
        """
        알림 관리자를 초기화합니다.

        Args:
            filepath: 알림 데이터를 저장할 파일 경로
        """
        self.filepath = Path(filepath)
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.reminders = []
        self.reminder_history = []  # 완료된 알림 기록
        self._next_id = 1

    def add_reminder(self, message, delay_seconds, priority=1, repeat=0):
        """
        새 알림을 등록합니다.

        Args:
            message: 알림 메시지
            delay_seconds: 지금부터 N초 후에 알림
            priority: 우선순위 (1이 가장 높음)
            repeat: 반복 횟수 (0이면 1회만 실행)

        Returns:
            dict: 등록된 알림 정보
        """
        reminder_id = self._next_id
        self._next_id += 1

        trigger_time = time.time() + delay_seconds
        trigger_datetime = datetime.fromtimestamp(trigger_time)

        reminder = {
            "id": reminder_id,
            "message": message,
            "delay_seconds": delay_seconds,
            "priority": priority,
            "repeat": repeat,
            "repeat_remaining": repeat,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "trigger_at": trigger_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "대기 중",
        }

        # sched에 이벤트 등록
        event = self.scheduler.enter(
            delay_seconds,
            priority,
            self._trigger_reminder,
            argument=(reminder,)
        )
        reminder["_event"] = event  # 취소를 위해 이벤트 참조 저장

        self.reminders.append(reminder)
        print(f"  [알림 등록] #{reminder_id} '{message}' "
              f"({delay_seconds}초 후, 우선순위: {priority})")
        return reminder

    def add_reminder_at(self, message, target_time_str, priority=1):
        """
        특정 시간에 알림을 등록합니다 (HH:MM 형식).

        Args:
            message: 알림 메시지
            target_time_str: 목표 시간 (HH:MM)
            priority: 우선순위

        Returns:
            dict 또는 None: 등록된 알림 정보
        """
        try:
            now = datetime.now()
            target = datetime.strptime(target_time_str, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )
            # 이미 지난 시간이면 내일로 설정
            if target <= now:
                target += timedelta(days=1)

            delay = (target - now).total_seconds()
            print(f"  목표 시간: {target.strftime('%Y-%m-%d %H:%M')} "
                  f"(약 {delay:.0f}초 후)")
            return self.add_reminder(message, delay, priority)
        except ValueError:
            print(f"  [오류] 잘못된 시간 형식: {target_time_str} (HH:MM 필요)")
            return None

    def cancel_reminder(self, reminder_id):
        """
        등록된 알림을 취소합니다.

        Args:
            reminder_id: 취소할 알림 ID

        Returns:
            bool: 취소 성공 여부
        """
        for reminder in self.reminders:
            if reminder["id"] == reminder_id and reminder["status"] == "대기 중":
                try:
                    self.scheduler.cancel(reminder["_event"])
                    reminder["status"] = "취소됨"
                    print(f"  [알림 취소] #{reminder_id} '{reminder['message']}'")
                    return True
                except ValueError:
                    print(f"  [오류] 알림 #{reminder_id}은(는) 이미 처리되었습니다.")
                    return False

        print(f"  [오류] 알림 #{reminder_id}을(를) 찾을 수 없습니다.")
        return False

    def _trigger_reminder(self, reminder):
        """
        알림이 발동될 때 호출되는 콜백 함수입니다.

        Args:
            reminder: 발동된 알림 정보
        """
        now = datetime.now().strftime("%H:%M:%S")
        priority_label = {1: "긴급", 2: "중요", 3: "일반"}.get(
            reminder["priority"], "일반"
        )

        # 알림 출력
        print()
        print("  " + "*" * 50)
        print(f"  *  REMINDER [{priority_label}] - {now}")
        print(f"  *  {reminder['message']}")
        print("  " + "*" * 50)

        # 상태 업데이트
        reminder["status"] = "완료"
        reminder["completed_at"] = now

        # 기록에 추가
        history_entry = {
            "id": reminder["id"],
            "message": reminder["message"],
            "triggered_at": now,
            "priority": reminder["priority"],
        }
        self.reminder_history.append(history_entry)

        # 반복 알림 처리
        if reminder["repeat_remaining"] > 0:
            reminder["repeat_remaining"] -= 1
            print(f"  (반복 알림: {reminder['repeat_remaining'] + 1}회 남음, "
                  f"{reminder['delay_seconds']}초 후 다시 알림)")

            # 새 이벤트 등록
            new_event = self.scheduler.enter(
                reminder["delay_seconds"],
                reminder["priority"],
                self._trigger_reminder,
                argument=(reminder,)
            )
            reminder["_event"] = new_event
            reminder["status"] = "대기 중 (반복)"

    def run(self, blocking=True):
        """
        스케줄러를 실행하여 등록된 알림을 처리합니다.

        Args:
            blocking: True면 모든 알림이 완료될 때까지 차단
        """
        pending_count = len([
            r for r in self.reminders if r["status"].startswith("대기")
        ])
        if pending_count == 0:
            print("  대기 중인 알림이 없습니다.")
            return

        print(f"\n  스케줄러 시작... ({pending_count}개 알림 대기 중)")
        print(f"  현재 시각: {datetime.now().strftime('%H:%M:%S')}")
        print("  " + "-" * 40)

        if blocking:
            self.scheduler.run()
            print("  " + "-" * 40)
            print("  모든 알림이 처리되었습니다.")
        else:
            # 비차단 모드: 별도 스레드에서 실행
            thread = threading.Thread(target=self.scheduler.run, daemon=True)
            thread.start()
            return thread

    def list_reminders(self):
        """등록된 모든 알림을 표시합니다."""
        print()
        print(f"  ── 알림 목록 (총 {len(self.reminders)}개) ──")

        if not self.reminders:
            print("  등록된 알림이 없습니다.")
            print()
            return

        priority_label = {1: "긴급", 2: "중요", 3: "일반"}

        for r in self.reminders:
            p = priority_label.get(r["priority"], "일반")
            status_icon = {
                "대기 중": "[대기]",
                "대기 중 (반복)": "[반복]",
                "완료": "[완료]",
                "취소됨": "[취소]",
            }.get(r["status"], "[???]")

            print(f"  #{r['id']:>2} {status_icon} [{p}] {r['message']}")
            print(f"      예정: {r['trigger_at']} | "
                  f"생성: {r['created_at']}")
            if r.get("completed_at"):
                print(f"      완료: {r['completed_at']}")
        print()

    def list_history(self):
        """알림 실행 기록을 표시합니다."""
        print()
        print(f"  ── 알림 기록 ({len(self.reminder_history)}건) ──")
        if not self.reminder_history:
            print("  아직 기록이 없습니다.")
        else:
            for h in self.reminder_history:
                p = {1: "긴급", 2: "중요", 3: "일반"}.get(h["priority"], "일반")
                print(f"  [{h['triggered_at']}] [{p}] {h['message']}")
        print()

    def save_reminders(self):
        """알림 데이터를 JSON 파일에 저장합니다."""
        data = {
            "reminders": [
                {k: v for k, v in r.items() if k != "_event"}
                for r in self.reminders
            ],
            "history": self.reminder_history,
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  [저장 완료] {self.filepath}")


# ── 편의 함수들 ──────────────────────────────────────────────────────────

def quick_timer(seconds, message="타이머 종료!"):
    """
    간단한 카운트다운 타이머입니다.

    Args:
        seconds: 대기 시간 (초)
        message: 완료 시 표시할 메시지
    """
    print(f"\n  타이머 시작: {seconds}초")
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer_display = f"{mins:02d}:{secs:02d}"
        print(f"  남은 시간: {timer_display}", end="\r")
        time.sleep(1)

    print(f"  {' ' * 25}", end="\r")  # 이전 줄 지우기
    print(f"  [타이머 완료] {message}")


def pomodoro_demo(work_seconds=3, break_seconds=2):
    """
    뽀모도로 타이머 데모 (짧은 시간으로 시연).

    Args:
        work_seconds: 작업 시간 (초, 데모용으로 짧게)
        break_seconds: 휴식 시간 (초, 데모용으로 짧게)
    """
    print("\n  ── 뽀모도로 타이머 (데모) ──")
    print(f"  작업: {work_seconds}초 / 휴식: {break_seconds}초")

    # 작업 시간
    print(f"\n  [작업 시작] 집중하세요!")
    for i in range(work_seconds, 0, -1):
        print(f"  작업 중... {i}초 남음", end="\r")
        time.sleep(1)
    print(f"  {'':25}", end="\r")
    print("  [작업 완료] 수고했습니다!")

    # 휴식 시간
    print(f"\n  [휴식 시작] 잠시 쉬세요!")
    for i in range(break_seconds, 0, -1):
        print(f"  휴식 중... {i}초 남음", end="\r")
        time.sleep(1)
    print(f"  {'':25}", end="\r")
    print("  [휴식 완료] 다시 시작할 준비가 되었습니다!")
    print()


# ── 메인 데모 ────────────────────────────────────────────────────────────

def main():
    """알림 기능 데모를 실행합니다."""
    print("=" * 55)
    print("  개인 비서 - 알림 기능 데모")
    print("=" * 55)
    print(f"  현재 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    manager = ReminderManager()

    # ── 1. 알림 등록 ──
    print("\n--- [1단계] 알림 등록 ---")

    # 짧은 간격으로 데모 알림 등록 (1~5초)
    manager.add_reminder("물 마시기 알림", delay_seconds=2, priority=3)
    manager.add_reminder("이메일 확인하세요!", delay_seconds=3, priority=2)
    manager.add_reminder("회의 10분 전입니다!", delay_seconds=1, priority=1)
    manager.add_reminder("스트레칭 시간", delay_seconds=4, priority=3, repeat=1)

    # 취소할 알림 등록 후 취소
    r5 = manager.add_reminder("취소될 알림", delay_seconds=5, priority=3)
    manager.cancel_reminder(r5["id"])

    # ── 2. 등록된 알림 확인 ──
    print("\n--- [2단계] 등록된 알림 확인 ---")
    manager.list_reminders()

    # ── 3. 스케줄러 실행 (알림 처리) ──
    print("\n--- [3단계] 알림 처리 시작 ---")
    print("  (데모를 위해 짧은 간격으로 설정, 약 8초 소요)")
    manager.run(blocking=True)

    # ── 4. 알림 기록 확인 ──
    print("\n--- [4단계] 알림 실행 기록 ---")
    manager.list_history()

    # ── 5. 최종 상태 확인 ──
    print("\n--- [5단계] 최종 알림 상태 ---")
    manager.list_reminders()

    # ── 6. 데이터 저장 ──
    print("\n--- [6단계] 알림 데이터 저장 ---")
    manager.save_reminders()

    # ── 7. 카운트다운 타이머 데모 ──
    print("\n--- [7단계] 카운트다운 타이머 ---")
    quick_timer(3, "타이머 데모 완료!")

    # ── 8. 뽀모도로 데모 ──
    print("\n--- [8단계] 뽀모도로 타이머 데모 ---")
    pomodoro_demo(work_seconds=2, break_seconds=1)

    print("  알림 기능 데모가 완료되었습니다!")


if __name__ == "__main__":
    main()
