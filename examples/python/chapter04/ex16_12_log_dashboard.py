#!/usr/bin/env python3
"""예제 16-12: 로그 통계 대시보드

서버 로그 데이터를 파싱하고 통계를 포매팅된 표로 출력합니다.
"""

import json
from collections import Counter, defaultdict
from datetime import datetime

# 서버 로그 데이터 (JSON Lines 형태)
log_data = """{"timestamp": "2024-10-01 09:15:23", "level": "INFO", "endpoint": "/api/users", "method": "GET", "status": 200, "response_ms": 45}
{"timestamp": "2024-10-01 09:15:45", "level": "INFO", "endpoint": "/api/products", "method": "GET", "status": 200, "response_ms": 82}
{"timestamp": "2024-10-01 09:16:02", "level": "WARNING", "endpoint": "/api/orders", "method": "POST", "status": 400, "response_ms": 120}
{"timestamp": "2024-10-01 09:16:30", "level": "INFO", "endpoint": "/api/users", "method": "POST", "status": 201, "response_ms": 95}
{"timestamp": "2024-10-01 09:17:15", "level": "ERROR", "endpoint": "/api/payment", "method": "POST", "status": 500, "response_ms": 3500}
{"timestamp": "2024-10-01 09:18:00", "level": "INFO", "endpoint": "/api/products", "method": "GET", "status": 200, "response_ms": 55}
{"timestamp": "2024-10-01 09:18:30", "level": "INFO", "endpoint": "/api/users", "method": "GET", "status": 200, "response_ms": 38}
{"timestamp": "2024-10-01 09:19:05", "level": "WARNING", "endpoint": "/api/auth", "method": "POST", "status": 401, "response_ms": 25}
{"timestamp": "2024-10-01 09:19:45", "level": "INFO", "endpoint": "/api/products", "method": "GET", "status": 200, "response_ms": 67}
{"timestamp": "2024-10-01 09:20:10", "level": "ERROR", "endpoint": "/api/payment", "method": "POST", "status": 500, "response_ms": 4200}
{"timestamp": "2024-10-01 09:20:30", "level": "INFO", "endpoint": "/api/orders", "method": "GET", "status": 200, "response_ms": 110}
{"timestamp": "2024-10-01 09:21:00", "level": "INFO", "endpoint": "/api/users", "method": "GET", "status": 200, "response_ms": 42}
{"timestamp": "2024-10-01 09:21:30", "level": "WARNING", "endpoint": "/api/auth", "method": "POST", "status": 403, "response_ms": 18}
{"timestamp": "2024-10-01 09:22:00", "level": "INFO", "endpoint": "/api/products", "method": "PUT", "status": 200, "response_ms": 78}
{"timestamp": "2024-10-01 09:22:30", "level": "INFO", "endpoint": "/api/orders", "method": "POST", "status": 201, "response_ms": 135}
{"timestamp": "2024-10-01 09:23:00", "level": "ERROR", "endpoint": "/api/payment", "method": "POST", "status": 502, "response_ms": 5000}
{"timestamp": "2024-10-01 09:23:30", "level": "INFO", "endpoint": "/api/users", "method": "DELETE", "status": 204, "response_ms": 60}
{"timestamp": "2024-10-01 09:24:00", "level": "INFO", "endpoint": "/api/products", "method": "GET", "status": 200, "response_ms": 48}
{"timestamp": "2024-10-01 09:24:30", "level": "INFO", "endpoint": "/api/orders", "method": "GET", "status": 200, "response_ms": 95}
{"timestamp": "2024-10-01 09:25:00", "level": "WARNING", "endpoint": "/api/auth", "method": "POST", "status": 429, "response_ms": 12}
"""

# 로그 파싱
logs = []
for line in log_data.strip().split("\n"):
    logs.append(json.loads(line))

def box_line(text, width=58):
    return "║ " + text.ljust(width - 4) + " ║"

# ===== 대시보드 헤더 =====
print("╔" + "═" * 56 + "╗")
print("║" + "서버 로그 통계 대시보드".center(44) + "║")
print("║" + f"  분석 기간: {logs[0]['timestamp'][:10]}".ljust(56) + "║")
print("║" + f"  총 로그 수: {len(logs)}건".ljust(56) + "║")
print("╠" + "═" * 56 + "╣")

# ===== 1. 로그 레벨 분포 =====
level_counter = Counter(log["level"] for log in logs)
level_icons = {"INFO": "●", "WARNING": "▲", "ERROR": "✖"}

print("║" + "  [로그 레벨 분포]".ljust(56) + "║")
print("║" + " " * 56 + "║")
for level in ["INFO", "WARNING", "ERROR"]:
    count = level_counter.get(level, 0)
    pct = count / len(logs) * 100
    bar_len = int(pct / 100 * 30)
    bar = "█" * bar_len + "░" * (30 - bar_len)
    icon = level_icons.get(level, " ")
    line = f"  {icon} {level:<8} {bar} {count:>2}건 ({pct:.0f}%)"
    print("║" + line.ljust(56) + "║")

print("╠" + "═" * 56 + "╣")

# ===== 2. 엔드포인트별 통계 =====
endpoint_stats = defaultdict(lambda: {"count": 0, "total_ms": 0, "errors": 0, "methods": Counter()})
for log in logs:
    ep = log["endpoint"]
    endpoint_stats[ep]["count"] += 1
    endpoint_stats[ep]["total_ms"] += log["response_ms"]
    endpoint_stats[ep]["methods"][log["method"]] += 1
    if log["status"] >= 400:
        endpoint_stats[ep]["errors"] += 1

print("║" + "  [엔드포인트별 통계]".ljust(56) + "║")
print("║" + " " * 56 + "║")
header = f"  {'엔드포인트':<18} {'요청':>4} {'오류':>4} {'평균ms':>8} {'메서드'}"
print("║" + header.ljust(56) + "║")
print("║" + ("  " + "-" * 52).ljust(56) + "║")

for ep, stats in sorted(endpoint_stats.items()):
    avg_ms = stats["total_ms"] / stats["count"]
    methods = ", ".join(f"{m}" for m, _ in stats["methods"].most_common())
    line = f"  {ep:<18} {stats['count']:>4} {stats['errors']:>4} {avg_ms:>7.0f} {methods}"
    print("║" + line.ljust(56) + "║")

print("╠" + "═" * 56 + "╣")

# ===== 3. HTTP 상태 코드 분포 =====
status_counter = Counter(log["status"] for log in logs)
status_desc = {200: "OK", 201: "Created", 204: "No Content", 400: "Bad Request",
               401: "Unauthorized", 403: "Forbidden", 429: "Too Many", 500: "Server Error", 502: "Bad Gateway"}

print("║" + "  [HTTP 상태 코드 분포]".ljust(56) + "║")
print("║" + " " * 56 + "║")
for status, count in sorted(status_counter.items()):
    desc = status_desc.get(status, "Unknown")
    bar = "█" * (count * 2)
    category = "✓" if status < 300 else ("▲" if status < 500 else "✖")
    line = f"  {category} {status} {desc:<14} {bar} {count}건"
    print("║" + line.ljust(56) + "║")

print("╠" + "═" * 56 + "╣")

# ===== 4. 응답 시간 분석 =====
response_times = [log["response_ms"] for log in logs]
print("║" + "  [응답 시간 분석]".ljust(56) + "║")
print("║" + " " * 56 + "║")

stats_lines = [
    f"  평균 응답 시간  : {sum(response_times) / len(response_times):>8.0f} ms",
    f"  중앙값          : {sorted(response_times)[len(response_times)//2]:>8} ms",
    f"  최소 응답 시간  : {min(response_times):>8} ms",
    f"  최대 응답 시간  : {max(response_times):>8} ms",
]
for line in stats_lines:
    print("║" + line.ljust(56) + "║")

# 응답 시간 분포
print("║" + " " * 56 + "║")
print("║" + "  응답 시간 분포:".ljust(56) + "║")
ranges = [
    ("0-50ms", 0, 50),
    ("51-100ms", 51, 100),
    ("101-500ms", 101, 500),
    ("500ms+", 500, 99999)
]
for label, low, high in ranges:
    count = sum(1 for t in response_times if low <= t <= high)
    bar = "█" * (count * 2)
    line = f"  {label:<10} {bar} {count}건"
    print("║" + line.ljust(56) + "║")

print("╠" + "═" * 56 + "╣")

# ===== 5. 경고 및 알림 =====
print("║" + "  [경고 및 알림]".ljust(56) + "║")
print("║" + " " * 56 + "║")

# 오류율 확인
error_count = sum(1 for log in logs if log["status"] >= 500)
error_rate = error_count / len(logs) * 100
if error_rate > 10:
    alert = f"  !! 높은 오류율: {error_rate:.1f}% (임계값: 10%)"
else:
    alert = f"  ○  오류율 정상: {error_rate:.1f}% (임계값: 10%)"
print("║" + alert.ljust(56) + "║")

# 느린 응답 확인
slow_requests = [log for log in logs if log["response_ms"] > 1000]
if slow_requests:
    line = f"  !! 느린 요청 {len(slow_requests)}건 감지 (>1000ms):"
    print("║" + line.ljust(56) + "║")
    for req in slow_requests:
        line = f"     {req['endpoint']} - {req['response_ms']}ms ({req['status']})"
        print("║" + line.ljust(56) + "║")
else:
    print("║" + "  ○  모든 요청 정상 응답 시간".ljust(56) + "║")

# 반복 오류 확인
error_endpoints = Counter(log["endpoint"] for log in logs if log["status"] >= 500)
if error_endpoints:
    print("║" + " " * 56 + "║")
    print("║" + "  반복 오류 엔드포인트:".ljust(56) + "║")
    for ep, count in error_endpoints.most_common():
        line = f"     {ep}: {count}회 오류"
        print("║" + line.ljust(56) + "║")

print("╚" + "═" * 56 + "╝")
