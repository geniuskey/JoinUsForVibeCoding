#!/usr/bin/env python3
"""
예제 29-01: 날씨 정보 표시
- urllib를 사용한 공공 날씨 API 호출 시뮬레이션
- 실제 네트워크 없이도 동작하는 데모 모드 포함
- 텍스트 기반 날씨 정보 출력
"""

import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
import random


# ── 시뮬레이션용 날씨 데이터 ──────────────────────────────────────────────

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


# ── API 호출 (시뮬레이션 포함) ─────────────────────────────────────────────

def fetch_weather(city="서울", use_simulation=True):
    """
    날씨 정보를 가져옵니다.

    Args:
        city: 도시 이름
        use_simulation: True이면 시뮬레이션 데이터 사용,
                        False이면 실제 API 호출 시도

    Returns:
        dict: 날씨 데이터
    """
    if use_simulation:
        print(f"[시뮬레이션 모드] '{city}' 날씨 데이터를 생성합니다...")
        data = _generate_simulated_weather()
        data["city"] = city
        return data

    # 실제 API 호출 예시 (Open-Meteo 무료 API, API 키 불필요)
    # 서울 좌표: 위도 37.5665, 경도 126.9780
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


# ── 날씨 표시 함수들 ──────────────────────────────────────────────────────

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
        # 바람냉각지수 간이 공식
        wind_chill = (
            13.12 + 0.6215 * avg_temp
            - 11.37 * (wind ** 0.16)
            + 0.3965 * avg_temp * (wind ** 0.16)
        )
        print(f"  체감 온도(추정): {wind_chill:.1f}°C")
    else:
        print(f"  평균 기온: {avg_temp:.1f}°C")

    # 간단한 외출 조언
    print()
    _print_advice(today)


def _print_advice(weather):
    """날씨에 따른 외출 조언을 출력합니다."""
    print("  ── 외출 조언 ──")
    condition = weather["condition"]
    high = weather["temp_high"]

    if "비" in condition or "소나기" in condition:
        print("  - 우산을 꼭 챙기세요!")
    if "눈" in condition:
        print("  - 눈길 조심하세요! 따뜻하게 입고 나가세요.")
    if high >= 30:
        print("  - 폭염 주의! 충분한 수분 섭취가 필요합니다.")
    elif high >= 25:
        print("  - 따뜻한 날씨입니다. 가벼운 옷차림을 추천합니다.")
    elif high >= 15:
        print("  - 쾌적한 날씨입니다. 활동하기 좋아요!")
    elif high >= 5:
        print("  - 쌀쌀합니다. 겉옷을 챙기세요.")
    else:
        print("  - 매우 춥습니다. 방한복을 착용하세요.")

    if weather["humidity"] >= 80:
        print("  - 습도가 높아요. 불쾌지수가 높을 수 있습니다.")
    if weather["wind_speed"] >= 10:
        print("  - 바람이 강합니다. 모자가 날아갈 수 있어요!")


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

    print()

    # 주간 요약 통계
    highs = [d["temp_high"] for d in forecast]
    lows = [d["temp_low"] for d in forecast]
    print(f"  주간 최고 기온: {max(highs)}°C / 최저 기온: {min(lows)}°C")
    print(f"  평균 최고: {sum(highs) / len(highs):.1f}°C / "
          f"평균 최저: {sum(lows) / len(lows):.1f}°C")

    rainy_days = sum(1 for d in forecast if "비" in d["condition"] or "소나기" in d["condition"])
    if rainy_days > 0:
        print(f"  비 예보: {rainy_days}일 (우산 필요!)")
    print()


def display_temperature_chart(data):
    """간단한 텍스트 막대 그래프로 기온 변화를 표시합니다."""
    forecast = data["forecast"]

    print()
    print("=" * 60)
    print(f"  기온 변화 그래프 (7일)")
    print("=" * 60)

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

        # 최저 기온 막대
        low_bar_len = int((low - min_temp) / temp_range * chart_width)
        # 최고 기온까지의 확장 막대
        high_bar_len = int((high - min_temp) / temp_range * chart_width)

        bar = " " * low_bar_len + "=" * (high_bar_len - low_bar_len)
        label = f"{day['day_name']} {day['date'][-5:]}"
        print(f"  {label:<9} |{bar:<{chart_width}}| {low:>3}~{high}°C")

    print()


# ── 메인 실행 ───────────────────────────────────────────────────────────

def main():
    """메인 함수: 날씨 정보를 가져와서 다양한 형식으로 표시합니다."""
    print("╔══════════════════════════════════════════╗")
    print("║       개인 비서 - 날씨 정보 모듈         ║")
    print("╚══════════════════════════════════════════╝")

    # 시뮬레이션 모드로 날씨 데이터 가져오기
    # (네트워크가 있으면 use_simulation=False로 변경)
    weather_data = fetch_weather(city="서울", use_simulation=True)

    # 1) 현재 날씨 상세 표시
    display_current_weather(weather_data)

    # 2) 주간 예보 테이블
    display_weekly_forecast(weather_data)

    # 3) 기온 변화 그래프
    display_temperature_chart(weather_data)

    # 다른 도시 날씨도 확인
    print("-" * 60)
    print("  [다른 도시 날씨 조회]")
    for city in ["부산", "제주"]:
        other = fetch_weather(city=city, use_simulation=True)
        today = other["forecast"][0]
        print(f"  {city}: {today['icon']} {today['condition']} "
              f"({today['temp_low']}~{today['temp_high']}°C)")

    print()
    print("  날씨 정보 모듈 데모가 완료되었습니다!")


if __name__ == "__main__":
    main()
