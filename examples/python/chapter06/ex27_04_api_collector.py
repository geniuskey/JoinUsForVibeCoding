"""
예제 27-04: API 데이터 수집 시뮬레이션

urllib를 사용한 공공 API 데이터 수집을 시뮬레이션합니다.
실제 네트워크 호출 없이 API 수집 패턴을 학습할 수 있도록
로컬에서 가상의 API 응답을 생성하고 처리합니다.
"""

import json
import os
import random
import datetime
import hashlib
import time


class MockAPIServer:
    """가상 API 서버: 실제 API 호출을 시뮬레이션합니다."""

    def __init__(self, seed=42):
        self.seed = seed
        random.seed(seed)
        self._generate_data()

    def _generate_data(self):
        """가상 API 응답 데이터를 미리 생성합니다."""

        # 날씨 데이터
        cities = ["서울", "부산", "대구", "인천", "광주", "대전"]
        self.weather_data = {}
        for city in cities:
            self.weather_data[city] = {
                "도시": city,
                "온도": round(random.uniform(15, 35), 1),
                "습도": random.randint(40, 90),
                "풍속": round(random.uniform(0, 15), 1),
                "상태": random.choice(["맑음", "흐림", "비", "구름많음"]),
                "측정시간": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

        # 환율 데이터
        self.exchange_data = {
            "USD": {"통화": "미국 달러", "매매기준율": round(random.uniform(1280, 1380), 2)},
            "EUR": {"통화": "유로", "매매기준율": round(random.uniform(1400, 1500), 2)},
            "JPY": {"통화": "일본 엔(100엔)", "매매기준율": round(random.uniform(880, 960), 2)},
            "CNY": {"통화": "중국 위안", "매매기준율": round(random.uniform(175, 195), 2)},
            "GBP": {"통화": "영국 파운드", "매매기준율": round(random.uniform(1650, 1750), 2)},
        }

        # 주식 시세 데이터
        stocks = [
            ("삼성전자", "005930", 60000, 80000),
            ("SK하이닉스", "000660", 120000, 180000),
            ("NAVER", "035420", 170000, 230000),
            ("카카오", "035720", 40000, 65000),
            ("현대차", "005380", 170000, 230000),
        ]
        self.stock_data = {}
        for name, code, min_p, max_p in stocks:
            price = random.randint(min_p, max_p)
            change = random.randint(-3000, 3000)
            self.stock_data[code] = {
                "종목명": name,
                "종목코드": code,
                "현재가": price,
                "전일대비": change,
                "등락률": round(change / price * 100, 2),
                "거래량": random.randint(100000, 5000000),
            }

    def get(self, endpoint, params=None):
        """가상 API 엔드포인트에 GET 요청을 시뮬레이션합니다."""

        # 네트워크 지연 시뮬레이션
        time.sleep(0.1)

        if endpoint == "/api/weather":
            city = (params or {}).get("city", "서울")
            if city in self.weather_data:
                return {"status": 200, "data": self.weather_data[city]}
            return {"status": 404, "error": f"도시를 찾을 수 없음: {city}"}

        elif endpoint == "/api/weather/all":
            return {"status": 200, "data": list(self.weather_data.values())}

        elif endpoint == "/api/exchange":
            currency = (params or {}).get("currency")
            if currency and currency in self.exchange_data:
                return {"status": 200, "data": self.exchange_data[currency]}
            return {"status": 200, "data": self.exchange_data}

        elif endpoint == "/api/stock":
            code = (params or {}).get("code")
            if code and code in self.stock_data:
                return {"status": 200, "data": self.stock_data[code]}
            return {"status": 200, "data": list(self.stock_data.values())}

        return {"status": 404, "error": f"알 수 없는 엔드포인트: {endpoint}"}


class APICollector:
    """API 데이터 수집기: 캐싱, 에러 처리, 재시도 기능을 포함합니다."""

    def __init__(self, cache_dir="/tmp/dashboard-data/cache"):
        self.api = MockAPIServer()
        self.cache_dir = cache_dir
        self.cache_ttl = 300  # 캐시 유효 시간 (초)
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_path(self, endpoint, params):
        """요청에 대한 캐시 파일 경로를 생성합니다."""
        cache_key = f"{endpoint}_{json.dumps(params or {}, sort_keys=True)}"
        cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{cache_hash}.json")

    def _load_cache(self, cache_path):
        """캐시 파일에서 데이터를 로드합니다."""
        if not os.path.exists(cache_path):
            return None

        # 캐시 유효 시간 확인
        file_age = time.time() - os.path.getmtime(cache_path)
        if file_age > self.cache_ttl:
            return None  # 캐시 만료

        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_cache(self, cache_path, data):
        """데이터를 캐시 파일에 저장합니다."""
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def collect(self, endpoint, params=None, use_cache=True, max_retries=3):
        """API에서 데이터를 수집합니다."""

        # 캐시 확인
        cache_path = self._get_cache_path(endpoint, params)
        if use_cache:
            cached = self._load_cache(cache_path)
            if cached is not None:
                print(f"  [캐시 적중] {endpoint}")
                return cached

        # API 호출 (재시도 포함)
        for attempt in range(1, max_retries + 1):
            try:
                print(f"  [API 호출] {endpoint} (시도 {attempt}/{max_retries})")
                response = self.api.get(endpoint, params)

                if response["status"] == 200:
                    # 캐시 저장
                    if use_cache:
                        self._save_cache(cache_path, response["data"])
                    return response["data"]
                else:
                    print(f"  [오류] {response.get('error', '알 수 없는 오류')}")

            except Exception as e:
                print(f"  [예외] {e}")

            if attempt < max_retries:
                wait_time = attempt * 0.5
                print(f"  [대기] {wait_time}초 후 재시도...")
                time.sleep(wait_time)

        print(f"  [실패] 최대 재시도 횟수 초과: {endpoint}")
        return None

    def collect_all_weather(self):
        """모든 도시의 날씨 데이터를 수집합니다."""
        return self.collect("/api/weather/all")

    def collect_exchange_rates(self):
        """환율 데이터를 수집합니다."""
        return self.collect("/api/exchange")

    def collect_stock_prices(self):
        """주식 시세 데이터를 수집합니다."""
        return self.collect("/api/stock")


def save_collected_data(data, filepath):
    """수집된 데이터를 JSON 파일로 저장합니다."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  저장 완료: {filepath}")


if __name__ == "__main__":
    print("=" * 60)
    print("  API 데이터 수집기")
    print("=" * 60)
    print()

    collector = APICollector()
    output_dir = "/tmp/dashboard-data/api"

    # 1. 날씨 데이터 수집
    print("[1] 날씨 데이터 수집")
    print("-" * 40)
    weather = collector.collect_all_weather()
    if weather:
        save_collected_data(weather, f"{output_dir}/weather.json")
        print("\n  수집된 날씨 데이터:")
        for city_data in weather:
            print(f"    {city_data['도시']}: {city_data['온도']}°C, "
                  f"{city_data['상태']}, 습도 {city_data['습도']}%")
    print()

    # 2. 환율 데이터 수집
    print("[2] 환율 데이터 수집")
    print("-" * 40)
    exchange = collector.collect_exchange_rates()
    if exchange:
        save_collected_data(exchange, f"{output_dir}/exchange.json")
        print("\n  수집된 환율 데이터:")
        for code, info in exchange.items():
            print(f"    {code} ({info['통화']}): {info['매매기준율']:,.2f}원")
    print()

    # 3. 주식 데이터 수집
    print("[3] 주식 시세 수집")
    print("-" * 40)
    stocks = collector.collect_stock_prices()
    if stocks:
        save_collected_data(stocks, f"{output_dir}/stocks.json")
        print("\n  수집된 주식 데이터:")
        for stock in stocks:
            sign = "+" if stock["전일대비"] >= 0 else ""
            print(f"    {stock['종목명']} ({stock['종목코드']}): "
                  f"{stock['현재가']:,}원 ({sign}{stock['전일대비']:,}, "
                  f"{sign}{stock['등락률']}%)")
    print()

    # 4. 캐시 테스트 - 같은 요청을 다시 보내면 캐시에서 가져옴
    print("[4] 캐시 동작 확인")
    print("-" * 40)
    weather_cached = collector.collect_all_weather()
    print("  -> 두 번째 호출 시 캐시에서 즉시 로드됨")
    print()

    # 5. 수집 결과 요약
    print("=" * 60)
    print("  수집 결과 요약")
    print("=" * 60)
    print(f"  날씨 데이터: {len(weather) if weather else 0}개 도시")
    print(f"  환율 데이터: {len(exchange) if exchange else 0}개 통화")
    print(f"  주식 데이터: {len(stocks) if stocks else 0}개 종목")
    print(f"  캐시 디렉토리: {collector.cache_dir}")

    cache_files = os.listdir(collector.cache_dir) if os.path.exists(collector.cache_dir) else []
    print(f"  캐시 파일 수: {len(cache_files)}개")
