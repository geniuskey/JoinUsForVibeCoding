"""
예제 10-3: 나쁜 프롬프트 vs 좋은 프롬프트 — API 설계
====================================================
나쁜 프롬프트: "API 만들어"
좋은 프롬프트: "사용자 관리 REST API의 엔드포인트 목록을 설계해줘.
              각 엔드포인트에 HTTP 메서드, 경로, 요청/응답 형식,
              상태 코드를 포함해줘. 표 형식으로 정리해줘."
"""


# --- 나쁜 프롬프트로 생성된 코드 ---
# 프롬프트: "API 만들어"

def bad_api():
    """모호한 요청의 결과: 최소한의 스켈레톤"""
    endpoints = ["/api/data"]
    return endpoints


# --- 좋은 프롬프트로 생성된 코드 ---
# 프롬프트: "사용자 관리 REST API의 엔드포인트 목록을 설계해줘.
#           각 엔드포인트에 HTTP 메서드, 경로, 설명, 요청 본문,
#           성공 응답 코드를 포함해줘. 딕셔너리 리스트로 반환해줘."

def design_user_api():
    """
    사용자 관리 REST API 스펙을 반환합니다.

    Returns:
        list[dict]: 엔드포인트 명세 목록
    """
    endpoints = [
        {
            "method": "GET",
            "path": "/api/users",
            "description": "전체 사용자 목록 조회",
            "request_body": None,
            "success_code": 200,
            "response_example": '[{"id":1,"name":"김코딩","email":"kim@example.com"}]',
        },
        {
            "method": "GET",
            "path": "/api/users/{id}",
            "description": "특정 사용자 조회",
            "request_body": None,
            "success_code": 200,
            "response_example": '{"id":1,"name":"김코딩","email":"kim@example.com"}',
        },
        {
            "method": "POST",
            "path": "/api/users",
            "description": "새 사용자 생성",
            "request_body": '{"name":"...","email":"...","password":"..."}',
            "success_code": 201,
            "response_example": '{"id":2,"name":"이바이브","email":"lee@example.com"}',
        },
        {
            "method": "PUT",
            "path": "/api/users/{id}",
            "description": "사용자 정보 수정",
            "request_body": '{"name":"...","email":"..."}',
            "success_code": 200,
            "response_example": '{"id":1,"name":"김수정","email":"kim2@example.com"}',
        },
        {
            "method": "DELETE",
            "path": "/api/users/{id}",
            "description": "사용자 삭제",
            "request_body": None,
            "success_code": 204,
            "response_example": "(본문 없음)",
        },
    ]
    return endpoints


def print_api_spec(endpoints):
    """API 스펙을 보기 좋게 출력합니다."""
    header = f"{'메서드':<8} {'경로':<22} {'설명':<20} {'코드':<6}"
    print(header)
    print("-" * len(header))
    for ep in endpoints:
        print(f"{ep['method']:<8} {ep['path']:<22} "
              f"{ep['description']:<20} {ep['success_code']:<6}")

    print()
    print("[상세 스펙]")
    for ep in endpoints:
        print(f"\n  {ep['method']} {ep['path']}")
        print(f"    설명     : {ep['description']}")
        if ep["request_body"]:
            print(f"    요청 본문: {ep['request_body']}")
        print(f"    응답({ep['success_code']}): {ep['response_example']}")


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 60)
    print("[나쁜 프롬프트 결과]")
    result = bad_api()
    print(f"  엔드포인트: {result}")
    print("  → 어떤 리소스? 어떤 메서드? 어떤 응답? 전혀 알 수 없음\n")

    print("=" * 60)
    print("[좋은 프롬프트 결과]")
    spec = design_user_api()
    print_api_spec(spec)
