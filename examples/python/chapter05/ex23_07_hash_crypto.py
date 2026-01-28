"""
예제 23-07: 해시와 암호화 기초
- hashlib으로 해시 생성
- secrets 모듈로 안전한 랜덤 값 생성
- 비밀번호 해싱과 검증

이 예제는 교육 목적으로 취약한 코드와 안전한 코드를 모두 보여줍니다.
"""

import hashlib
import secrets
import hmac
import time


# ============================================================
# ❌ 취약한 코드: 안전하지 않은 해시/비밀번호 처리
# ============================================================

def vulnerable_store_password(password: str) -> str:
    """
    ❌ 취약: MD5로 비밀번호 해싱 (솔트 없음)
    - MD5는 암호학적으로 깨진 해시 함수
    - 솔트가 없어 레인보우 테이블 공격에 취약
    - 동일한 비밀번호는 항상 같은 해시를 생성
    """
    # ❌ MD5 사용 금지!
    return hashlib.md5(password.encode()).hexdigest()


def vulnerable_check_password(password: str, stored_hash: str) -> bool:
    """
    ❌ 취약: 단순 문자열 비교 (타이밍 공격에 취약)
    """
    # ❌ == 연산자는 타이밍 공격에 취약
    password_hash = hashlib.md5(password.encode()).hexdigest()
    return password_hash == stored_hash


def vulnerable_generate_token() -> str:
    """
    ❌ 취약: random 모듈로 보안 토큰 생성
    - random은 예측 가능한 의사 난수 생성기
    - 보안 목적으로 사용하면 안 됨
    """
    import random
    # ❌ random은 보안용이 아닙니다!
    return ''.join(random.choice('abcdef0123456789') for _ in range(32))


# ============================================================
# ✅ 안전한 코드: 올바른 해시/암호화 사용
# ============================================================

def safe_hash_password(password: str, salt: bytes = None) -> tuple:
    """
    ✅ 안전: SHA-256 + 솔트로 비밀번호 해싱

    더 좋은 방법: hashlib.pbkdf2_hmac() 사용 (아래 best_hash_password 참조)

    Returns:
        (salt_hex, hash_hex) 튜플
    """
    if salt is None:
        # ✅ secrets로 안전한 랜덤 솔트 생성
        salt = secrets.token_bytes(32)

    # ✅ 솔트 + 비밀번호를 합쳐서 해싱
    salted = salt + password.encode('utf-8')
    password_hash = hashlib.sha256(salted).hexdigest()

    return salt.hex(), password_hash


def best_hash_password(password: str) -> str:
    """
    ✅ 최선: PBKDF2로 비밀번호 해싱 (권장)
    - PBKDF2: Password-Based Key Derivation Function 2
    - 반복 횟수로 무차별 대입 공격 속도를 늦춤
    - 솔트를 자동으로 포함

    Returns:
        "알고리즘$반복횟수$솔트$해시" 형식의 문자열
    """
    # ✅ 안전한 랜덤 솔트 생성
    salt = secrets.token_bytes(32)

    # ✅ PBKDF2-HMAC-SHA256, 반복 600,000회
    iterations = 600_000
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations
    )

    # 저장 형식: 알고리즘$반복횟수$솔트(hex)$해시(hex)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"


def best_verify_password(password: str, stored: str) -> bool:
    """
    ✅ PBKDF2 해시 비밀번호 검증
    - hmac.compare_digest()로 타이밍 공격 방지
    """
    parts = stored.split("$")
    if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
        return False

    iterations = int(parts[1])
    salt = bytes.fromhex(parts[2])
    stored_hash = parts[3]

    # 같은 솔트와 반복 횟수로 해시 재계산
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations
    )

    # ✅ 상수 시간 비교 (타이밍 공격 방지)
    return hmac.compare_digest(dk.hex(), stored_hash)


def safe_generate_token(length: int = 32) -> str:
    """
    ✅ 안전: secrets 모듈로 보안 토큰 생성
    - 암호학적으로 안전한 난수 생성기 사용
    """
    return secrets.token_hex(length)


def safe_generate_url_token(length: int = 32) -> str:
    """
    ✅ URL에 안전한 토큰 생성
    """
    return secrets.token_urlsafe(length)


def safe_generate_api_key() -> str:
    """
    ✅ API 키 형식의 토큰 생성
    """
    prefix = "sk"
    token = secrets.token_hex(24)
    return f"{prefix}-{token}"


# ============================================================
# ✅ 데이터 무결성 검증 (HMAC)
# ============================================================

def create_signed_message(message: str, secret_key: str) -> str:
    """
    ✅ HMAC으로 메시지에 서명
    - 메시지가 변조되지 않았음을 검증할 수 있음
    """
    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return f"{message}|{signature}"


def verify_signed_message(signed_message: str, secret_key: str) -> tuple:
    """
    ✅ HMAC 서명 검증
    Returns:
        (is_valid, original_message)
    """
    if "|" not in signed_message:
        return False, ""

    message, received_sig = signed_message.rsplit("|", 1)

    expected_sig = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    # ✅ 상수 시간 비교
    is_valid = hmac.compare_digest(expected_sig, received_sig)
    return is_valid, message


# ============================================================
# ✅ 파일 해시 (무결성 확인)
# ============================================================

def calculate_file_hash(filepath: str, algorithm: str = "sha256") -> str:
    """
    ✅ 파일의 해시를 계산 (무결성 확인용)
    - 대용량 파일도 메모리 효율적으로 처리
    """
    h = hashlib.new(algorithm)

    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


# ============================================================
# 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("예제 23-07: 해시와 암호화 기초")
    print("=" * 60)

    test_password = "MyP@ssw0rd123!"

    # --- ❌ 취약한 코드 시연 ---
    print("\n--- ❌ 취약한 코드: MD5 + 솔트 없음 ---")

    md5_hash = vulnerable_store_password(test_password)
    print(f"  비밀번호: {test_password}")
    print(f"  MD5 해시: {md5_hash}")

    # 같은 비밀번호 = 같은 해시 (문제!)
    md5_hash2 = vulnerable_store_password(test_password)
    print(f"  같은 비밀번호 재해싱: {md5_hash2}")
    print(f"  동일 여부: {md5_hash == md5_hash2} (항상 같음 = 레인보우 테이블에 취약!)")

    print("\n  ❌ 취약한 토큰 생성:")
    token1 = vulnerable_generate_token()
    print(f"  random 토큰: {token1}")
    print("  -> random 모듈은 예측 가능하여 보안 목적에 부적합!")

    # --- ✅ 안전한 코드 시연 ---
    print("\n\n--- ✅ 안전한 코드: SHA-256 + 솔트 ---")

    salt1, hash1 = safe_hash_password(test_password)
    salt2, hash2 = safe_hash_password(test_password)
    print(f"  비밀번호: {test_password}")
    print(f"  해시 1: salt={salt1[:16]}... hash={hash1[:32]}...")
    print(f"  해시 2: salt={salt2[:16]}... hash={hash2[:32]}...")
    print(f"  동일 여부: {hash1 == hash2} (매번 다름 = 레인보우 테이블 방지!)")

    # --- ✅ PBKDF2 (권장) ---
    print("\n\n--- ✅ 최선: PBKDF2-HMAC-SHA256 (권장) ---")

    print(f"  비밀번호 해싱 중... (반복 600,000회)")
    start = time.time()
    stored = best_hash_password(test_password)
    elapsed = time.time() - start
    print(f"  저장 형식: {stored[:60]}...")
    print(f"  해싱 시간: {elapsed:.3f}초 (느릴수록 무차별 대입에 강함)")

    # 검증
    print(f"\n  올바른 비밀번호 검증: {best_verify_password(test_password, stored)}")
    print(f"  틀린 비밀번호 검증: {best_verify_password('wrong_password', stored)}")

    # --- ✅ 안전한 토큰 생성 ---
    print("\n\n--- ✅ 안전한 토큰 생성 (secrets 모듈) ---")

    print(f"  hex 토큰: {safe_generate_token(32)}")
    print(f"  URL 토큰: {safe_generate_url_token(32)}")
    print(f"  API 키:   {safe_generate_api_key()}")

    # secrets 모듈의 다른 기능
    print(f"\n  랜덤 정수 (0~999): {secrets.randbelow(1000)}")
    print(f"  랜덤 바이트 (8): {secrets.token_bytes(8).hex()}")

    # --- ✅ HMAC 메시지 서명 ---
    print("\n\n--- ✅ HMAC 메시지 서명/검증 ---")

    secret = "my-secret-key"
    message = "주문번호:12345,금액:50000원"

    signed = create_signed_message(message, secret)
    print(f"  원본 메시지: {message}")
    print(f"  서명된 메시지: {signed[:60]}...")

    # 정상 검증
    is_valid, original = verify_signed_message(signed, secret)
    print(f"\n  정상 검증: 유효={is_valid}, 메시지='{original}'")

    # 변조된 메시지 검증
    tampered = signed.replace("50000", "99999")
    is_valid, _ = verify_signed_message(tampered, secret)
    print(f"  변조 검증: 유효={is_valid} (변조 감지!)")

    # 잘못된 키로 검증
    is_valid, _ = verify_signed_message(signed, "wrong-key")
    print(f"  잘못된 키: 유효={is_valid} (위조 감지!)")

    # --- 해시 알고리즘 비교 ---
    print("\n\n--- 해시 알고리즘 비교 ---")
    test_data = "Hello, 바이브 코딩!".encode('utf-8')

    algorithms = ['md5', 'sha1', 'sha256', 'sha512']
    for algo in algorithms:
        h = hashlib.new(algo, test_data)
        security = "❌ 취약" if algo in ['md5', 'sha1'] else "✅ 안전"
        print(f"  {algo:8s} ({h.digest_size*8:3d}비트) {security}: {h.hexdigest()[:40]}...")

    print("\n" + "=" * 60)
    print("핵심 원칙:")
    print("  1. 비밀번호는 PBKDF2 또는 bcrypt/scrypt로 해싱하세요")
    print("  2. MD5, SHA-1은 비밀번호 해싱에 사용하지 마세요")
    print("  3. 솔트를 반드시 사용하세요 (레인보우 테이블 방지)")
    print("  4. 보안 토큰은 secrets 모듈을 사용하세요 (random 금지)")
    print("  5. 비교 시 hmac.compare_digest()를 사용하세요")
    print("")
    print("바이브 코딩 팁: AI에게 '비밀번호를 PBKDF2로 안전하게")
    print("              해싱하는 코드를 만들어줘'라고 요청하세요.")
    print("=" * 60)
