# Chapter 23: 보안 고려사항

소프트웨어 개발에서 보안은 선택이 아닌 필수입니다. 특히 바이브 코딩으로 AI가 생성한 코드를 사용할 때는 보안에 대한 이해가 더욱 중요합니다. AI는 기능적으로 올바른 코드를 생성하지만, 보안 취약점이 포함된 코드를 만들 수도 있습니다. 이 장에서는 소프트웨어 보안의 기본 원칙부터 실전에서 마주치는 주요 취약점, 그리고 AI 생성 코드를 안전하게 검토하는 방법까지 체계적으로 배웁니다.

---

## 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- **보안의 중요성**을 이해하고 개발 초기부터 보안을 고려할 수 있다
- **OWASP Top 10** 등 일반적인 웹 보안 취약점을 설명할 수 있다
- **입력 검증** 코드를 작성하여 외부 입력을 안전하게 처리할 수 있다
- **SQL 인젝션**의 원리를 이해하고 파라미터화 쿼리로 방지할 수 있다
- **명령어 인젝션**과 **경로 순회** 공격을 방지할 수 있다
- 비밀번호, API 키 등 **민감 정보**를 안전하게 관리할 수 있다
- **해시와 암호화**의 기본 원리를 이해하고 올바르게 적용할 수 있다
- AI가 생성한 코드의 **보안 취약점을 검토**하고 수정할 수 있다
- 보안 체크리스트를 활용하여 **체계적인 보안 검토**를 수행할 수 있다

---

## 23.1 보안이 왜 중요한가?

프로그래밍을 배우기 시작하면 "동작하는 코드"를 만드는 데 집중하게 됩니다. 기능이 정상적으로 작동하면 완성이라고 생각하기 쉽습니다. 하지만 실제 서비스에서는 "동작하는 코드"만으로는 충분하지 않습니다. **안전하게 동작하는 코드**가 필요합니다.

### 보안 사고의 현실

보안 취약점은 단순한 기술적 문제가 아닙니다. 실제 피해로 이어집니다:

| 위협 유형 | 발생 가능한 피해 |
|-----------|-----------------|
| 개인정보 유출 | 사용자의 이름, 이메일, 비밀번호 등이 외부에 노출 |
| 데이터 변조 | 주문 금액 변경, 계정 권한 탈취 등 |
| 서비스 마비 | 서비스가 중단되어 사업적 손실 발생 |
| 금전적 피해 | 결제 정보 유출, 랜섬웨어 등으로 직접적 금전 손실 |
| 신뢰도 하락 | 기업의 평판 손상, 고객 이탈 |

### "나중에 보안을 추가하겠다"는 위험한 생각

많은 개발자가 "일단 기능부터 만들고, 보안은 나중에 추가하자"고 생각합니다. 하지만 이 접근 방식에는 심각한 문제가 있습니다:

1. **나중에**는 결코 오지 않습니다 -- 새로운 기능 요청이 계속 들어옵니다
2. **구조적 문제**는 사후에 수정하기 어렵습니다 -- 보안은 설계 단계부터 고려해야 합니다
3. **이미 유출된 데이터**는 되돌릴 수 없습니다 -- 사후 대응은 의미가 없습니다

> **Warning:** 보안은 개발의 마지막이 아닌 **처음부터** 고려해야 합니다. 바이브 코딩에서 AI에게 코드를 요청할 때도 "보안을 고려해서 작성해줘"라고 명시적으로 요청하세요.

### 바이브 코딩에서의 보안

AI가 생성한 코드는 기능적으로 올바르게 동작할 수 있지만, 보안 관점에서는 취약할 수 있습니다. AI는 다음과 같은 문제를 일으킬 수 있습니다:

- **편의를 위해 보안을 생략**: 짧고 간단한 예제를 선호하여 입력 검증을 생략
- **오래된 패턴 사용**: 더 이상 안전하지 않은 함수나 알고리즘 사용
- **하드코딩된 값**: API 키나 비밀번호를 코드에 직접 작성
- **불완전한 에러 처리**: 내부 정보가 에러 메시지로 노출

따라서 바이브 코딩을 할 때는 AI가 생성한 코드를 **보안 관점에서 반드시 검토**하는 습관이 중요합니다.

> **Tip:** AI에게 코드를 요청할 때 "보안 모범 사례를 따르는 코드를 작성해줘", "입력 검증을 포함해줘", "OWASP Top 10을 고려해줘" 같은 프롬프트를 추가하면 더 안전한 코드를 얻을 수 있습니다.

---

## 23.2 일반적인 취약점 이해하기 (OWASP)

**OWASP(Open Web Application Security Project)**는 웹 애플리케이션 보안을 위한 비영리 단체로, 가장 흔하고 위험한 보안 취약점 목록인 **OWASP Top 10**을 정기적으로 발표합니다.

### OWASP Top 10 주요 항목

웹 애플리케이션에서 자주 발생하는 취약점을 요약하면 다음과 같습니다:

| 순위 | 취약점 | 설명 | 이 장에서 다루는 내용 |
|------|--------|------|---------------------|
| 1 | **인젝션** | SQL, OS 명령 등에 악의적 입력 삽입 | 23.4, 23.5, 23.6 |
| 2 | **인증 실패** | 약한 비밀번호, 세션 관리 부실 | 23.8 |
| 3 | **민감 데이터 노출** | 비밀번호, API 키 등이 평문으로 노출 | 23.7, 23.8 |
| 4 | **보안 설정 오류** | 디버그 모드, 기본 비밀번호 등 | 23.7 |
| 5 | **입력 검증 부재** | 외부 입력을 검증하지 않고 사용 | 23.3 |

### 보안의 기본 원칙

이러한 취약점을 방지하기 위한 핵심 원칙들이 있습니다:

**1. 신뢰 경계(Trust Boundary) 인식**

프로그램 안에는 "신뢰할 수 있는 영역"과 "신뢰할 수 없는 영역"이 있습니다. 사용자 입력, 외부 API 응답, 파일 내용 등 외부에서 들어오는 모든 데이터는 **신뢰할 수 없는 데이터**입니다.

```
신뢰할 수 없는 입력:                신뢰할 수 있는 영역:
┌─────────────────────┐            ┌─────────────────────┐
│ - 사용자 입력       │            │                     │
│ - URL 파라미터      │  ──검증──> │  프로그램 내부 로직  │
│ - API 응답          │            │                     │
│ - 파일 내용         │            │                     │
│ - 환경 변수         │            │                     │
└─────────────────────┘            └─────────────────────┘
```

**2. 최소 권한 원칙(Least Privilege)**

프로그램이나 사용자에게 필요한 최소한의 권한만 부여합니다. 읽기만 필요한 작업에 쓰기 권한을 주지 않고, 특정 테이블만 접근하면 되는 DB 사용자에게 전체 DB 관리자 권한을 주지 않습니다.

**3. 심층 방어(Defense in Depth)**

한 가지 보안 장치에만 의존하지 않고 여러 겹의 보안을 적용합니다. 입력 검증, 파라미터화 쿼리, 출력 인코딩을 동시에 적용하는 것이 그 예입니다.

> **Note:** OWASP Top 10은 웹 애플리케이션에 초점을 맞추지만, 여기서 배우는 원칙들은 CLI 도구, 데스크톱 앱, API 서버 등 모든 종류의 프로그램에 적용됩니다.

---

## 23.3 입력 검증

**모든 외부 입력은 신뢰하지 않는다** -- 이것이 보안의 가장 기본적인 원칙입니다. 사용자가 입력한 데이터는 반드시 검증한 후 사용해야 합니다.

### 검증 없는 코드의 위험

입력을 검증하지 않으면 어떤 문제가 발생할까요? 다음은 검증 없이 사용자 정보를 그대로 저장하는 취약한 코드입니다:

```python
# ❌ 취약: 입력값을 검증하지 않고 그대로 사용
def vulnerable_create_user(username: str, age: str, email: str) -> dict:
    return {
        "username": username,   # 빈 문자열도 허용됨
        "age": age,             # 문자열이 들어와도 그대로 저장
        "email": email,         # 이메일 형식을 확인하지 않음
        "status": "created"
    }
```

이 코드는 빈 문자열, 10,000자 길이의 문자열, HTML 태그가 포함된 입력 등 모든 것을 그대로 받아들입니다. 이는 XSS 공격, 데이터 오염, 서비스 장애 등으로 이어질 수 있습니다.

### 체계적인 입력 검증

안전한 코드는 **타입, 길이, 형식, 범위**를 모두 확인합니다.

**예제 23-01: 입력 검증 기초**

```python
# examples/python/chapter05/ex23_01_input_validation.py

import re
from typing import Optional

class ValidationError(Exception):
    """입력 검증 실패 시 발생하는 예외"""
    pass

def validate_username(username: str) -> str:
    """
    ✅ 사용자 이름 검증
    - 타입 확인: 문자열인지
    - 길이 확인: 3~20자
    - 문자 확인: 영문, 숫자, 밑줄만 허용
    """
    if not isinstance(username, str):
        raise ValidationError("사용자 이름은 문자열이어야 합니다")

    username = username.strip()

    if len(username) < 3:
        raise ValidationError(
            f"사용자 이름이 너무 짧습니다 (최소 3자, 현재 {len(username)}자)"
        )
    if len(username) > 20:
        raise ValidationError(
            f"사용자 이름이 너무 깁니다 (최대 20자, 현재 {len(username)}자)"
        )
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError(
            "사용자 이름은 영문, 숫자, 밑줄(_)만 사용할 수 있습니다"
        )
    return username

def validate_age(age_input: str) -> int:
    """✅ 나이 검증: 문자열 -> 정수 변환 + 범위 확인"""
    try:
        age = int(age_input)
    except (ValueError, TypeError):
        raise ValidationError(f"나이는 숫자여야 합니다: '{age_input}'")

    if age < 1 or age > 150:
        raise ValidationError(f"나이는 1~150 사이여야 합니다: {age}")
    return age

def validate_email(email: str) -> str:
    """✅ 이메일 검증: 형식 + 길이 확인"""
    if not isinstance(email, str):
        raise ValidationError("이메일은 문자열이어야 합니다")

    email = email.strip().lower()
    if len(email) > 254:
        raise ValidationError("이메일이 너무 깁니다 (최대 254자)")

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValidationError(f"올바른 이메일 형식이 아닙니다: '{email}'")
    return email
```

이 코드의 핵심 검증 전략을 정리하면 다음과 같습니다:

| 검증 단계 | 확인 내용 | 예시 |
|-----------|----------|------|
| **타입 검증** | 예상하는 타입인지 | `isinstance(username, str)` |
| **길이 검증** | 최소/최대 길이 충족 여부 | `3 <= len(username) <= 20` |
| **형식 검증** | 허용된 문자/패턴만 포함 | `re.match(r'^[a-zA-Z0-9_]+$', ...)` |
| **범위 검증** | 값이 유효 범위 안에 있는지 | `1 <= age <= 150` |

### 문자열 정제(Sanitization)

검증과 함께 **정제**도 중요합니다. 정제는 위험한 내용을 제거하거나 변환하는 과정입니다.

```python
def sanitize_string(text: str, max_length: int = 255,
                    allow_html: bool = False) -> str:
    """
    ✅ 문자열 정제(Sanitization)
    - 앞뒤 공백 제거
    - 길이 제한
    - HTML 태그 제거 (선택)
    """
    if not isinstance(text, str):
        raise ValidationError("문자열이 아닙니다")

    text = text.strip()
    if len(text) > max_length:
        text = text[:max_length]

    if not allow_html:
        text = re.sub(r'<[^>]+>', '', text)

    return text
```

**실행:**

```bash
$ python examples/python/chapter05/ex23_01_input_validation.py
```

**결과:**

```
--- ❌ 취약한 코드: 검증 없는 사용자 생성 ---
빈 입력 허용됨: {'username': '', 'age': '', 'email': '', 'status': 'created'}
비정상 입력 허용됨: username 길이=10000, age='abc', email='not-email'

--- ✅ 안전한 코드: 검증된 사용자 생성 ---
정상 생성: {'username': 'john_doe', 'age': 25, 'email': 'john@example.com', ...}

--- 다양한 비정상 입력 테스트 ---
  [빈 사용자 이름] 차단됨 -> 사용자 이름이 너무 짧습니다 (최소 3자, 현재 0자)
  [너무 짧은 이름] 차단됨 -> 사용자 이름이 너무 짧습니다 (최소 3자, 현재 2자)
  [나이에 문자열] 차단됨 -> 나이는 숫자여야 합니다: 'abc'
  [범위 초과 나이] 차단됨 -> 나이는 1~150 사이여야 합니다: 200
  [잘못된 이메일] 차단됨 -> 올바른 이메일 형식이 아닙니다: 'not-email'
  [특수문자 이름] 차단됨 -> 사용자 이름은 영문, 숫자, 밑줄(_)만 사용할 수 있습니다

--- ✅ 문자열 정제(Sanitization) ---
  원본: '  <script>alert('XSS')</script>안녕하세요  '
  정제: 'alert('XSS')안녕하세요'
```

검증 없는 코드에서는 모든 비정상 입력이 허용되지만, 안전한 코드에서는 각각 적절한 오류 메시지와 함께 차단됩니다.

> **Tip:** 바이브 코딩에서 AI에게 코드를 요청할 때 **"입력 검증 코드를 추가해줘"**, **"모든 외부 입력을 검증하는 코드를 포함해줘"** 라고 명시적으로 요청하세요. 기본적으로 AI는 검증을 생략하는 경우가 많습니다.

---

## 23.4 SQL 인젝션 방지

**SQL 인젝션(SQL Injection)**은 가장 오래되었지만 여전히 가장 위험한 공격 중 하나입니다. 사용자 입력이 SQL 쿼리에 직접 삽입될 때 발생하며, 공격자가 데이터베이스를 자유롭게 조작할 수 있게 됩니다.

### SQL 인젝션의 원리

SQL 인젝션은 "사용자 입력"이 "SQL 명령어"로 해석되는 데서 발생합니다. 다음 코드를 보겠습니다:

```python
# ❌ 취약: 사용자 입력을 SQL 쿼리에 직접 삽입
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

정상적인 사용자가 `alice`와 `alice_pass_456`을 입력하면:

```sql
SELECT * FROM users WHERE username = 'alice' AND password = 'alice_pass_456'
```

하지만 공격자가 `username`에 `' OR '1'='1' --`를 입력하면:

```sql
SELECT * FROM users WHERE username = '' OR '1'='1' --' AND password = '아무거나'
```

`'1'='1'`은 항상 참이고, `--`는 뒤의 내용을 주석 처리합니다. 결과적으로 **모든 사용자의 정보가 유출**됩니다.

> **Warning:** SQL 인젝션은 인증 우회, 데이터 유출, 데이터 삭제, 심지어 서버 장악까지 가능하게 합니다. 절대 사용자 입력을 SQL 쿼리에 직접 삽입하지 마세요!

### 파라미터화 쿼리로 방지

**예제 23-02: SQL 인젝션 취약 코드 vs 안전한 코드**

```python
# examples/python/chapter05/ex23_02_sql_injection.py

import sqlite3

# ❌ 취약한 코드: 문자열 포맷팅으로 SQL 쿼리 생성
def vulnerable_login(db_path, username, password):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # ❌ 절대 이렇게 하면 안 됩니다!
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# ✅ 안전한 코드: 파라미터화 쿼리 사용
def safe_login(db_path, username, password):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # ✅ ? 플레이스홀더를 사용하여 값을 별도로 전달
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    results = cursor.fetchall()
    conn.close()
    return results
```

파라미터화 쿼리는 `?` 플레이스홀더를 사용하여 SQL 구조와 데이터를 **완전히 분리**합니다. 데이터베이스 드라이버가 자동으로 이스케이프 처리를 하므로 SQL 인젝션이 불가능합니다.

### 모든 SQL 작업에 파라미터화 적용

SELECT뿐만 아니라 INSERT, UPDATE, DELETE, LIKE 검색에도 모두 파라미터화 쿼리를 사용해야 합니다:

```python
# ✅ INSERT도 파라미터화
cursor.execute(
    "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
    (username, password_hash, email)
)

# ✅ UPDATE도 파라미터화
cursor.execute(
    "UPDATE users SET email = ? WHERE id = ?",
    (new_email, user_id)
)

# ✅ LIKE 검색도 파라미터화
cursor.execute(
    "SELECT username, email FROM users WHERE username LIKE ?",
    (f"%{search_term}%",)
)
```

**실행:**

```bash
$ python examples/python/chapter05/ex23_02_sql_injection.py
```

**결과:**

```
--- ❌ 취약한 코드: SQL 인젝션 공격 시연 ---

[1] 정상 로그인 시도:
  결과: 1명 찾음 - 성공

[2] ❌ SQL 인젝션 공격 - 인증 우회:
  공격 입력: username = "' OR '1'='1' --"
  결과: 3명의 정보가 유출됨!
    -> ID:1, 이름:admin, 비밀번호:super_secret_123, ...
    -> ID:2, 이름:alice, 비밀번호:alice_pass_456, ...

--- ✅ 안전한 코드: 파라미터화 쿼리 ---

[2] ✅ 같은 SQL 인젝션 공격 시도 -> 차단:
  결과: 0명 찾음 - 공격 차단! (0명이어야 정상)
```

취약한 코드에서는 공격자의 입력이 SQL 명령어로 해석되어 모든 사용자 정보가 유출되지만, 파라미터화 쿼리를 사용한 코드에서는 공격이 완전히 차단됩니다.

> **Note:** 다른 데이터베이스에서도 파라미터화 쿼리 문법이 있습니다. MySQL은 `%s`, PostgreSQL은 `%s` 또는 `$1`, Oracle은 `:name` 형식을 사용합니다. 어떤 데이터베이스를 사용하든 원칙은 동일합니다: **사용자 입력을 SQL 문자열에 직접 넣지 마세요**.

---

## 23.5 명령어 인젝션 방지

**명령어 인젝션(Command Injection)**은 프로그램이 외부 명령을 실행할 때, 사용자 입력이 운영체제 명령으로 해석되는 공격입니다. SQL 인젝션과 원리는 같지만, 대상이 SQL이 아닌 **운영체제 셸(Shell)**이라는 점이 다릅니다.

### shell=True의 위험성

Python의 `subprocess` 모듈에서 `shell=True` 옵션을 사용하면, 명령어가 셸을 통해 해석됩니다. 이때 사용자 입력에 세미콜론(`;`), 파이프(`|`), 백틱(`` ` ``) 등의 셸 특수문자가 포함되면 추가 명령이 실행됩니다.

**예제 23-03: 명령어 인젝션 취약 코드 vs 안전한 코드**

```python
# examples/python/chapter05/ex23_03_command_injection.py

import subprocess
import shlex
import re

# ❌ 취약: shell=True와 문자열 포맷팅
def vulnerable_ping(host: str) -> str:
    # ❌ shell=True + 문자열 포맷팅 = 명령어 인젝션 취약!
    command = f"echo '[시뮬레이션] ping -c 1 {host}'"
    result = subprocess.run(command, shell=True,
                            capture_output=True, text=True)
    return result.stdout

# ✅ 안전: 리스트 형태 인자와 shell=False
def safe_ping(host: str) -> str:
    # 입력 검증: 호스트명에 허용된 문자만 포함
    if not re.match(r'^[a-zA-Z0-9.\-]+$', host):
        return f"오류: 올바른 호스트명이 아닙니다: '{host}'"

    # ✅ 리스트 형태로 인자 전달 - 셸 해석 없음
    command = ["echo", f"[시뮬레이션] ping -c 1 {host}"]
    result = subprocess.run(command, capture_output=True, text=True,
                            timeout=10)  # ✅ 타임아웃 설정
    return result.stdout
```

`shell=True`를 사용하면 `127.0.0.1; cat /etc/passwd` 같은 입력으로 추가 명령을 실행할 수 있습니다. 반면 리스트 인자를 사용하면 전체 문자열이 하나의 인자로 전달되어 셸 해석이 일어나지 않습니다.

### 불가피하게 셸을 사용해야 할 때

파이프(`|`)나 리디렉션(`>`)이 필요하여 불가피하게 `shell=True`를 사용해야 한다면, `shlex.quote()`로 사용자 입력을 이스케이프해야 합니다:

```python
import shlex

def safe_shell_command(user_input: str) -> str:
    # ✅ shlex.quote()로 셸 이스케이프
    safe_input = shlex.quote(user_input)
    command = f"echo '입력값:' {safe_input}"
    result = subprocess.run(command, shell=True,
                            capture_output=True, text=True)
    return result.stdout
```

**실행:**

```bash
$ python examples/python/chapter05/ex23_03_command_injection.py
```

**결과:**

```
--- ❌ 취약한 코드: 명령어 인젝션 가능 ---

[2] ❌ 명령어 인젝션 공격:
  결과: [시뮬레이션] ping -c 1 127.0.0.1
해킹 성공! 시스템 명령 실행됨
  -> 세미콜론(;) 뒤의 명령도 실행되었습니다!

--- ✅ 안전한 코드: 명령어 인젝션 차단 ---

[2] ✅ 같은 인젝션 공격 시도 -> 차단:
  결과: 오류: 올바른 호스트명이 아닙니다: '127.0.0.1; echo '해킹 성공!''
  -> 입력 검증에 의해 차단되었습니다!
```

### 명령어 인젝션 방지 체크리스트

| 규칙 | 설명 |
|------|------|
| `subprocess`는 리스트 인자 + `shell=False` 사용 | 셸 해석 없이 직접 실행 |
| `os.system()` 사용 금지 | 항상 셸을 통해 실행되므로 위험 |
| 불가피한 경우 `shlex.quote()`로 이스케이프 | 셸 특수문자를 안전하게 처리 |
| 사용자 입력은 반드시 검증 후 사용 | 허용된 문자만 통과 |
| `timeout` 옵션 설정 | 무한 실행 방지 |

> **Warning:** `os.system()` 함수는 항상 셸을 통해 명령을 실행합니다. 이 함수는 **절대 사용하지 마세요**. 대신 `subprocess.run()`을 리스트 인자와 함께 사용하세요.

---

## 23.6 경로 순회 방지

**경로 순회(Path Traversal)**는 `../`(상위 디렉토리 이동)를 이용하여 허용된 디렉토리 밖의 파일에 접근하는 공격입니다. 파일 업로드, 다운로드, 읽기 기능이 있는 프로그램에서 자주 발생합니다.

### 경로 순회 공격의 원리

사용자가 `photo.txt`라는 정상적인 파일명 대신 `../../secret_config.txt`를 요청하면, 프로그램이 의도하지 않은 파일에 접근하게 됩니다:

```
의도한 경로: /app/uploads/photo.txt
공격 경로:   /app/uploads/../../secret_config.txt
실제 경로:   /secret_config.txt  (서버의 비밀 설정 파일!)
```

**예제 23-04: 경로 순회(Path Traversal) 방지**

```python
# examples/python/chapter05/ex23_04_path_traversal.py

from pathlib import Path

# ❌ 취약: 파일명을 검증 없이 경로에 연결
def vulnerable_read_file(base_dir: str, filename: str) -> str:
    uploads_dir = os.path.join(base_dir, "uploads")
    # ❌ 단순 문자열 연결 - 경로 순회에 취약!
    filepath = os.path.join(uploads_dir, filename)
    with open(filepath, "r") as f:
        return f.read()

# ✅ 안전: pathlib으로 경로를 정규화하고 허용 범위 확인
def safe_read_file(base_dir: str, filename: str) -> str:
    uploads_dir = Path(base_dir) / "uploads"

    # 1. 요청된 경로 구성 + 정규화
    requested_path = (uploads_dir / filename).resolve()

    # 2. ✅ 핵심: 정규화된 경로가 허용된 디렉토리 안에 있는지 확인
    uploads_resolved = uploads_dir.resolve()

    try:
        requested_path.relative_to(uploads_resolved)
    except ValueError:
        return "접근 거부: 허용된 디렉토리 밖의 파일입니다!"

    # 3. 파일 존재 확인 후 읽기
    if not requested_path.is_file():
        return "파일을 찾을 수 없습니다."
    return requested_path.read_text()
```

핵심은 `resolve()`로 경로를 정규화한 후, `relative_to()`로 정규화된 경로가 허용된 디렉토리 안에 있는지 검증하는 것입니다. `../`가 포함된 경로는 `resolve()` 과정에서 실제 경로로 변환되고, 이 경로가 허용 범위를 벗어나면 접근이 차단됩니다.

### 파일명 정제

사용자가 제공하는 파일명도 정제해야 합니다:

```python
def sanitize_filename(filename: str) -> str:
    """✅ 파일명 정제"""
    import re

    # Path 컴포넌트에서 파일명만 추출
    name = Path(filename).name

    # 숨김 파일 방지
    name = name.lstrip(".")

    # 위험한 문자 제거
    name = re.sub(r'[^a-zA-Z0-9가-힣._\-]', '_', name)

    if not name:
        name = "unnamed_file"
    return name
```

**실행:**

```bash
$ python examples/python/chapter05/ex23_04_path_traversal.py
```

**결과:**

```
--- ❌ 취약한 코드: 경로 순회 공격 가능 ---

[2] ❌ 경로 순회 공격 (../로 상위 디렉토리 접근):
  내용: DB_PASSWORD=super_secret_123
  -> 업로드 디렉토리 밖의 비밀 파일에 접근 성공!

--- ✅ 안전한 코드: pathlib으로 경로 순회 차단 ---

[2] ✅ 같은 경로 순회 공격 시도 -> 차단:
  결과: 접근 거부: 허용된 디렉토리 밖의 파일입니다!

--- ✅ 파일명 정제(Sanitization) ---
  '../../../etc/passwd' -> 'passwd'
  '.hidden_file' -> 'hidden_file'
  '<script>alert.js' -> '_script_alert.js'
```

> **Note:** `os.path.join()`만으로는 경로 순회를 방지할 수 없습니다. `os.path.join("/uploads", "../secret.txt")`의 결과는 `/secret.txt`입니다. 반드시 `resolve()` + `relative_to()` 검증을 함께 사용하세요.

---

## 23.7 민감 정보 관리

비밀번호, API 키, 데이터베이스 자격증명 같은 **민감 정보(Secrets)**를 어떻게 관리하느냐는 보안의 핵심 요소입니다. 가장 흔한 실수는 이런 정보를 소스 코드에 직접 작성하는 것입니다.

### 하드코딩의 위험

**예제 23-05: 환경 변수로 비밀 관리**

```python
# examples/python/chapter05/ex23_05_env_secrets.py

# ❌ 취약: 비밀 정보를 코드에 하드코딩
def vulnerable_database_config() -> dict:
    config = {
        "db_host": "production-db.example.com",
        "db_password": "SuperSecret123!@#",      # ❌ 비밀번호 하드코딩
        "api_key": "sk-1234567890abcdef",         # ❌ API 키 하드코딩
        "jwt_secret": "my-super-secret-jwt-key",  # ❌ JWT 시크릿 하드코딩
    }
    return config
```

이 코드의 문제점은 명확합니다:

1. **Git에 영구 기록**: 한 번 커밋되면 히스토리에서 완전히 삭제하기 매우 어렵습니다
2. **코드 공유 불가**: 소스 코드를 공유하면 비밀도 함께 유출됩니다
3. **환경별 관리 불가**: 개발/스테이징/운영 환경마다 코드를 수정해야 합니다

### 환경 변수 사용

안전한 방법은 **환경 변수**를 사용하는 것입니다:

```python
import os

def get_required_env(key: str) -> str:
    """✅ 필수 환경 변수를 안전하게 가져오기"""
    value = os.environ.get(key)
    if value is None:
        raise EnvironmentError(
            f"필수 환경 변수 '{key}'가 설정되지 않았습니다.\n"
            f"설정 방법: export {key}=값"
        )
    if not value.strip():
        raise EnvironmentError(f"환경 변수 '{key}'가 비어 있습니다.")
    return value

# ✅ 안전: 모든 비밀 정보를 환경 변수에서 가져옴
def safe_database_config() -> dict:
    config = {
        "db_host": get_required_env("DB_HOST"),
        "db_password": get_required_env("DB_PASSWORD"),
        "api_key": get_required_env("API_KEY"),
    }
    return config
```

### 비밀 값 마스킹

로그나 화면에 비밀 정보를 출력할 때는 반드시 **마스킹**해야 합니다:

```python
def mask_secret(value: str) -> str:
    """✅ 비밀 값을 마스킹 (처음 2자만 표시)"""
    if len(value) <= 4:
        return "****"
    return value[:2] + "*" * (len(value) - 2)

# 사용 예:
# mask_secret("SuperSecret123") -> "Su************"
```

### .env 파일 활용

**예제 23-06: .env 파일 사용**

환경 변수를 매번 터미널에서 설정하는 것은 번거롭습니다. `.env` 파일을 사용하면 편리하게 관리할 수 있습니다.

```python
# examples/python/chapter05/ex23_06_dotenv_usage.py

def load_dotenv(filepath: str = ".env", override: bool = False) -> dict:
    """
    ✅ .env 파일을 파싱하여 환경 변수로 설정

    지원하는 형식:
    - KEY=value
    - KEY="quoted value"
    - KEY='single quoted value'
    - # 주석
    - export KEY=value
    """
    env_vars = {}
    env_path = Path(filepath)

    if not env_path.is_file():
        print(f"  경고: .env 파일을 찾을 수 없습니다: {filepath}")
        return env_vars

    with open(env_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:]

            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()

            # 따옴표 제거
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]

            env_vars[key] = value
            if override or key not in os.environ:
                os.environ[key] = value

    return env_vars
```

`.env` 파일 예시:

```bash
# .env (이 파일은 절대 Git에 커밋하지 마세요!)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_dev
DB_USER=dev_user
DB_PASSWORD="my_secret_pass_123"
API_KEY='sk-demo-key-abcdef'
APP_ENV=development
```

### .gitignore 설정

`.env` 파일이 실수로 Git에 커밋되지 않도록 `.gitignore`에 반드시 추가해야 합니다:

```bash
# .gitignore
# 환경 변수 파일 - 절대 커밋하지 마세요!
.env
.env.local
.env.production
.env.*.local

# .env.example은 커밋해도 됩니다 (실제 비밀 없음)
!.env.example
```

> **Warning:** `.env` 파일은 **절대 Git에 커밋하지 마세요!** 대신 `.env.example` 파일을 만들어 필요한 환경 변수의 목록과 형식을 문서화하고, 이 파일만 Git에 커밋하세요.

**실행:**

```bash
$ python examples/python/chapter05/ex23_05_env_secrets.py
```

**결과:**

```
--- ❌ 취약한 코드: 하드코딩된 비밀 ---
  db_password: SuperSecret123!@#
  api_key: sk-1234567890abcdef
  -> 코드에 비밀번호와 API 키가 노출되어 있습니다!

--- ✅ 안전한 코드: 환경 변수 사용 ---
  DB_PASSWORD: de**************
  API_KEY: sk****************
  -> 비밀 값이 마스킹되어 안전합니다!
```

---

## 23.8 해시와 암호화 기초

비밀번호를 안전하게 저장하고, 데이터의 무결성을 검증하고, 안전한 토큰을 생성하려면 **해시(Hash)**와 **암호화(Cryptography)**의 기본 개념을 이해해야 합니다.

### 해시 함수란?

해시 함수는 입력 데이터를 고정된 길이의 문자열(해시값)로 변환하는 단방향 함수입니다. 같은 입력은 항상 같은 해시값을 생성하지만, 해시값에서 원래 데이터를 역추적하는 것은 사실상 불가능합니다.

### 취약한 비밀번호 저장 vs 안전한 비밀번호 저장

**예제 23-07: 해시와 암호화 기초**

```python
# examples/python/chapter05/ex23_07_hash_crypto.py

import hashlib
import secrets
import hmac

# ❌ 취약: MD5로 비밀번호 해싱 (솔트 없음)
def vulnerable_store_password(password: str) -> str:
    # MD5는 암호학적으로 깨진 해시 함수
    # 솔트 없이 동일 비밀번호 = 동일 해시 (레인보우 테이블 공격 가능)
    return hashlib.md5(password.encode()).hexdigest()

# ✅ 최선: PBKDF2로 비밀번호 해싱 (권장)
def best_hash_password(password: str) -> str:
    # 안전한 랜덤 솔트 생성
    salt = secrets.token_bytes(32)
    # PBKDF2-HMAC-SHA256, 반복 600,000회
    iterations = 600_000
    dk = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt, iterations
    )
    # 저장 형식: 알고리즘$반복횟수$솔트(hex)$해시(hex)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"

# ✅ PBKDF2 해시 비밀번호 검증
def best_verify_password(password: str, stored: str) -> bool:
    parts = stored.split("$")
    if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
        return False
    iterations = int(parts[1])
    salt = bytes.fromhex(parts[2])
    stored_hash = parts[3]
    dk = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt, iterations
    )
    # ✅ 상수 시간 비교 (타이밍 공격 방지)
    return hmac.compare_digest(dk.hex(), stored_hash)
```

#### MD5가 위험한 이유

| 문제 | 설명 |
|------|------|
| **암호학적으로 깨진 해시** | 충돌 공격이 실질적으로 가능 |
| **너무 빠름** | GPU로 초당 수십억 개의 해시를 계산 가능 |
| **솔트 없음** | 동일 비밀번호 = 동일 해시 (레인보우 테이블) |

#### PBKDF2가 안전한 이유

| 특징 | 설명 |
|------|------|
| **솔트(Salt)** | 각 비밀번호에 고유한 랜덤 값을 추가 |
| **반복 연산** | 60만 회 반복으로 무차별 대입 공격 속도를 늦춤 |
| **SHA-256** | 안전한 해시 알고리즘 사용 |
| **상수 시간 비교** | `hmac.compare_digest()`로 타이밍 공격 방지 |

### 안전한 토큰 생성

보안 토큰(세션 ID, API 키 등)을 생성할 때는 `random` 모듈이 아닌 `secrets` 모듈을 사용해야 합니다:

```python
import secrets

# ✅ 안전한 토큰 생성
hex_token = secrets.token_hex(32)         # 16진수 문자열
url_token = secrets.token_urlsafe(32)     # URL-safe 문자열
api_key = f"sk-{secrets.token_hex(24)}"   # API 키 형식
```

> **Warning:** `random` 모듈은 예측 가능한 의사 난수 생성기입니다. 보안 목적(토큰, 키, 비밀번호 등)에는 **절대 사용하지 마세요**. 반드시 `secrets` 모듈을 사용하세요.

### HMAC으로 데이터 무결성 검증

HMAC(Hash-based Message Authentication Code)은 메시지가 변조되지 않았음을 검증하는 데 사용됩니다:

```python
def create_signed_message(message: str, secret_key: str) -> str:
    """✅ HMAC으로 메시지에 서명"""
    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"{message}|{signature}"

def verify_signed_message(signed_message: str, secret_key: str) -> tuple:
    """✅ HMAC 서명 검증"""
    message, received_sig = signed_message.rsplit("|", 1)
    expected_sig = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    # ✅ 상수 시간 비교
    is_valid = hmac.compare_digest(expected_sig, received_sig)
    return is_valid, message
```

**실행:**

```bash
$ python examples/python/chapter05/ex23_07_hash_crypto.py
```

**결과:**

```
--- ❌ 취약한 코드: MD5 + 솔트 없음 ---
  비밀번호: MyP@ssw0rd123!
  MD5 해시: a1b2c3d4e5f6...
  같은 비밀번호 재해싱: a1b2c3d4e5f6...
  동일 여부: True (항상 같음 = 레인보우 테이블에 취약!)

--- ✅ 최선: PBKDF2-HMAC-SHA256 (권장) ---
  비밀번호 해싱 중... (반복 600,000회)
  해싱 시간: 0.287초 (느릴수록 무차별 대입에 강함)
  올바른 비밀번호 검증: True
  틀린 비밀번호 검증: False

--- ✅ HMAC 메시지 서명/검증 ---
  정상 검증: 유효=True
  변조 검증: 유효=False (변조 감지!)
  잘못된 키: 유효=False (위조 감지!)
```

### 해시 알고리즘 비교표

| 알고리즘 | 비트 수 | 보안 상태 | 용도 |
|---------|---------|----------|------|
| MD5 | 128 | 취약 | 사용 금지 (파일 체크섬 외) |
| SHA-1 | 160 | 취약 | 사용 금지 |
| SHA-256 | 256 | 안전 | 데이터 무결성, 일반 해싱 |
| SHA-512 | 512 | 안전 | 높은 보안이 필요한 경우 |
| PBKDF2 | 가변 | 안전 | 비밀번호 해싱 (권장) |

---

## 23.9 AI 생성 코드의 보안 검토

바이브 코딩에서 가장 중요한 보안 습관은 **AI가 생성한 코드를 보안 관점에서 검토하는 것**입니다. AI는 뛰어난 코드 생성 능력을 가지고 있지만, 보안을 항상 최우선으로 고려하지는 않습니다.

### 보안 체크리스트 자동화

**예제 23-08: AI에게 보안 검토 요청 - 보안 체크리스트 자동화**

다음은 Python 소스 코드의 보안 취약점을 자동으로 검사하는 도구입니다:

```python
# examples/python/chapter05/ex23_08_security_review.py

class SecurityChecker:
    """
    ✅ Python 소스 코드의 보안 취약점을 검사하는 도구

    검사 항목:
    1. 하드코딩된 비밀 정보
    2. 안전하지 않은 함수 사용 (eval, exec)
    3. SQL 인젝션 위험
    4. 명령어 인젝션 위험
    5. 안전하지 않은 역직렬화 (pickle)
    6. 디버그 모드 설정
    7. 취약한 암호화 (MD5, SHA-1)
    8. 안전하지 않은 난수 생성
    """

    def check_source(self, source_code: str, filename: str = "<code>") -> list:
        """소스 코드를 검사하고 발견 사항을 반환"""
        self.findings = []
        lines = source_code.split('\n')

        self._check_hardcoded_secrets(lines, filename)
        self._check_unsafe_functions(lines, filename)
        self._check_sql_injection(lines, filename)
        self._check_command_injection(lines, filename)
        self._check_unsafe_deserialization(lines, filename)
        self._check_debug_settings(lines, filename)
        self._check_weak_crypto(lines, filename)
        self._check_insecure_random(lines, filename)

        return self.findings
```

이 도구는 소스 코드를 줄 단위로 분석하여 알려진 취약 패턴을 탐지합니다. 예를 들어 `f"SELECT * FROM users WHERE name = '{user_input}'"` 같은 패턴을 발견하면 SQL 인젝션 위험으로 보고합니다.

**실행:**

```bash
$ python examples/python/chapter05/ex23_08_security_review.py
```

**결과:**

```
보안 검사 결과: 12개 문제 발견
==================================================

[HIGH] 높음 (즉시 수정 필요) - 7건
----------------------------------------
  1. [비밀 정보 하드코딩] 하드코딩된 비밀번호
     파일: vulnerable_app.py:8
     코드: DB_PASSWORD = "SuperSecret123"
     권장: 환경 변수(os.environ)를 사용하세요

  2. [SQL 인젝션] SQL 쿼리에 문자열 포맷팅 사용
     파일: vulnerable_app.py:17
     권장: 파라미터화 쿼리(?)를 사용하세요
  ...

[MEDIUM] 중간 (수정 권장) - 5건
----------------------------------------
  1. [안전하지 않은 함수] eval() 사용
     권장: ast.literal_eval()을 사용하거나 eval()을 제거하세요
  ...
```

### AI에게 보안 검토 요청하는 프롬프트

AI에게 보안 검토를 요청할 때는 **구체적인 항목을 명시**하는 것이 효과적입니다:

```
다음 Python 코드의 보안을 검토해주세요.

검토 항목:
1. 입력 검증: 모든 외부 입력이 적절히 검증되는지
2. SQL 인젝션: 파라미터화 쿼리를 사용하는지
3. 명령어 인젝션: subprocess가 안전하게 사용되는지
4. 경로 순회: 파일 경로가 안전하게 처리되는지
5. 비밀 관리: 하드코딩된 비밀 정보가 없는지
6. 암호화: 안전한 해시/암호화 알고리즘을 사용하는지
7. 인증/권한: 적절한 접근 제어가 있는지
8. 에러 처리: 민감한 정보가 에러 메시지에 노출되지 않는지
9. 로깅: 비밀 정보가 로그에 기록되지 않는지
10. 의존성: 알려진 취약점이 있는 라이브러리를 사용하지 않는지

각 문제에 대해 위치, 위험 수준, 문제 설명, 수정 방법(코드 포함)을 제공해주세요.
```

> **Tip:** 바이브 코딩에서 AI에게 **"이 코드의 보안 취약점을 찾아서 수정 방법과 함께 알려줘"** 라고 요청하면 체계적인 보안 검토 결과를 받을 수 있습니다. 항상 생성된 코드를 검토하는 습관을 들이세요.

---

## 23.10 실습: 취약한 코드 찾기

지금까지 배운 내용을 종합하여, 여러 보안 취약점이 있는 코드를 분석하고 수정하는 실습을 해봅시다.

**예제 23-09: 실습 - 취약한 코드 찾기**

```python
# examples/python/chapter05/ex23_09_find_vulnerabilities.py

class VulnerableApp:
    """
    ❌ 이 클래스에는 최소 8개의 보안 취약점이 있습니다.
    모두 찾을 수 있나요?
    """
    # 취약점 1: 하드코딩된 비밀 정보
    SECRET_KEY = "my-super-secret-key-12345"
    DB_PASSWORD = "admin123"

    def register(self, username, password, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # 취약점 2: MD5로 비밀번호 해싱 (솔트 없음)
        password_hash = hashlib.md5(password.encode()).hexdigest()
        # 취약점 3: SQL 인젝션
        cursor.execute(
            f"INSERT INTO users (username, password, email) "
            f"VALUES ('{username}', '{password_hash}', '{email}')"
        )
        # 취약점 4: 상세한 에러 메시지 노출
        # 취약점 5: 예측 가능한 토큰 (random 모듈)
        # 취약점 6: 경로 순회 방지 없음
        # 취약점 7: 명령어 인젝션 (shell=True)
        # 취약점 8: 입력 검증 부재
```

### 취약점 대조표

아래는 8가지 취약점과 그 수정 방법을 정리한 표입니다:

| # | 취약점 | 취약한 코드 | 안전한 코드 |
|---|--------|------------|------------|
| 1 | **하드코딩된 비밀** | `SECRET_KEY = "my-super-..."` | `os.environ.get("APP_SECRET_KEY")` |
| 2 | **약한 해시** | `hashlib.md5(password...)` | `hashlib.pbkdf2_hmac('sha256', ...)` |
| 3 | **SQL 인젝션** | `f"SELECT ... '{username}'"` | `cursor.execute("SELECT ... ?", (username,))` |
| 4 | **에러 노출** | `{"detail": str(e), "query": ...}` | `{"message": "등록에 실패했습니다"}` |
| 5 | **예측 가능 토큰** | `random.choice(...)` | `secrets.token_urlsafe(32)` |
| 6 | **경로 순회** | `f"/tmp/{username}/{filename}"` | `path.relative_to(allowed_dir)` |
| 7 | **명령어 인젝션** | `shell=True` + f-string | `["find", dir, "-name", pattern]` |
| 8 | **입력 검증 부재** | 검증 없이 DB에 저장 | 정규식으로 형식/길이 검증 |

**실행:**

```bash
$ python examples/python/chapter05/ex23_09_find_vulnerabilities.py
```

**결과:**

```
--- ❌ 취약한 앱(VulnerableApp) 시연 ---

[2] ❌ SQL 인젝션 공격:
  결과: {'status': 'success', 'username': "evil','hack','evil@x.com','admin')--"}

[4] ❌ 경로 순회 공격:
  결과: (시스템 파일 내용 노출!)

--- ✅ 안전한 앱(SecureApp) 시연 ---

[2] ✅ 약한 비밀번호 거부:
  결과: {'status': 'error', 'message': '비밀번호는 최소 8자 이상이어야 합니다'}

[4] ✅ SQL 인젝션 차단:
  결과: {'status': 'error', 'message': '사용자 이름은 영문, 숫자, 밑줄만 가능합니다'}

[7] ✅ 경로 순회 차단:
  결과: 접근 거부: 허용되지 않은 경로입니다

[8] ✅ 명령어 인젝션 차단:
  결과: 검색 패턴에 허용되지 않은 문자가 포함되어 있습니다
```

> **Note:** 이 실습은 실제 보안 감사(Security Audit)의 축소판입니다. 실제 프로젝트에서도 동일한 방법론으로 코드를 검토할 수 있습니다. 취약한 코드와 안전한 코드를 비교하면서 각 수정이 어떤 공격을 방지하는지 이해하는 것이 중요합니다.

---

## 23.11 바이브 코딩 보안 체크리스트

AI와 함께 코드를 작성한 후, 다음 체크리스트를 사용하여 보안을 검토하세요:

### 코드 작성 시 체크리스트

```
[ ] 모든 외부 입력(사용자, API, 파일)을 검증하는가?
[ ] SQL 쿼리에 파라미터화 쿼리(?)를 사용하는가?
[ ] subprocess에서 shell=False와 리스트 인자를 사용하는가?
[ ] 파일 경로에 경로 순회 방지가 적용되어 있는가?
[ ] 비밀 정보가 코드에 하드코딩되어 있지 않은가?
[ ] 비밀번호는 PBKDF2(또는 bcrypt/scrypt)로 해싱하는가?
[ ] 보안 토큰은 secrets 모듈로 생성하는가?
[ ] 에러 메시지에 내부 정보가 노출되지 않는가?
[ ] 로그에 비밀 정보(비밀번호, API 키)가 기록되지 않는가?
[ ] .env 파일이 .gitignore에 추가되어 있는가?
```

### AI에게 코드를 요청할 때 추가할 프롬프트

| 상황 | 추가할 프롬프트 |
|------|---------------|
| 데이터베이스 코드 | "파라미터화 쿼리를 사용해줘" |
| 사용자 입력 처리 | "입력 검증을 포함해줘" |
| 파일 처리 | "경로 순회 방지 코드를 추가해줘" |
| 비밀번호 관리 | "PBKDF2로 안전하게 해싱해줘" |
| 외부 명령 실행 | "shell=True를 제거하고 안전하게 바꿔줘" |
| 설정 관리 | "하드코딩 대신 환경 변수를 사용해줘" |
| 전체 보안 검토 | "이 코드의 보안 취약점을 찾아서 수정해줘" |

---

## 정리

이 장에서 배운 핵심 내용을 정리합니다:

### 보안의 기본 원칙

1. **모든 외부 입력은 신뢰하지 않는다** -- 반드시 검증한 후 사용합니다
2. **보안은 처음부터 고려한다** -- "나중에 추가하겠다"는 위험한 생각입니다
3. **심층 방어를 적용한다** -- 한 가지 보안 장치에만 의존하지 않습니다
4. **최소 권한 원칙을 따른다** -- 필요한 최소한의 권한만 부여합니다

### 주요 취약점과 방지법

| 취약점 | 방지법 | 핵심 코드 |
|--------|--------|----------|
| **입력 검증 부재** | 타입, 길이, 형식, 범위 검증 | `re.match()`, `isinstance()` |
| **SQL 인젝션** | 파라미터화 쿼리 | `cursor.execute("... ?", (value,))` |
| **명령어 인젝션** | 리스트 인자 + shell=False | `subprocess.run(["cmd", arg])` |
| **경로 순회** | resolve() + relative_to() | `path.relative_to(allowed_dir)` |
| **비밀 노출** | 환경 변수 + .env | `os.environ.get("SECRET")` |
| **약한 해시** | PBKDF2 + 솔트 | `hashlib.pbkdf2_hmac()` |
| **예측 가능 토큰** | secrets 모듈 | `secrets.token_urlsafe()` |

### 바이브 코딩에서의 보안

AI가 생성한 코드는 반드시 보안 관점에서 검토해야 합니다. AI에게 코드를 요청할 때 보안 요구사항을 명시적으로 전달하고, 생성된 코드에 대해 보안 체크리스트를 적용하는 습관을 들이세요.

---

## 다음 장 미리보기

다음 Chapter 24에서는 **코드 품질과 유지보수**를 다룹니다. 프롬프트 템플릿, 코드 리뷰 체크리스트, 자동 포맷팅, 린터 활용, 독스트링 작성 등 코드의 품질을 높이고 장기적으로 유지보수하기 쉬운 코드를 만드는 방법을 배웁니다. 보안이 코드의 "안전성"을 다루었다면, 다음 장은 코드의 "건강함"을 다룹니다.

---

## 연습 문제

### 연습 1: 입력 검증 함수 작성

다음 조건을 만족하는 `validate_phone_number()` 함수를 작성하세요:
- 한국 전화번호 형식: `010-XXXX-XXXX`
- 숫자와 하이픈만 허용
- 총 길이 13자

```python
def validate_phone_number(phone: str) -> str:
    """
    전화번호 검증
    올바른 형식: 010-1234-5678
    """
    # 여기에 검증 코드를 작성하세요
    pass
```

> **Tip:** AI에게 "한국 전화번호를 검증하는 함수를 만들어줘. 정규식을 사용하고, ValidationError를 발생시켜줘" 라고 요청해보세요.

### 연습 2: SQL 인젝션 수정

다음 취약한 코드를 파라미터화 쿼리로 수정하세요:

```python
# ❌ 취약한 코드
def search_products(category: str, min_price: str):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM products WHERE category = '{category}' AND price >= {min_price}"
    cursor.execute(query)
    return cursor.fetchall()
```

### 연습 3: 환경 변수 마이그레이션

다음 코드에서 하드코딩된 비밀 정보를 환경 변수로 변경하세요:

```python
# ❌ 수정 전
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "myapp@gmail.com"
SMTP_PASSWORD = "my_email_password_123"
API_KEY = "sk-abcdef1234567890"
```

### 연습 4: 보안 검토 실습

AI에게 간단한 사용자 관리 코드를 생성하도록 요청한 후, 이 장에서 배운 보안 체크리스트를 적용하여 취약점을 찾고 수정해보세요:

1. AI에게 "사용자 등록과 로그인 기능을 만들어줘"라고 요청합니다
2. 생성된 코드에서 보안 취약점을 찾습니다
3. AI에게 "이 코드의 보안 취약점을 찾아서 수정해줘"라고 요청합니다
4. 수정된 코드가 이 장의 원칙을 따르는지 확인합니다

### 연습 5: 종합 실습 -- 안전한 미니 앱

이 장에서 배운 모든 보안 원칙을 적용하여 다음 기능을 가진 안전한 메모 앱을 만들어보세요:

- 사용자 등록/로그인 (안전한 비밀번호 해싱)
- 메모 저장/읽기 (파라미터화 쿼리)
- 파일 첨부 (경로 순회 방지)
- 설정 관리 (환경 변수 사용)

> **Tip:** AI에게 "보안을 최우선으로 고려하는 메모 앱을 만들어줘. OWASP Top 10을 모두 방어하는 코드를 작성해줘" 라고 요청해보세요. 그런 다음 생성된 코드를 이 장의 체크리스트로 검토하세요.
