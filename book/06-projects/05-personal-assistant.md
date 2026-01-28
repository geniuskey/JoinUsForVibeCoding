# Chapter 29: 프로젝트 5 - 개인 비서 CLI

터미널에서 날씨를 확인하고, 일정을 관리하고, 메모를 작성하고, 알림까지 받을 수 있는 나만의 개인 비서가 있다면 어떨까요? 이 프로젝트에서는 지금까지 배운 파이썬 기술을 총동원하여 **다기능 개인 비서 CLI 도구**를 만듭니다. 날씨 정보 조회, 일정 관리, 메모 작성, 알림 설정 등 실생활에서 바로 사용할 수 있는 기능들을 하나씩 구현하고, 마지막에 하나의 통합 CLI로 완성합니다.

---

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- 여러 모듈을 조합하여 **복합 CLI 애플리케이션**을 설계하고 구현할 수 있다
- `urllib`과 `json`을 사용하여 **외부 API 데이터**를 가져오고 표시할 수 있다
- JSON 파일 기반의 **CRUD(생성, 조회, 수정, 삭제)** 데이터 관리를 구현할 수 있다
- 텍스트 파일과 인덱스를 활용한 **메모 시스템**을 만들 수 있다
- `sched` 모듈로 **시간 기반 알림**을 구현할 수 있다
- `argparse` 서브커맨드로 여러 기능을 **하나의 CLI로 통합**할 수 있다
- `configparser`로 애플리케이션 **설정을 체계적으로 관리**할 수 있다
- AI와의 반복적 대화를 통해 프로젝트를 **점진적으로 확장**하는 방법을 체험할 수 있다

---

## 29.1 프로젝트 개요

### 무엇을 만드는가?

터미널에서 실행되는 개인 비서 CLI 도구를 만듭니다. 하나의 명령어로 다양한 기능에 접근할 수 있는 통합 도구입니다.

```
$ assistant weather --city 서울           # 날씨 확인
$ assistant schedule add "팀 회의" --date 2025-03-15
$ assistant memo add "아이디어" --content "새 프로젝트 구상"
$ assistant timer 300 --message "휴식!"   # 5분 타이머
$ assistant status                        # 상태 요약
```

### 프로젝트 구조

이 프로젝트는 6개의 단계로 나누어 점진적으로 완성합니다. 각 단계가 독립적인 모듈로 동작하며, 마지막에 하나로 통합됩니다.

```
personal_assistant/
├── weather_display.py      # 날씨 정보 표시
├── schedule_manager.py     # 일정 관리 (CRUD)
├── memo_feature.py         # 메모 기능
├── reminder.py             # 알림 기능
├── unified_commands.py     # 통합 CLI
├── config_manager.py       # 설정 관리
└── data/                   # 데이터 저장 디렉토리
    ├── schedules.json
    ├── memos/
    ├── reminders.json
    └── config/settings.ini
```

### 사용하는 표준 라이브러리

| 라이브러리 | 용도 |
|-----------|------|
| `urllib` | HTTP 요청 (날씨 API 호출) |
| `json` | 데이터 저장/불러오기 |
| `datetime` | 날짜/시간 처리 |
| `pathlib` | 파일 경로 관리 |
| `argparse` | CLI 인자 파싱 |
| `configparser` | 설정 파일 관리 |
| `sched` / `time` | 타이머 및 알림 스케줄링 |
| `uuid` | 고유 ID 생성 |
| `os` | 파일 시스템 작업 |

> **Note:** 이 프로젝트는 파이썬 표준 라이브러리만 사용합니다. 외부 패키지를 설치할 필요가 없으므로, 어떤 환경에서든 바로 실행할 수 있습니다.

### 요구사항 정리

AI에게 프로젝트를 요청하기 전에 요구사항을 명확히 정리하는 것이 중요합니다. 다음은 이 프로젝트의 핵심 요구사항입니다.

| 기능 | 핵심 요구사항 |
|------|-------------|
| 날씨 | 도시별 현재 날씨, 주간 예보, 기온 그래프 |
| 일정 | 일정 추가/조회/수정/삭제, 카테고리 분류, 반복 일정 |
| 메모 | 메모 작성/읽기/수정/삭제, 태그 분류, 키워드 검색 |
| 알림 | 시간 지정 알림, 카운트다운 타이머, 뽀모도로 |
| 통합 | argparse 서브커맨드, 상태 요약, 도움말 |
| 설정 | INI 파일 설정, 백업/복원, JSON 내보내기 |

> **Tip:** 프로젝트를 시작하기 전에 이처럼 요구사항을 표로 정리하면, AI에게 한 번에 전달하거나 단계별로 나누어 요청하기 쉬워집니다.

---

## 29.2 AI에게 프로젝트 설계 요청하기

프로젝트 전체를 한 번에 요청하기보다, 모듈 단위로 나누어 요청하는 것이 더 좋은 결과를 얻는 방법입니다. 다음은 이 프로젝트에서 사용할 프롬프트 전략입니다.

### 첫 번째 프롬프트: 전체 설계

```
파이썬 표준 라이브러리만 사용해서 개인 비서 CLI 도구를 만들고 싶어.
다음 기능이 필요해:
1. 날씨 정보 표시 (시뮬레이션 데이터 + 실제 API 호출)
2. 일정 관리 (JSON 파일 기반 CRUD)
3. 메모 기능 (텍스트 파일 기반, 태그 지원)
4. 알림 기능 (sched 모듈 사용)
5. argparse 서브커맨드로 전체 통합
6. configparser로 설정 관리

먼저 전체 프로젝트의 디렉토리 구조와 각 모듈의 역할을 설계해줘.
```

> **Tip:** "먼저 전체 설계를 해줘"라고 요청하면 AI가 코드를 바로 작성하지 않고 구조를 먼저 잡아줍니다. 설계를 확인한 후 각 모듈을 하나씩 구현하면 실수를 줄일 수 있습니다.

### 단계별 구현 전략

이 프로젝트에서는 각 기능을 독립 모듈로 먼저 만들고, 테스트한 후, 마지막에 통합합니다.

```
[1단계] 날씨 모듈 → 단독 테스트
[2단계] 일정 모듈 → 단독 테스트
[3단계] 메모 모듈 → 단독 테스트
[4단계] 알림 모듈 → 단독 테스트
[5단계] 통합 CLI → 모듈 연결 + 테스트
[6단계] 설정 관리 → 전체 설정 적용
```

이 방식의 장점은 각 모듈이 독립적으로 동작하므로, 문제가 생겼을 때 원인을 쉽게 찾을 수 있다는 것입니다.

---

## 29.3 예제 29-1: 날씨 정보 표시

첫 번째 모듈은 날씨 정보를 가져와 터미널에 표시하는 기능입니다. 네트워크가 없는 환경에서도 동작하도록 시뮬레이션 모드를 포함합니다.

### AI에게 요청하기

```
날씨 정보 모듈을 만들어줘. 요구사항:
- urllib로 실제 API 호출 가능 (Open-Meteo 무료 API)
- 네트워크 없이도 테스트할 수 있는 시뮬레이션 모드
- 현재 날씨 상세 표시 (기온, 습도, 풍속, 체감온도)
- 7일 주간 예보 테이블
- 텍스트 기반 기온 변화 그래프
- 날씨에 따른 외출 조언
파이썬 표준 라이브러리만 사용해줘.
```

### 핵심 코드 분석

날씨 모듈의 핵심은 데이터 소스를 유연하게 전환할 수 있는 구조입니다. 시뮬레이션 데이터와 실제 API를 동일한 인터페이스로 사용합니다.

**예제 29-1: 날씨 정보 표시**

```python
# examples/python/chapter06/ex29_01_weather_display.py
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
import random


# ── 시뮬레이션용 날씨 데이터 ──────────────────────────────────

def _generate_simulated_weather():
    """네트워크 없이 테스트할 수 있도록 시뮬레이션 날씨 데이터를 생성합니다."""
    conditions = [
        ("맑음", "☀️", (15, 28)),
        ("구름 조금", "⛅", (12, 25)),
        ("흐림", "☁️", (10, 22)),
        ("비", "🌧️", (8, 18)),
        ("소나기", "🌦️", (10, 20)),
        ("눈", "❄️", (-5, 3)),
    ]

    today = datetime.now()
    forecast = []

    for day_offset in range(7):
        date = today + timedelta(days=day_offset)
        condition_name, icon, temp_range = random.choice(conditions)
        low = random.randint(temp_range[0], temp_range[0] + 5)
        high = random.randint(temp_range[1] - 5, temp_range[1])
        humidity = random.randint(30, 90)

        forecast.append({
            "date": date.strftime("%Y-%m-%d"),
            "day_name": ["월", "화", "수", "목", "금", "토", "일"][date.weekday()],
            "condition": condition_name,
            "icon": icon,
            "temp_high": high,
            "temp_low": low,
            "humidity": humidity,
            "wind_speed": round(random.uniform(0.5, 15.0), 1),
        })

    return {
        "city": "서울",
        "country": "대한민국",
        "last_updated": today.strftime("%Y-%m-%d %H:%M"),
        "forecast": forecast,
    }
```

이 함수는 실제 날씨 데이터와 동일한 구조의 딕셔너리를 반환합니다. 중요한 설계 포인트는 다음과 같습니다:

1. **날씨 조건 리스트**: 이름, 아이콘, 기온 범위를 튜플로 관리합니다
2. **7일 예보 생성**: `timedelta`로 날짜를 순차적으로 생성합니다
3. **요일 계산**: `weekday()` 메서드로 한국어 요일을 매핑합니다

다음은 실제 API 호출과 시뮬레이션을 전환하는 함수입니다.

```python
def fetch_weather(city="서울", use_simulation=True):
    """
    날씨 정보를 가져옵니다.
    use_simulation=True이면 시뮬레이션, False이면 실제 API 호출
    """
    if use_simulation:
        print(f"[시뮬레이션 모드] '{city}' 날씨 데이터를 생성합니다...")
        data = _generate_simulated_weather()
        data["city"] = city
        return data

    # 실제 API 호출 (Open-Meteo 무료 API, API 키 불필요)
    coordinates = {
        "서울": (37.5665, 126.9780),
        "부산": (35.1796, 129.0756),
        "대구": (35.8714, 128.6014),
        "인천": (37.4563, 126.7052),
        "광주": (35.1595, 126.8526),
        "대전": (36.3504, 127.3845),
        "제주": (33.4996, 126.5312),
    }

    lat, lon = coordinates.get(city, coordinates["서울"])
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,"
        f"relative_humidity_2m_max,wind_speed_10m_max"
        f"&timezone=Asia/Seoul&forecast_days=7"
    )

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"[경고] API 호출 실패: {e}")
        print("[대체] 시뮬레이션 데이터를 사용합니다.")
        return _generate_simulated_weather()
```

> **Note:** `fetch_weather` 함수의 설계 패턴을 주목하세요. API 호출이 실패하면 자동으로 시뮬레이션 데이터로 대체합니다. 이런 **폴백(fallback) 패턴**은 네트워크에 의존하는 프로그램에서 매우 중요합니다.

### 날씨 표시 함수

가져온 데이터를 터미널에 보기 좋게 표시하는 함수들입니다.

```python
def display_current_weather(data):
    """현재(오늘) 날씨를 상세하게 표시합니다."""
    today = data["forecast"][0]
    city = data["city"]

    print()
    print("=" * 50)
    print(f"  {city} 현재 날씨 정보")
    print(f"  마지막 업데이트: {data['last_updated']}")
    print("=" * 50)
    print()
    print(f"  날씨: {today['icon']}  {today['condition']}")
    print(f"  최고 기온: {today['temp_high']}°C")
    print(f"  최저 기온: {today['temp_low']}°C")
    print(f"  습도: {today['humidity']}%")
    print(f"  풍속: {today['wind_speed']} m/s")
    print()

    # 체감 온도 간이 계산
    avg_temp = (today["temp_high"] + today["temp_low"]) / 2
    wind = today["wind_speed"]
    if avg_temp <= 10 and wind >= 4.8:
        wind_chill = (
            13.12 + 0.6215 * avg_temp
            - 11.37 * (wind ** 0.16)
            + 0.3965 * avg_temp * (wind ** 0.16)
        )
        print(f"  체감 온도(추정): {wind_chill:.1f}°C")
    else:
        print(f"  평균 기온: {avg_temp:.1f}°C")
```

주간 예보는 테이블 형식으로 깔끔하게 출력합니다.

```python
def display_weekly_forecast(data):
    """7일간의 주간 예보를 테이블 형태로 표시합니다."""
    city = data["city"]
    forecast = data["forecast"]

    print()
    print("=" * 60)
    print(f"  {city} 주간 예보 (7일)")
    print("=" * 60)
    print(f"  {'날짜':<12} {'요일':>4} {'날씨':<10} {'최고':>5} {'최저':>5} {'습도':>5}")
    print("  " + "-" * 56)

    for day in forecast:
        print(
            f"  {day['date']:<12} "
            f"{day['day_name']:>4} "
            f"{day['icon']} {day['condition']:<7} "
            f"{day['temp_high']:>4}°C "
            f"{day['temp_low']:>4}°C "
            f"{day['humidity']:>4}%"
        )
```

텍스트 기반 기온 변화 그래프도 포함되어 있습니다.

```python
def display_temperature_chart(data):
    """간단한 텍스트 막대 그래프로 기온 변화를 표시합니다."""
    forecast = data["forecast"]

    # 전체 범위 계산
    all_temps = []
    for day in forecast:
        all_temps.extend([day["temp_high"], day["temp_low"]])
    min_temp = min(all_temps)
    max_temp = max(all_temps)
    temp_range = max_temp - min_temp if max_temp != min_temp else 1

    chart_width = 30  # 막대 최대 길이

    for day in forecast:
        high = day["temp_high"]
        low = day["temp_low"]

        low_bar_len = int((low - min_temp) / temp_range * chart_width)
        high_bar_len = int((high - min_temp) / temp_range * chart_width)

        bar = " " * low_bar_len + "=" * (high_bar_len - low_bar_len)
        label = f"{day['day_name']} {day['date'][-5:]}"
        print(f"  {label:<9} |{bar:<{chart_width}}| {low:>3}~{high}°C")
```

### 실행 결과

```bash
$ python examples/python/chapter06/ex29_01_weather_display.py
```

```
╔══════════════════════════════════════════╗
║       개인 비서 - 날씨 정보 모듈         ║
╚══════════════════════════════════════════╝
[시뮬레이션 모드] '서울' 날씨 데이터를 생성합니다...

==================================================
  서울 현재 날씨 정보
  마지막 업데이트: 2025-03-15 14:30
==================================================

  날씨: ☀️  맑음
  최고 기온: 24°C
  최저 기온: 16°C
  습도: 45%
  풍속: 3.2 m/s

  평균 기온: 20.0°C

  ── 외출 조언 ──
  - 쾌적한 날씨입니다. 활동하기 좋아요!

============================================================
  서울 주간 예보 (7일)
============================================================
  날짜          요일 날씨         최고   최저   습도
  --------------------------------------------------------
  2025-03-15    토  ☀️ 맑음       24°C   16°C   45%
  2025-03-16    일  ⛅ 구름 조금   22°C   14°C   52%
  ...
```

> **Tip:** `display_temperature_chart` 함수의 텍스트 막대 그래프는 외부 라이브러리 없이도 데이터를 시각화할 수 있는 좋은 방법입니다. 최솟값과 최댓값 사이의 비율을 계산하여 막대 길이를 결정합니다.

---

## 29.4 예제 29-2: 일정 관리

두 번째 모듈은 JSON 파일 기반의 일정 관리 시스템입니다. CRUD(Create, Read, Update, Delete) 전체 기능을 구현합니다.

### AI에게 요청하기

```
JSON 파일 기반 일정 관리 모듈을 만들어줘. 요구사항:
- 일정 추가 (제목, 날짜, 시간, 카테고리, 반복 설정)
- 일정 조회 (오늘, 이번 주, 카테고리별, 키워드 검색)
- 일정 수정, 삭제, 완료 처리
- UUID 기반 짧은 고유 ID 사용
- 날짜별로 그룹핑하여 출력
- 클래스로 구조화해줘
```

### 핵심 코드 분석

`ScheduleManager` 클래스가 일정 데이터의 모든 관리를 담당합니다.

**예제 29-2: 일정 관리**

```python
# examples/python/chapter06/ex29_02_schedule_manager.py
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import uuid

SCHEDULE_FILE = Path("/tmp/personal_assistant_schedule.json")


class ScheduleManager:
    """JSON 파일 기반 일정 관리 클래스"""

    def __init__(self, filepath=SCHEDULE_FILE):
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
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.schedules, f, ensure_ascii=False, indent=2)
```

여기서 주목할 점은 **방어적 프로그래밍** 패턴입니다.

- `_load()`에서 `json.JSONDecodeError`를 잡아 손상된 파일을 처리합니다
- `_save()`에서 `mkdir(parents=True, exist_ok=True)`로 디렉토리를 자동 생성합니다
- `ensure_ascii=False`로 한국어가 깨지지 않게 저장합니다

### 일정 추가 (Create)

```python
    def add(self, title, date_str, time_str="", description="",
            category="일반", repeat="없음"):
        """새 일정을 추가합니다."""
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
```

> **Note:** `uuid.uuid4()[:8]`로 짧은 고유 ID를 생성하는 방식을 주목하세요. UUID의 처음 8자만 사용하면 사용자가 쉽게 입력할 수 있으면서도 충돌 가능성이 매우 낮습니다.

### 일정 조회 (Read)

다양한 조건으로 일정을 조회하는 메서드들입니다.

```python
    def get_today(self):
        """오늘 일정을 조회합니다."""
        today = datetime.now().strftime("%Y-%m-%d")
        return [s for s in self.schedules if s["date"] == today]

    def get_this_week(self):
        """이번 주 일정을 조회합니다 (월~일)."""
        today = datetime.now()
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

    def search(self, keyword):
        """키워드로 일정을 검색합니다."""
        keyword_lower = keyword.lower()
        return [
            s for s in self.schedules
            if keyword_lower in s["title"].lower()
            or keyword_lower in s.get("description", "").lower()
        ]
```

리스트 컴프리헨션을 활용한 필터링이 핵심입니다. 날짜 문자열의 비교(`monday_str <= s["date"] <= sunday_str`)가 가능한 이유는 `YYYY-MM-DD` 형식이 사전순 정렬과 시간순 정렬이 일치하기 때문입니다.

### 일정 수정/삭제/완료 (Update, Delete)

```python
    def update(self, schedule_id, **kwargs):
        """일정을 수정합니다."""
        for i, s in enumerate(self.schedules):
            if s["id"] == schedule_id:
                allowed_fields = {"title", "date", "time", "description",
                                  "category", "repeat", "completed"}
                for key, value in kwargs.items():
                    if key in allowed_fields:
                        self.schedules[i][key] = value
                self.schedules[i]["updated_at"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                self._save()
                return self.schedules[i]
        return None

    def delete(self, schedule_id):
        """일정을 삭제합니다."""
        for i, s in enumerate(self.schedules):
            if s["id"] == schedule_id:
                removed = self.schedules.pop(i)
                self._save()
                return removed
        return None

    def complete(self, schedule_id):
        """일정을 완료 처리합니다."""
        return self.update(schedule_id, completed=True)
```

`update` 메서드에서 `**kwargs`를 사용하여 원하는 필드만 선택적으로 수정할 수 있습니다. `allowed_fields` 집합으로 허용된 필드만 변경되도록 제한하여 안전성을 확보했습니다.

### 실행 결과

```bash
$ python examples/python/chapter06/ex29_02_schedule_manager.py
```

```
=======================================================
  개인 비서 - 일정 관리 모듈 데모
=======================================================

--- [1단계] 일정 추가 ---
[추가 완료] '팀 회의' 일정이 추가되었습니다. (ID: a1b2c3d4)
[추가 완료] '점심 약속' 일정이 추가되었습니다. (ID: e5f6g7h8)
[추가 완료] '헬스장 운동' 일정이 추가되었습니다. (ID: i9j0k1l2)
...

--- [2단계] 일정 조회 ---

  ── 오늘의 일정 (총 3건) ──

  [2025-03-15 (토)]
    [ ] [업무] 10:00 팀 회의
        ID: a1b2c3d4 | 2분기 계획 논의
    [ ] [약속] 12:30 점심 약속
        ID: e5f6g7h8 | 홍길동님과 강남역
    [ ] [운동] 18:00 헬스장 운동
        ID: i9j0k1l2 | 상체 운동일 | 반복: 매주
```

> **Warning:** JSON 파일 기반 데이터 저장은 소규모 개인 프로젝트에 적합합니다. 데이터가 수천 건 이상이거나 동시 접근이 필요한 경우에는 SQLite 같은 데이터베이스를 사용하는 것이 좋습니다.

---

## 29.5 예제 29-3: 메모 기능

세 번째 모듈은 텍스트 파일 기반의 메모 시스템입니다. 각 메모는 개별 텍스트 파일로 저장되고, 인덱스 파일로 메타데이터를 관리합니다.

### AI에게 요청하기

```
텍스트 파일 기반 메모 관리 모듈을 만들어줘. 요구사항:
- 메모를 개별 .txt 파일로 저장
- JSON 인덱스 파일로 메타데이터(제목, 태그, 작성일 등) 관리
- 메모 내용에서 #태그를 자동 추출
- 키워드 검색 (제목 + 내용), 태그별 검색
- 태그 클라우드 표시
- 메모 생성/읽기/수정/삭제
```

### 핵심 코드 분석

메모 모듈의 특징은 **텍스트 파일 + JSON 인덱스**의 이중 구조입니다.

**예제 29-3: 메모 기능**

```python
# examples/python/chapter06/ex29_03_memo_feature.py
import os
import json
from datetime import datetime
from pathlib import Path

MEMO_DIR = Path("/tmp/personal_assistant_memos")
MEMO_INDEX_FILE = MEMO_DIR / "_index.json"


class MemoManager:
    """텍스트 파일 기반 메모 관리 클래스"""

    def __init__(self, memo_dir=MEMO_DIR):
        self.memo_dir = Path(memo_dir)
        self.memo_dir.mkdir(parents=True, exist_ok=True)
        self.index = self._load_index()

    def _extract_tags(self, content):
        """메모 내용에서 #태그를 추출합니다."""
        tags = []
        for word in content.split():
            if word.startswith("#") and len(word) > 1:
                tag = word.lstrip("#").rstrip(".,!?;:")
                if tag:
                    tags.append(tag)
        return list(set(tags))  # 중복 제거
```

태그 추출 로직은 SNS의 해시태그와 동일한 방식입니다. `#` 뒤에 오는 단어를 추출하고, 문장 부호를 제거하며, 중복을 없앱니다.

### 메모 생성

```python
    def create(self, title, content, tags=None):
        """새 메모를 생성합니다."""
        memo_id = self.index["next_id"]
        self.index["next_id"] += 1

        # 내용에서 태그 자동 추출 (명시적 태그가 없는 경우)
        if tags is None:
            tags = self._extract_tags(content)

        # 파일명 생성 (ID_제목.txt)
        safe_title = title.replace(" ", "_").replace("/", "_")[:30]
        filename = f"memo_{memo_id:04d}_{safe_title}.txt"
        filepath = self.memo_dir / filename

        # 메모 파일 작성
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        memo_text = f"제목: {title}\n"
        memo_text += f"작성일: {created_at}\n"
        if tags:
            memo_text += f"태그: {', '.join('#' + t for t in tags)}\n"
        memo_text += f"{'-' * 40}\n"
        memo_text += content
        memo_text += "\n"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(memo_text)

        # 인덱스에 메타데이터 추가
        meta = {
            "id": memo_id,
            "title": title,
            "filename": filename,
            "tags": tags,
            "created_at": created_at,
            "updated_at": created_at,
            "char_count": len(content),
        }
        self.index["memos"].append(meta)
        self._save_index()

        print(f"  [메모 저장] #{memo_id} '{title}' ({len(content)}자)")
        return meta
```

이 설계의 핵심 아이디어는 다음과 같습니다.

- **텍스트 파일**: 사람이 직접 읽고 편집할 수 있습니다
- **JSON 인덱스**: 빠른 검색과 메타데이터 관리를 제공합니다
- **자동 태그 추출**: 내용에 `#태그`를 쓰면 자동으로 분류됩니다

### 검색 기능

```python
    def search(self, keyword):
        """키워드로 메모를 검색합니다 (제목 + 내용)."""
        keyword_lower = keyword.lower()
        results = []

        for meta in self.index["memos"]:
            # 제목 검색
            if keyword_lower in meta["title"].lower():
                results.append(meta)
                continue

            # 내용 검색
            filepath = self.memo_dir / meta["filename"]
            if filepath.exists():
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                if keyword_lower in content.lower():
                    results.append(meta)

        return results

    def search_by_tag(self, tag):
        """태그로 메모를 검색합니다."""
        tag_lower = tag.lower().lstrip("#")
        return [
            m for m in self.index["memos"]
            if tag_lower in [t.lower() for t in m.get("tags", [])]
        ]

    def list_tags(self):
        """사용된 모든 태그를 반환합니다."""
        all_tags = {}
        for meta in self.index["memos"]:
            for tag in meta.get("tags", []):
                all_tags[tag] = all_tags.get(tag, 0) + 1
        return sorted(all_tags.items(), key=lambda x: x[1], reverse=True)
```

검색 기능은 두 단계로 동작합니다. 먼저 인덱스(메타데이터)에서 제목을 검색하고, 일치하지 않으면 실제 파일 내용까지 검색합니다. 이 방식은 대부분의 경우 인덱스만으로 빠르게 결과를 찾을 수 있어 효율적입니다.

### 실행 결과

```bash
$ python examples/python/chapter06/ex29_03_memo_feature.py
```

```
=======================================================
  개인 비서 - 메모 기능 데모
=======================================================

--- [1단계] 메모 생성 ---
  [메모 저장] #1 '프로젝트 아이디어' (125자)
  [메모 저장] #2 'Python 학습 노트' (98자)
  [메모 저장] #3 '회의 메모 - 2분기 계획' (156자)
  [메모 저장] #4 '읽을 책 목록' (89자)
  [메모 저장] #5 '맛집 기록 - 강남' (72자)

--- [6단계] 태그 클라우드 ---

  ── 태그 목록 ──
  #학습       ** (2개)
  #프로젝트   * (1개)
  #AI         * (1개)
  #코드리뷰   * (1개)
  #파이썬     * (1개)
  #회의       * (1개)
  ...
```

> **Tip:** 태그 시스템은 메모를 체계적으로 관리하는 강력한 도구입니다. 메모를 작성할 때 관련 태그를 내용에 포함하면, 나중에 태그별로 쉽게 찾을 수 있습니다. AI에게 "태그 추천 기능을 추가해줘"라고 요청하면 더 스마트한 분류가 가능합니다.

---

## 29.6 예제 29-4: 알림 기능

네 번째 모듈은 `sched` 모듈을 활용한 시간 기반 알림 시스템입니다. 우선순위별 알림, 반복 알림, 카운트다운 타이머, 뽀모도로 타이머를 포함합니다.

### AI에게 요청하기

```
sched 모듈 기반 알림 관리 모듈을 만들어줘. 요구사항:
- 초 단위 지연 알림 등록 (우선순위 지원)
- 특정 시간(HH:MM) 알림 등록
- 알림 취소, 기록 조회
- 반복 알림 지원
- 간단한 카운트다운 타이머
- 뽀모도로 타이머 (작업/휴식 사이클)
- JSON 파일로 알림 데이터 저장
데모용으로 짧은 시간(1~5초)으로 테스트해줘.
```

### 핵심 코드 분석

`sched` 모듈은 파이썬 표준 라이브러리의 이벤트 스케줄러입니다. 지정된 시간 후에 함수를 실행하는 기능을 제공합니다.

**예제 29-4: 알림 기능**

```python
# examples/python/chapter06/ex29_04_reminder.py
import sched
import time
import json
from datetime import datetime, timedelta
from pathlib import Path

REMINDER_FILE = Path("/tmp/personal_assistant_reminders.json")


class ReminderManager:
    """sched 모듈 기반 알림 관리 클래스"""

    def __init__(self, filepath=REMINDER_FILE):
        self.filepath = Path(filepath)
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.reminders = []
        self.reminder_history = []
        self._next_id = 1

    def add_reminder(self, message, delay_seconds, priority=1, repeat=0):
        """새 알림을 등록합니다."""
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
        reminder["_event"] = event

        self.reminders.append(reminder)
        print(f"  [알림 등록] #{reminder_id} '{message}' "
              f"({delay_seconds}초 후, 우선순위: {priority})")
        return reminder
```

`sched.scheduler`의 핵심 메서드를 정리하면 다음과 같습니다.

| 메서드 | 설명 |
|--------|------|
| `enter(delay, priority, action, argument)` | delay초 후에 action 실행 |
| `cancel(event)` | 등록된 이벤트 취소 |
| `run()` | 스케줄러 실행 (모든 이벤트 처리까지 대기) |

### 알림 콜백 및 반복 처리

```python
    def _trigger_reminder(self, reminder):
        """알림이 발동될 때 호출되는 콜백 함수입니다."""
        now = datetime.now().strftime("%H:%M:%S")
        priority_label = {1: "긴급", 2: "중요", 3: "일반"}.get(
            reminder["priority"], "일반"
        )

        print()
        print("  " + "*" * 50)
        print(f"  *  REMINDER [{priority_label}] - {now}")
        print(f"  *  {reminder['message']}")
        print("  " + "*" * 50)

        reminder["status"] = "완료"
        reminder["completed_at"] = now

        # 반복 알림 처리
        if reminder["repeat_remaining"] > 0:
            reminder["repeat_remaining"] -= 1
            new_event = self.scheduler.enter(
                reminder["delay_seconds"],
                reminder["priority"],
                self._trigger_reminder,
                argument=(reminder,)
            )
            reminder["_event"] = new_event
            reminder["status"] = "대기 중 (반복)"
```

반복 알림의 핵심은 콜백 함수 내에서 새 이벤트를 다시 등록하는 것입니다. `repeat_remaining` 카운터를 줄이면서 반복 횟수를 제어합니다.

### 카운트다운 타이머와 뽀모도로

```python
def quick_timer(seconds, message="타이머 종료!"):
    """간단한 카운트다운 타이머입니다."""
    print(f"\n  타이머 시작: {seconds}초")
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer_display = f"{mins:02d}:{secs:02d}"
        print(f"  남은 시간: {timer_display}", end="\r")
        time.sleep(1)

    print(f"  {' ' * 25}", end="\r")
    print(f"  [타이머 완료] {message}")


def pomodoro_demo(work_seconds=3, break_seconds=2):
    """뽀모도로 타이머 데모 (짧은 시간으로 시연)."""
    print("\n  ── 뽀모도로 타이머 (데모) ──")
    print(f"  작업: {work_seconds}초 / 휴식: {break_seconds}초")

    print(f"\n  [작업 시작] 집중하세요!")
    for i in range(work_seconds, 0, -1):
        print(f"  작업 중... {i}초 남음", end="\r")
        time.sleep(1)
    print(f"  {'':25}", end="\r")
    print("  [작업 완료] 수고했습니다!")

    print(f"\n  [휴식 시작] 잠시 쉬세요!")
    for i in range(break_seconds, 0, -1):
        print(f"  휴식 중... {i}초 남음", end="\r")
        time.sleep(1)
    print(f"  {'':25}", end="\r")
    print("  [휴식 완료] 다시 시작할 준비가 되었습니다!")
```

> **Note:** `print(..., end="\r")`을 사용하면 같은 줄을 덮어씁니다. 이것이 터미널에서 카운트다운 애니메이션을 구현하는 핵심 기법입니다. `\r`은 커서를 줄의 시작으로 이동시킵니다.

### 실행 결과

```bash
$ python examples/python/chapter06/ex29_04_reminder.py
```

```
=======================================================
  개인 비서 - 알림 기능 데모
=======================================================
  현재 시각: 2025-03-15 14:30:00

--- [1단계] 알림 등록 ---
  [알림 등록] #1 '물 마시기 알림' (2초 후, 우선순위: 3)
  [알림 등록] #2 '이메일 확인하세요!' (3초 후, 우선순위: 2)
  [알림 등록] #3 '회의 10분 전입니다!' (1초 후, 우선순위: 1)
  [알림 등록] #4 '스트레칭 시간' (4초 후, 우선순위: 3)
  [알림 등록] #5 '취소될 알림' (5초 후, 우선순위: 3)
  [알림 취소] #5 '취소될 알림'

--- [3단계] 알림 처리 시작 ---
  스케줄러 시작... (4개 알림 대기 중)

  **************************************************
  *  REMINDER [긴급] - 14:30:01
  *  회의 10분 전입니다!
  **************************************************

  **************************************************
  *  REMINDER [일반] - 14:30:02
  *  물 마시기 알림
  **************************************************
  ...
```

---

## 29.7 예제 29-5: 명령어 통합

다섯 번째 단계에서는 지금까지 만든 모든 모듈을 `argparse` 서브커맨드로 하나의 CLI 도구로 통합합니다. 이것이 이 프로젝트의 가장 중요한 단계입니다.

### AI에게 요청하기

```
지금까지 만든 날씨, 일정, 메모, 알림 모듈을 argparse 서브커맨드로 통합해줘.
요구사항:
- weather, schedule, memo, timer, status 서브커맨드
- schedule과 memo는 add/list/done/delete 등 하위 서브커맨드
- 단축 별칭 지원 (w=weather, s=schedule, m=memo, t=timer)
- 인수 없이 실행하면 데모 모드로 동작
- 도움말(--help)이 한국어로 잘 표시되도록
```

### 핵심 코드 분석

통합 CLI의 핵심은 `argparse`의 서브커맨드 구조입니다.

**예제 29-5: 명령어 통합**

```python
# examples/python/chapter06/ex29_05_unified_commands.py
import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path("/tmp/personal_assistant")
SCHEDULE_FILE = DATA_DIR / "schedules.json"
MEMO_DIR = DATA_DIR / "memos"


def build_parser():
    """argparse 파서를 구성합니다."""
    parser = argparse.ArgumentParser(
        prog="assistant",
        description="개인 비서 CLI - 일정, 메모, 날씨, 알림을 한 곳에서!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  %(prog)s weather --city 서울
  %(prog)s schedule add "회의" --date 2025-03-15 --time 10:00
  %(prog)s schedule list --today
  %(prog)s memo add "아이디어" --content "새 프로젝트 구상"
  %(prog)s memo search --keyword "프로젝트"
  %(prog)s timer 300 --message "휴식 시간!"
  %(prog)s status
        """
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="사용 가능한 명령어",
        description="아래 명령어 중 하나를 선택하세요"
    )
```

여기서 `RawDescriptionHelpFormatter`를 사용하면 `epilog`의 줄바꿈이 그대로 유지됩니다. 이것이 도움말을 보기 좋게 만드는 핵심입니다.

### 서브커맨드 등록

각 기능은 서브커맨드로 등록됩니다. `schedule`처럼 하위에 추가 서브커맨드가 필요한 경우, 중첩 서브파서를 사용합니다.

```python
    # ── weather 서브커맨드 ──
    weather_parser = subparsers.add_parser(
        "weather", help="날씨 정보 확인",
        aliases=["w"]  # 단축 별칭
    )
    weather_parser.add_argument("--city", "-c", default="서울")
    weather_parser.add_argument("--weekly", "-w", action="store_true")
    weather_parser.set_defaults(func=cmd_weather)

    # ── schedule 서브커맨드 (중첩) ──
    schedule_parser = subparsers.add_parser(
        "schedule", help="일정 관리", aliases=["s"]
    )
    schedule_sub = schedule_parser.add_subparsers(dest="schedule_cmd")

    # schedule add
    s_add = schedule_sub.add_parser("add", help="일정 추가")
    s_add.add_argument("title", help="일정 제목")
    s_add.add_argument("--date", "-d", required=True, help="날짜 (YYYY-MM-DD)")
    s_add.add_argument("--time", "-t", default="", help="시간 (HH:MM)")
    s_add.add_argument("--category", "-c", default="일반",
                       choices=["일반", "업무", "개인", "약속", "운동", "공부"])
    s_add.set_defaults(func=cmd_schedule_add)

    # schedule list
    s_list = schedule_sub.add_parser("list", help="일정 목록")
    s_list.add_argument("--today", action="store_true")
    s_list.add_argument("--week", action="store_true")
    s_list.set_defaults(func=cmd_schedule_list)
```

> **Note:** `set_defaults(func=cmd_weather)`의 패턴에 주목하세요. 각 서브커맨드에 처리 함수를 연결해두면, `args.func(args)`로 해당 함수를 자동으로 호출할 수 있습니다. 이것이 argparse의 서브커맨드 디스패치 패턴입니다.

### 상태 요약 기능

```python
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
```

`status` 명령은 대시보드처럼 전체 상태를 한 눈에 보여줍니다. 오늘 미완료 일정, 저장된 메모 수, 데이터 크기 등을 요약합니다.

### 데모 모드

```python
def main():
    """인수가 있으면 CLI 모드, 없으면 데모 모드로 실행합니다."""
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
```

`len(sys.argv) == 1`로 인수 없이 실행됐는지 확인하고, 그런 경우 데모 모드를 실행합니다. 이는 사용자가 도구를 처음 접했을 때 사용법을 바로 보여주는 좋은 패턴입니다.

### 실행 결과

```bash
$ python examples/python/chapter06/ex29_05_unified_commands.py
```

```
=======================================================
  개인 비서 CLI - 통합 명령어 데모
=======================================================

───────────────────────────────────────────────────────
  >>> assistant weather --city 서울
  [1. 날씨 확인]
───────────────────────────────────────────────────────

  ☀️ 서울 날씨 (2025-03-15)
  상태: 맑음
  기온: 15~22°C
  습도: 52%  |  풍속: 3.5 m/s

───────────────────────────────────────────────────────
  >>> assistant schedule add 팀 회의 --date 2025-03-15 --time 10:00
  [3. 오늘 일정 추가 - 팀 회의]
───────────────────────────────────────────────────────
  [추가 완료] #1 '팀 회의' (2025-03-15)

  ...

───────────────────────────────────────────────────────
  >>> assistant status
  [14. 상태 요약]
───────────────────────────────────────────────────────

  ╔══════════════════════════════════════╗
  ║       개인 비서 상태 요약             ║
  ╚══════════════════════════════════════╝
  현재 시각: 2025-03-15 14:30:00

  [일정] 오늘: 2건 (미완료: 1건)
    -  12:30 점심 약속
  [메모] 저장됨: 2건
  [저장소] /tmp/personal_assistant
           크기: 1,234 bytes

=======================================================
  통합 명령어 데모가 완료되었습니다!

  실제 사용법:
    python ex29_05_unified_commands.py weather --city 부산
    python ex29_05_unified_commands.py schedule list --today
    python ex29_05_unified_commands.py memo add '메모' -c '내용'
    python ex29_05_unified_commands.py timer 60 -m '1분 완료!'
    python ex29_05_unified_commands.py status
    python ex29_05_unified_commands.py --help
=======================================================
```

> **Tip:** 통합 단계에서 가장 중요한 것은 **일관된 인터페이스**입니다. 모든 서브커맨드가 동일한 패턴을 따르면 사용자가 새로운 명령어를 쉽게 예측할 수 있습니다. `assistant <기능> <동작> [옵션]` 구조가 그 예입니다.

---

## 29.8 예제 29-6: 설정 관리

마지막 모듈은 `configparser`를 사용한 설정 관리 시스템입니다. 사용자 프로필, 표시 옵션, 알림 설정 등을 INI 형식 파일로 관리합니다.

### AI에게 요청하기

```
configparser 기반 설정 관리 모듈을 만들어줘. 요구사항:
- 사용자, 화면, 날씨, 일정, 메모, 알림, 데이터 섹션
- 기본 설정값 자동 생성
- 설정 조회 (문자열, 불리언, 정수 타입별)
- 설정 변경, 제거, 섹션 제거
- 설정 검증 (유효성 검사)
- JSON 내보내기/가져오기
- 백업 및 기본값 초기화
- 설정 마법사 데모
```

### 핵심 코드 분석

`configparser`는 INI 파일 형식의 설정을 관리하는 표준 라이브러리입니다.

**예제 29-6: 설정 관리**

```python
# examples/python/chapter06/ex29_06_config_manager.py
import configparser
import json
import os
from datetime import datetime
from pathlib import Path

CONFIG_DIR = Path("/tmp/personal_assistant_config")
CONFIG_FILE = CONFIG_DIR / "settings.ini"

# 기본 설정값 정의
DEFAULT_CONFIG = {
    "사용자": {
        "이름": "사용자",
        "이메일": "",
        "도시": "서울",
        "언어": "한국어",
    },
    "화면": {
        "테마": "기본",
        "색상_사용": "true",
        "날짜_형식": "YYYY-MM-DD",
        "시간_형식": "24시간",
        "주_시작일": "월요일",
    },
    "날씨": {
        "기본_도시": "서울",
        "온도_단위": "섭씨",
        "자동_갱신": "true",
        "갱신_간격_분": "30",
    },
    "일정": {
        "기본_카테고리": "일반",
        "미리_알림_분": "10",
        "완료_자동_삭제": "false",
    },
    "알림": {
        "소리_사용": "true",
        "뽀모도로_작업_분": "25",
        "뽀모도로_휴식_분": "5",
        "뽀모도로_긴_휴식_분": "15",
    },
    "데이터": {
        "저장_디렉토리": "/tmp/personal_assistant",
        "자동_백업": "true",
        "백업_간격_시간": "24",
    },
}
```

기본 설정값을 딕셔너리로 미리 정의해두면, 설정 파일이 없을 때 자동으로 생성할 수 있습니다.

### ConfigManager 클래스

```python
class ConfigManager:
    """configparser 기반 설정 관리 클래스"""

    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = Path(config_file)
        self.config = configparser.ConfigParser()
        self.config.optionxform = str  # 대소문자 유지
        self._load_or_create()

    def _load_or_create(self):
        """설정 파일을 불러오거나 기본값으로 새로 생성합니다."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        if self.config_file.exists():
            self.config.read(self.config_file, encoding="utf-8")
        else:
            self._apply_defaults()
            self._save()

    def _apply_defaults(self):
        """기본 설정값을 적용합니다."""
        for section, values in DEFAULT_CONFIG.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for key, value in values.items():
                if not self.config.has_option(section, key):
                    self.config.set(section, key, str(value))
```

`config.optionxform = str` 설정이 중요합니다. 기본적으로 `configparser`는 키를 소문자로 변환하는데, 한국어 키를 사용하므로 원본을 유지해야 합니다.

### 타입별 설정 조회

```python
    def get(self, section, key, fallback=None):
        """문자열 설정값을 가져옵니다."""
        return self.config.get(section, key, fallback=fallback)

    def get_bool(self, section, key, fallback=False):
        """불리언 설정값을 가져옵니다."""
        value = self.get(section, key, str(fallback))
        return value.lower() in ("true", "yes", "1", "on")

    def get_int(self, section, key, fallback=0):
        """정수 설정값을 가져옵니다."""
        try:
            return int(self.get(section, key, str(fallback)))
        except (ValueError, TypeError):
            return fallback
```

INI 파일의 모든 값은 문자열이므로, `get_bool`과 `get_int` 같은 타입 변환 메서드를 별도로 만들었습니다. 이렇게 하면 호출하는 쪽에서 매번 변환하지 않아도 됩니다.

### 설정 검증

```python
    def validate(self):
        """설정값의 유효성을 검사합니다."""
        issues = []

        # 필수 섹션 확인
        for section in DEFAULT_CONFIG:
            if not self.config.has_section(section):
                issues.append(f"섹션 '{section}'이(가) 없습니다.")

        # 값 범위 확인
        pomodoro_work = self.get_int("알림", "뽀모도로_작업_분")
        if pomodoro_work < 1 or pomodoro_work > 120:
            issues.append(f"뽀모도로 작업 시간이 비정상적: {pomodoro_work}분")

        reminder_min = self.get_int("일정", "미리_알림_분")
        if reminder_min < 0:
            issues.append(f"미리 알림 시간이 음수: {reminder_min}분")

        if issues:
            for issue in issues:
                print(f"  [문제] {issue}")
        else:
            print("  모든 설정이 유효합니다!")

        return len(issues) == 0
```

> **Note:** 설정 검증은 프로그램이 시작될 때 실행하는 것이 좋습니다. 잘못된 설정으로 프로그램이 중간에 오류를 내는 것보다, 시작할 때 문제를 알려주는 것이 훨씬 좋은 사용자 경험입니다.

### JSON 내보내기/가져오기

```python
    def export_json(self, output_path=None):
        """설정을 JSON 형식으로 내보냅니다."""
        data = {}
        for section in self.config.sections():
            data[section] = dict(self.config.items(section))

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        return data

    def import_json(self, input_path):
        """JSON 파일에서 설정을 가져옵니다."""
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for section, values in data.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for key, value in values.items():
                self.config.set(section, key, str(value))

        self._save()
```

INI 파일과 JSON 간의 변환을 지원하면, 설정을 다른 형식으로 공유하거나 프로그래밍적으로 처리할 때 유용합니다.

### 실행 결과

```bash
$ python examples/python/chapter06/ex29_06_config_manager.py
```

```
=======================================================
  개인 비서 - 설정 관리 데모
=======================================================

--- [1단계] 설정 파일 생성 ---
  [설정 생성] 기본 설정으로 초기화: /tmp/.../settings.ini

--- [2단계] 기본 설정 확인 ---

  ╔══════════════════════════════════════════╗
  ║         개인 비서 설정 현황               ║
  ╚══════════════════════════════════════════╝

  [사용자]
    이름                 = 사용자
    이메일               =
    도시                 = 서울
    언어                 = 한국어

  [화면]
    테마                 = 기본
    색상_사용            = true (사용)
    날짜_형식            = YYYY-MM-DD
    시간_형식            = 24시간
    주_시작일            = 월요일

  ...

--- [3단계] 초기 설정 마법사 ---
  [설정 변경] [사용자] 이름: '사용자' -> '홍길동'
  [설정 변경] [사용자] 이메일: '' -> 'hong@example.com'
  [설정 변경] [화면] 테마: '기본' -> '어두운'
  ...

--- [8단계] 설정 검증 ---
  모든 설정이 유효합니다!
```

---

## 29.9 전체 프로젝트 통합 아키텍처

모든 모듈이 완성되었으니, 전체 구조를 다시 정리해 봅시다.

### 모듈 간의 관계

```
┌─────────────────────────────────────────────────────┐
│              unified_commands.py (통합 CLI)           │
│  argparse 서브커맨드로 모든 기능에 접근               │
├─────────┬──────────┬──────────┬────────┬────────────┤
│ weather │ schedule │   memo   │ timer  │   status   │
│ 날씨    │ 일정     │   메모   │ 알림   │   상태     │
├─────────┴──────────┴──────────┴────────┴────────────┤
│              config_manager.py (설정 관리)            │
│  모든 모듈의 동작 방식을 설정으로 제어                │
├─────────────────────────────────────────────────────┤
│                   데이터 저장소                       │
│  /tmp/personal_assistant/                            │
│  ├── schedules.json   (일정 데이터)                  │
│  ├── memos/           (메모 파일들)                  │
│  ├── reminders.json   (알림 기록)                    │
│  └── config/settings.ini (설정)                      │
└─────────────────────────────────────────────────────┘
```

### 설계 원칙 정리

이 프로젝트에서 적용한 핵심 설계 원칙들을 정리합니다.

| 원칙 | 적용 |
|------|------|
| **모듈화** | 각 기능이 독립적인 파일로 분리되어 개별 테스트 가능 |
| **일관된 인터페이스** | 모든 모듈이 클래스 기반 + CRUD 패턴 |
| **방어적 프로그래밍** | 파일 손상, 네트워크 실패, 잘못된 입력 처리 |
| **폴백 패턴** | API 실패 시 시뮬레이션 데이터로 대체 |
| **데이터 영속성** | JSON/텍스트 파일로 프로그램 종료 후에도 데이터 유지 |
| **설정 외부화** | 동작 방식을 코드가 아닌 설정 파일로 제어 |

---

## 29.10 프로젝트 확장 아이디어

### AI에게 추가 기능 요청하기

프로젝트가 완성된 후, AI에게 추가 기능을 요청하여 프로젝트를 확장할 수 있습니다. 다음은 좋은 확장 프롬프트 예시입니다.

**기능 확장 요청 예시:**

```
개인 비서 CLI에 다음 기능을 추가해줘:
1. 일정과 알림 연동 - 일정 시간 전에 자동으로 알림 등록
2. 메모에서 TODO 항목 추출 - 메모 내용의 "- [ ]" 패턴을 일정으로 변환
3. 주간 리포트 생성 - 한 주간의 완료 일정, 작성 메모를 요약
```

**데이터 관리 개선 요청:**

```
데이터 관리를 개선해줘:
1. SQLite 데이터베이스로 전환 (표준 라이브러리 sqlite3 사용)
2. 데이터 자동 백업 (설정된 간격으로)
3. CSV로 일정/메모 내보내기 기능
```

**사용자 경험 개선 요청:**

```
CLI 사용자 경험을 개선해줘:
1. ANSI 색상으로 출력 꾸미기 (긴급=빨강, 완료=초록 등)
2. 대화형 모드 추가 (메뉴 선택으로 기능 사용)
3. 자동완성 힌트 표시
```

> **Tip:** 프로젝트 확장을 요청할 때는 "기존 코드를 수정해줘"보다 "기존 구조를 유지하면서 추가해줘"라고 요청하는 것이 더 안정적인 결과를 얻습니다.

---

## 정리

이번 프로젝트에서 우리는 다음을 달성했습니다.

### 배운 기술

| 기술 | 활용 |
|------|------|
| `urllib` + `json` | 외부 API 데이터 가져오기 및 파싱 |
| `json` 파일 I/O | 구조화된 데이터의 영속적 저장 |
| `pathlib` | 크로스 플랫폼 파일/디렉토리 관리 |
| `datetime` + `timedelta` | 날짜 계산, 필터링, 형식 변환 |
| `uuid` | 고유 식별자 생성 |
| `sched` + `time` | 이벤트 스케줄링, 타이머 구현 |
| `argparse` 서브커맨드 | 다기능 CLI 도구 통합 |
| `configparser` | INI 형식 설정 파일 관리 |
| 클래스 설계 | Manager 패턴으로 데이터 관리 캡슐화 |
| 방어적 프로그래밍 | 예외 처리, 폴백, 입력 검증 |

### 프로젝트 개발 과정 요약

```
[1단계] 요구사항 정리 → 표로 정리하여 AI에게 전달
[2단계] 모듈별 구현 → 독립 모듈을 하나씩 완성
[3단계] 개별 테스트 → 각 모듈을 단독 실행하여 검증
[4단계] 통합 → argparse로 하나의 CLI로 연결
[5단계] 설정 추가 → 외부 설정으로 동작 제어
[6단계] 확장 → AI에게 추가 기능 요청
```

### 핵심 교훈

1. **분할 정복**: 큰 프로젝트도 작은 모듈로 나누면 관리할 수 있습니다
2. **독립성 유지**: 각 모듈이 독립적으로 동작하면 디버깅이 쉽습니다
3. **점진적 통합**: 모듈을 하나씩 추가하면서 테스트하면 안정적입니다
4. **설정 외부화**: 코드를 수정하지 않고 동작을 바꿀 수 있습니다
5. **AI와의 반복**: 한 번에 완벽한 코드를 요청하기보다, 단계별로 개선하는 것이 효과적입니다

---

## 다음 단계

축하합니다! 개인 비서 CLI 프로젝트를 완성했습니다. 이 프로젝트에서 배운 기술들을 바탕으로 다음과 같은 확장에 도전해 보세요.

### 도전 과제

1. **데이터베이스 전환**: JSON 파일 대신 `sqlite3`로 데이터를 관리해 보세요. AI에게 "기존 JSON 기반 일정 관리를 SQLite로 변환해줘"라고 요청해 보세요.

2. **대화형 모드 추가**: 서브커맨드 방식 외에 `input()`을 활용한 대화형 메뉴 모드를 추가해 보세요. "번호를 선택하세요: 1.날씨 2.일정 3.메모" 같은 인터페이스입니다.

3. **알림-일정 연동**: 일정의 시간에 맞춰 자동으로 알림이 등록되도록 두 모듈을 연결해 보세요.

4. **주간 리포트**: 한 주간의 활동을 요약하는 리포트 기능을 만들어 보세요. 완료된 일정 수, 작성한 메모 수, 가장 많이 사용한 태그 등을 포함합니다.

5. **데이터 시각화**: `display_temperature_chart`처럼 일정 통계나 메모 작성 빈도를 텍스트 그래프로 시각화해 보세요.

6. **플러그인 시스템**: 새로운 기능을 코드 수정 없이 추가할 수 있는 플러그인 구조를 설계해 보세요. AI에게 "플러그인 아키텍처를 적용해줘"라고 요청해 보세요.

> **Tip:** 확장 작업을 할 때는 항상 현재 동작하는 코드를 백업(git commit)한 후 진행하세요. AI와의 바이브 코딩에서도 버전 관리는 매우 중요합니다!

다음 장에서는 부록으로 이 책에서 다룬 내용을 정리하고, 바이브 코딩을 더 깊이 학습할 수 있는 리소스를 안내합니다.
