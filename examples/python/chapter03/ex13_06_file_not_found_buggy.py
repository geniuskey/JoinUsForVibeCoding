"""
예제 13-6: FileNotFoundError — 잘못된 파일 경로
=================================================
흔한 오류: 존재하지 않는 파일을 열려고 시도
"""

# 버그가 있는 코드: 존재하지 않는 파일 열기
filename = "학생명단.txt"

# 파일이 존재하지 않으면 FileNotFoundError 발생
file = open(filename, "r", encoding="utf-8")
content = file.read()
print(f"파일 내용:\n{content}")
file.close()
