"""
예제 20-02: 모듈 분리 예시
하나의 큰 파일을 역할별로 분리하는 방법을 보여줍니다.
분리 전/후를 비교하여 모듈화의 장점을 이해합니다.
"""


# ============================================================
# [분리 전] 모든 것이 한 파일에 섞여 있는 코드
# ============================================================

def show_monolithic_code():
    """모든 기능이 하나의 파일에 섞여 있는 예시를 보여줍니다."""
    print("=" * 60)
    print("[분리 전] 모든 코드가 한 파일에 있는 경우")
    print("=" * 60)
    print()

    # 데이터 검증, 비즈니스 로직, 출력이 모두 섞여 있음
    monolithic_code = '''
# app.py - 모든 것이 한 파일에!

users = []  # 전역 변수

def register(name, email, age):
    # 검증 로직
    if not name or len(name) < 2:
        return "이름은 2자 이상이어야 합니다"
    if "@" not in email:
        return "올바른 이메일 형식이 아닙니다"
    if age < 0 or age > 150:
        return "올바른 나이를 입력하세요"

    # 비즈니스 로직
    user = {"name": name, "email": email, "age": age}
    users.append(user)

    # 출력 로직
    print(f"가입 완료: {name} ({email})")
    return user

def list_users():
    # 비즈니스 로직 + 출력 로직 혼합
    print(f"총 {len(users)}명의 사용자:")
    for u in users:
        category = "미성년자" if u["age"] < 19 else "성인"
        print(f"  - {u['name']} ({u['email']}) [{category}]")
'''.strip()

    for line in monolithic_code.split("\n"):
        print(f"    {line}")
    print()
    print("  문제점: 검증, 비즈니스 로직, 출력이 모두 섞여 있음")
    print("         테스트하기 어렵고, 수정 시 다른 부분에 영향을 줌")


# ============================================================
# [분리 후] 역할별로 나눈 모듈들
# ============================================================

# --- validators.py 역할 ---
class Validators:
    """입력값 검증을 담당하는 모듈"""

    @staticmethod
    def validate_name(name):
        """이름 유효성 검사"""
        if not name or not isinstance(name, str):
            return False, "이름은 비어있을 수 없습니다"
        if len(name) < 2:
            return False, "이름은 2자 이상이어야 합니다"
        return True, "유효한 이름입니다"

    @staticmethod
    def validate_email(email):
        """이메일 유효성 검사"""
        if not email or "@" not in email:
            return False, "올바른 이메일 형식이 아닙니다"
        if "." not in email.split("@")[1]:
            return False, "이메일 도메인이 올바르지 않습니다"
        return True, "유효한 이메일입니다"

    @staticmethod
    def validate_age(age):
        """나이 유효성 검사"""
        if not isinstance(age, int):
            return False, "나이는 정수여야 합니다"
        if age < 0 or age > 150:
            return False, "나이는 0~150 사이여야 합니다"
        return True, "유효한 나이입니다"


# --- models.py 역할 ---
class User:
    """사용자 데이터 모델"""

    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    @property
    def category(self):
        """나이 기반 분류"""
        if self.age < 19:
            return "미성년자"
        elif self.age < 65:
            return "성인"
        else:
            return "시니어"

    def to_dict(self):
        return {"name": self.name, "email": self.email, "age": self.age}

    def __repr__(self):
        return f"User(name='{self.name}', email='{self.email}', age={self.age})"


# --- services.py 역할 ---
class UserService:
    """사용자 관련 비즈니스 로직"""

    def __init__(self):
        self._users = []

    def register(self, name, email, age):
        """새 사용자 등록 (검증 포함)"""
        # 검증은 Validators 모듈에 위임
        for validator, value in [
            (Validators.validate_name, name),
            (Validators.validate_email, email),
            (Validators.validate_age, age),
        ]:
            is_valid, message = validator(value)
            if not is_valid:
                return None, message

        user = User(name, email, age)
        self._users.append(user)
        return user, "등록 성공"

    def get_all_users(self):
        """전체 사용자 목록 반환"""
        return list(self._users)

    def find_by_name(self, name):
        """이름으로 사용자 검색"""
        return [u for u in self._users if name in u.name]

    @property
    def user_count(self):
        return len(self._users)


# --- formatters.py 역할 ---
class UserFormatter:
    """사용자 정보 출력 포맷 담당"""

    @staticmethod
    def format_user(user):
        return f"{user.name} ({user.email}) [{user.category}]"

    @staticmethod
    def format_user_list(users):
        if not users:
            return "등록된 사용자가 없습니다."
        lines = [f"총 {len(users)}명의 사용자:"]
        for user in users:
            lines.append(f"  - {UserFormatter.format_user(user)}")
        return "\n".join(lines)


def show_modular_code():
    """모듈로 분리된 코드의 구조를 보여줍니다."""
    print()
    print("=" * 60)
    print("[분리 후] 역할별로 모듈을 나눈 경우")
    print("=" * 60)
    print()

    module_structure = {
        "validators.py": "입력값 검증 (이름, 이메일, 나이)",
        "models.py": "데이터 모델 정의 (User 클래스)",
        "services.py": "비즈니스 로직 (등록, 검색)",
        "formatters.py": "출력 포맷 담당",
    }

    print("모듈 구조:")
    for module, role in module_structure.items():
        print(f"  {module:<20s} → {role}")
    print()
    print("  장점:")
    print("    1. 각 모듈의 역할이 명확함")
    print("    2. 독립적으로 테스트 가능")
    print("    3. 수정 시 영향 범위가 제한됨")
    print("    4. 코드 재사용이 쉬움")


def demo_modular_usage():
    """분리된 모듈을 실제로 사용하는 데모"""
    print()
    print("=" * 60)
    print("분리된 모듈 사용 데모")
    print("=" * 60)
    print()

    service = UserService()

    # 사용자 등록 테스트
    test_cases = [
        ("김바이브", "vibe@example.com", 25),
        ("이코딩", "coding@test.co.kr", 17),
        ("박파이썬", "python@dev.io", 30),
        ("", "bad@email.com", 25),          # 이름 검증 실패
        ("홍길동", "no-at-sign", 25),       # 이메일 검증 실패
        ("최개발", "dev@good.com", -5),     # 나이 검증 실패
    ]

    print("--- 사용자 등록 테스트 ---")
    for name, email, age in test_cases:
        user, message = service.register(name, email, age)
        if user:
            print(f"  성공: {UserFormatter.format_user(user)}")
        else:
            input_info = f"('{name}', '{email}', {age})"
            print(f"  실패: {message} {input_info}")

    print()
    print("--- 등록된 사용자 목록 ---")
    print(UserFormatter.format_user_list(service.get_all_users()))

    print()
    print("--- 이름 검색: '이' ---")
    results = service.find_by_name("이")
    for user in results:
        print(f"  {UserFormatter.format_user(user)}")

    if not results:
        print("  검색 결과 없음")


if __name__ == "__main__":
    # 1단계: 분리 전 코드 보여주기
    show_monolithic_code()

    # 2단계: 분리 후 구조 보여주기
    show_modular_code()

    # 3단계: 실제 사용 데모
    demo_modular_usage()

    print()
    print("모듈 분리 예시를 성공적으로 실행했습니다!")
