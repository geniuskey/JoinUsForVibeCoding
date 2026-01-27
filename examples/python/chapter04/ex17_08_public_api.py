"""
예제 17-8: 공공 API 활용
무료 공공 API를 활용하여 날씨 데이터를 조회하는 방법을 배웁니다.
네트워크 불가 시 시뮬레이션 데이터로 동작합니다.
"""

import urllib.request
import json


def fetch_weather_simulation():
    """날씨 데이터 조회를 시뮬레이션합니다."""
    print("1. 날씨 API 활용 (시뮬레이션):")

    # 실제 OpenWeatherMap API 호출 패턴
    # (무료 API 키 필요: https://openweathermap.org/api)
    #
    # 실제 코드:
    # api_key = os.environ.get("OPENWEATHER_API_KEY")
    # url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={api_key}&units=metric&lang=kr"

    # 시뮬레이션 데이터 (실제 API 응답과 동일한 구조)
    weather_data = {
        "name": "Seoul",
        "main": {
            "temp": 15.2,
            "feels_like": 13.8,
            "humidity": 62,
            "pressure": 1013,
        },
        "weather": [
            {
                "main": "Clouds",
                "description": "구름 조금",
                "icon": "02d",
            }
        ],
        "wind": {"speed": 3.5, "deg": 270},
        "sys": {"country": "KR", "sunrise": 1700000000, "sunset": 1700040000},
    }

    print(f"   도시: {weather_data['name']} ({weather_data['sys']['country']})")
    print(f"   기온: {weather_data['main']['temp']}°C")
    print(f"   체감 온도: {weather_data['main']['feels_like']}°C")
    print(f"   날씨: {weather_data['weather'][0]['description']}")
    print(f"   습도: {weather_data['main']['humidity']}%")
    print(f"   풍속: {weather_data['wind']['speed']} m/s")


def fetch_country_info():
    """국가 정보 API를 사용합니다 (restcountries.com)."""
    print(f"\n2. 국가 정보 API:")

    url = "https://restcountries.com/v3.1/name/korea?fullText=false"

    try:
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")

        with urllib.request.urlopen(req, timeout=10) as response:
            countries = json.loads(response.read().decode("utf-8"))

            for country in countries:
                name = country.get("name", {}).get("common", "N/A")
                official = country.get("name", {}).get("official", "N/A")
                capital = country.get("capital", ["N/A"])[0] if country.get("capital") else "N/A"
                population = country.get("population", 0)
                region = country.get("region", "N/A")

                print(f"   국가명: {name}")
                print(f"   공식명: {official}")
                print(f"   수도: {capital}")
                print(f"   인구: {population:,}명")
                print(f"   지역: {region}")
                print()

    except Exception as e:
        print(f"   네트워크 요청 실패: {e}")
        print(f"   --- 시뮬레이션 데이터 ---")
        print(f"   국가명: South Korea")
        print(f"   공식명: Republic of Korea")
        print(f"   수도: Seoul")
        print(f"   인구: 51,780,579명")
        print(f"   지역: Asia")


def fetch_random_activity():
    """무작위 활동 제안 API를 사용합니다."""
    print(f"3. 무작위 활동 제안 API:")

    url = "https://www.boredapi.com/api/activity"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            activity = json.loads(response.read().decode("utf-8"))

            print(f"   활동: {activity.get('activity', 'N/A')}")
            print(f"   유형: {activity.get('type', 'N/A')}")
            print(f"   참여 인원: {activity.get('participants', 'N/A')}명")
            print(f"   난이도: {activity.get('accessibility', 'N/A')}")

    except Exception as e:
        print(f"   네트워크 요청 실패: {e}")
        print(f"   --- 시뮬레이션 데이터 ---")

        simulated = {
            "activity": "Learn a new programming language",
            "type": "education",
            "participants": 1,
            "accessibility": 0.25,
        }
        print(f"   활동: {simulated['activity']}")
        print(f"   유형: {simulated['type']}")
        print(f"   참여 인원: {simulated['participants']}명")
        print(f"   난이도: {simulated['accessibility']}")


def display_api_summary():
    """유용한 무료 공공 API 목록을 보여줍니다."""
    print(f"\n4. 유용한 무료 공공 API 목록:")

    apis = [
        ("JSONPlaceholder", "https://jsonplaceholder.typicode.com", "테스트용 가짜 REST API"),
        ("httpbin.org", "https://httpbin.org", "HTTP 요청/응답 테스트"),
        ("REST Countries", "https://restcountries.com", "국가 정보"),
        ("Open Meteo", "https://open-meteo.com", "날씨 데이터 (키 불필요)"),
        ("GitHub API", "https://api.github.com", "GitHub 공개 데이터"),
        ("공공데이터포털", "https://data.go.kr", "한국 공공데이터 (키 필요)"),
    ]

    for name, url, desc in apis:
        print(f"   - {name}: {desc}")
        print(f"     URL: {url}")


if __name__ == "__main__":
    print("=" * 50)
    print("예제 17-8: 공공 API 활용")
    print("=" * 50)
    fetch_weather_simulation()
    fetch_country_info()
    fetch_random_activity()
    display_api_summary()
