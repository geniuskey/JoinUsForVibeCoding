"""
예제 12-5: 코드 스타일 통일 요청
==================================
일관되지 않은 코드 스타일을 PEP8 기준으로 통일하도록 AI에게 요청하는 예제입니다.

프롬프트: "코드 스타일이 뒤섞여 있어. PEP8 기준으로 통일해줘"
→ 들여쓰기, 명명 규칙, 공백 등을 일관되게 정리합니다.
"""


# --- 개선 전: 스타일이 뒤섞인 코드 ---
# (의도적으로 다양한 스타일 혼용)

class userProfile:                      # 클래스명: camelCase (잘못됨)
    def __init__(self, UserName, email): # 매개변수: PascalCase 혼용
        self.UserName=UserName           # 공백 없음
        self.email = email
        self.loginCount=0                # 공백 없음

    def GetDisplayName(self):            # 메서드: PascalCase (잘못됨)
        return self.UserName

    def increment_login(self):
        self.loginCount +=1              # 공백 불일치
        return self.loginCount

    def get_info_dict(self):
        return {"userName": self.UserName,  # 키: camelCase
                "Email": self.email,         # 키: PascalCase
                "login_count": self.loginCount}  # 키: snake_case


# --- "PEP8 기준으로 통일해줘" 요청 후 개선된 코드 ---

class UserProfile:                              # PascalCase 클래스명
    """사용자 프로필을 관리하는 클래스."""

    def __init__(self, username, email):         # snake_case 매개변수
        self.username = username                 # 공백 일관됨
        self.email = email
        self.login_count = 0                     # snake_case 속성

    def get_display_name(self):                  # snake_case 메서드
        """화면에 표시할 이름을 반환합니다."""
        return self.username

    def increment_login(self):
        """로그인 횟수를 1 증가시킵니다."""
        self.login_count += 1                    # 공백 일관됨
        return self.login_count

    def get_info_dict(self):
        """프로필 정보를 딕셔너리로 반환합니다."""
        return {
            "username": self.username,           # snake_case 키 통일
            "email": self.email,
            "login_count": self.login_count,
        }


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 55)
    print("[예제 12-5] 코드 스타일 통일 요청")
    print("=" * 55)

    # 개선 전 버전 실행
    print("\n[개선 전] 스타일이 뒤섞인 코드")
    print("-" * 40)
    old_user = userProfile("홍길동", "hong@example.com")
    old_user.increment_login()
    old_user.increment_login()
    print(f"  클래스명:   userProfile (camelCase)")
    print(f"  메서드명:   GetDisplayName (PascalCase)")
    print(f"  표시 이름:  {old_user.GetDisplayName()}")
    print(f"  정보 딕셔너리: {old_user.get_info_dict()}")
    print(f"  → 키 스타일이 뒤섞임: userName, Email, login_count")

    # 개선 후 버전 실행
    print()
    print("[개선 후] PEP8 통일 코드")
    print("-" * 40)
    new_user = UserProfile("홍길동", "hong@example.com")
    new_user.increment_login()
    new_user.increment_login()
    print(f"  클래스명:   UserProfile (PascalCase)")
    print(f"  메서드명:   get_display_name (snake_case)")
    print(f"  표시 이름:  {new_user.get_display_name()}")
    print(f"  정보 딕셔너리: {new_user.get_info_dict()}")
    print(f"  → 키 스타일 통일: username, email, login_count")

    # 스타일 비교 요약
    print()
    print("[PEP8 명명 규칙 요약]")
    print("-" * 55)
    rules = [
        ("클래스명", "userProfile", "UserProfile", "PascalCase"),
        ("함수/메서드", "GetDisplayName", "get_display_name", "snake_case"),
        ("변수/속성", "loginCount", "login_count", "snake_case"),
        ("매개변수", "UserName", "username", "snake_case"),
        ("상수", "maxRetry", "MAX_RETRY", "UPPER_SNAKE"),
    ]
    print(f"  {'항목':<12} {'잘못된 예':<18} {'올바른 예':<20} {'규칙'}")
    print(f"  {'-'*12} {'-'*18} {'-'*20} {'-'*12}")
    for category, wrong, correct, rule in rules:
        print(f"  {category:<12} {wrong:<18} {correct:<20} {rule}")

    print()
    print("Tip: AI에게 'PEP8 스타일로 통일해줘'라고 요청하면")
    print("     일관된 코드 스타일을 쉽게 적용할 수 있습니다.")
