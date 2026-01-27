"""
예제 15-10: 로그 파일 분석기
로그 파일을 파싱하여 오류와 경고를 분석합니다.
"""
import tempfile
import os
import re
from collections import Counter, defaultdict

# --- 샘플 로그 데이터 생성 ---
temp_dir = tempfile.mkdtemp()
log_path = os.path.join(temp_dir, "app.log")

log_lines = """2024-03-15 08:00:01 [INFO] 서버가 시작되었습니다. 포트: 8080
2024-03-15 08:00:02 [INFO] 데이터베이스 연결 성공
2024-03-15 08:01:15 [INFO] 사용자 로그인: user_001
2024-03-15 08:02:30 [WARNING] 메모리 사용량 80% 초과
2024-03-15 08:03:45 [INFO] API 요청 처리: /api/users (200)
2024-03-15 08:04:12 [ERROR] 파일을 찾을 수 없습니다: /data/config.yml
2024-03-15 08:05:00 [INFO] 사용자 로그인: user_002
2024-03-15 08:05:30 [WARNING] API 응답 시간 초과: 3.2초
2024-03-15 08:06:00 [INFO] API 요청 처리: /api/products (200)
2024-03-15 08:06:45 [ERROR] 데이터베이스 쿼리 실패: timeout
2024-03-15 08:07:15 [INFO] 사용자 로그인: user_003
2024-03-15 08:08:00 [WARNING] 디스크 사용량 90% 초과
2024-03-15 08:08:30 [INFO] API 요청 처리: /api/orders (200)
2024-03-15 08:09:00 [ERROR] 인증 실패: 잘못된 토큰
2024-03-15 08:09:15 [INFO] 사용자 로그아웃: user_001
2024-03-15 08:10:00 [CRITICAL] 서버 메모리 부족! 긴급 조치 필요
2024-03-15 08:10:30 [WARNING] 연결 풀 고갈 경고
2024-03-15 08:11:00 [INFO] 캐시 초기화 완료
2024-03-15 08:11:30 [ERROR] 외부 API 호출 실패: connection refused
2024-03-15 08:12:00 [INFO] 사용자 로그인: user_004
2024-03-15 08:12:30 [INFO] API 요청 처리: /api/users (200)
2024-03-15 08:13:00 [WARNING] 느린 쿼리 감지: 2.8초
2024-03-15 08:13:30 [ERROR] 파일 쓰기 실패: 권한 부족
2024-03-15 08:14:00 [INFO] 백업 작업 시작
2024-03-15 08:14:30 [INFO] 백업 완료: 150MB
"""

with open(log_path, "w", encoding="utf-8") as f:
    f.write(log_lines.strip())

print("=" * 60)
print("로그 파일 분석기")
print("=" * 60)

# --- 로그 파싱 ---
log_pattern = re.compile(
    r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+\[(\w+)\]\s+(.*)"
)

entries = []
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        match = log_pattern.match(line)
        if match:
            date, time, level, message = match.groups()
            entries.append({
                "date": date,
                "time": time,
                "level": level,
                "message": message,
            })

print(f"\n총 로그 항목: {len(entries)}개\n")

# --- 로그 레벨별 통계 ---
print("-" * 60)
print("1. 로그 레벨별 통계")
print("-" * 60)
level_counts = Counter(e["level"] for e in entries)
level_order = ["CRITICAL", "ERROR", "WARNING", "INFO"]

for level in level_order:
    count = level_counts.get(level, 0)
    pct = (count / len(entries)) * 100
    bar = "#" * int(pct)
    print(f"  {level:>10s}: {count:>3}개 ({pct:5.1f}%) {bar}")

# --- 오류 메시지 상세 ---
print()
print("-" * 60)
print("2. 오류(ERROR) 상세 목록")
print("-" * 60)
errors = [e for e in entries if e["level"] == "ERROR"]
for i, err in enumerate(errors, 1):
    print(f"  [{i}] {err['time']} - {err['message']}")

# --- 경고 메시지 상세 ---
print()
print("-" * 60)
print("3. 경고(WARNING) 상세 목록")
print("-" * 60)
warnings = [e for e in entries if e["level"] == "WARNING"]
for i, warn in enumerate(warnings, 1):
    print(f"  [{i}] {warn['time']} - {warn['message']}")

# --- 심각(CRITICAL) 메시지 ---
print()
print("-" * 60)
print("4. 심각(CRITICAL) 이벤트")
print("-" * 60)
criticals = [e for e in entries if e["level"] == "CRITICAL"]
if criticals:
    for c in criticals:
        print(f"  *** {c['time']} - {c['message']} ***")
else:
    print("  심각한 이벤트 없음")

# --- 시간대별 분석 ---
print()
print("-" * 60)
print("5. 시간대별 이벤트 분포")
print("-" * 60)
hour_minute = defaultdict(int)
for e in entries:
    hm = e["time"][:5]  # HH:MM
    hour_minute[hm] += 1

for time_key in sorted(hour_minute.keys()):
    count = hour_minute[time_key]
    bar = "*" * count
    print(f"  {time_key} : {bar} ({count})")

# --- 요약 보고서 ---
print()
print("=" * 60)
print("분석 요약 보고서")
print("=" * 60)
print(f"  분석 기간: {entries[0]['date']}")
print(f"  시작 시간: {entries[0]['time']}")
print(f"  종료 시간: {entries[-1]['time']}")
print(f"  총 이벤트: {len(entries)}건")
print(f"  오류 비율: {len(errors)/len(entries)*100:.1f}%")
print(f"  경고 비율: {len(warnings)/len(entries)*100:.1f}%")
if criticals:
    print(f"  *** 심각 이벤트 {len(criticals)}건 발생! 즉시 확인 필요 ***")

# 정리
os.remove(log_path)
os.rmdir(temp_dir)
print()
print("로그 파일 분석기 예제를 성공적으로 완료했습니다!")
