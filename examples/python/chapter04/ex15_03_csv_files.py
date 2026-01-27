"""
예제 15-03: CSV 파일 읽기/쓰기
csv 모듈을 사용하여 CSV 파일을 다루는 방법을 배웁니다.
"""
import csv
import tempfile
import os

temp_dir = tempfile.mkdtemp()

# --- CSV 파일 쓰기 ---
print("=" * 50)
print("1단계: CSV 파일 쓰기")
print("=" * 50)
csv_path = os.path.join(temp_dir, "students.csv")

students = [
    ["이름", "나이", "점수", "학과"],
    ["김민수", 22, 95, "컴퓨터공학"],
    ["이서연", 21, 88, "디자인"],
    ["박지훈", 23, 92, "경영학"],
    ["최예진", 20, 97, "수학"],
    ["정도현", 22, 85, "물리학"],
]

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(students)

print(f"CSV 파일이 생성되었습니다: students.csv")
print(f"총 {len(students) - 1}명의 학생 데이터를 저장했습니다.")

# --- CSV 파일 읽기 ---
print()
print("=" * 50)
print("2단계: CSV 파일 읽기 (csv.reader)")
print("=" * 50)
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            print(f"  헤더: {row}")
        else:
            print(f"  데이터: {row}")

# --- DictReader로 읽기 ---
print()
print("=" * 50)
print("3단계: DictReader로 읽기 (딕셔너리 형태)")
print("=" * 50)
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['이름']}님 - 나이: {row['나이']}, 점수: {row['점수']}, 학과: {row['학과']}")

# --- DictWriter로 쓰기 ---
print()
print("=" * 50)
print("4단계: DictWriter로 쓰기 (딕셔너리 형태)")
print("=" * 50)
csv_path2 = os.path.join(temp_dir, "products.csv")

products = [
    {"상품명": "노트북", "가격": 1200000, "재고": 15},
    {"상품명": "마우스", "가격": 35000, "재고": 120},
    {"상품명": "키보드", "가격": 89000, "재고": 75},
    {"상품명": "모니터", "가격": 450000, "재고": 30},
]

fieldnames = ["상품명", "가격", "재고"]
with open(csv_path2, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products)

print("products.csv 파일이 생성되었습니다.")

# 검증: 읽어서 출력
with open(csv_path2, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = int(row["가격"])
        print(f"  {row['상품명']:>5s} | {price:>10,}원 | 재고: {row['재고']}개")

# --- 통계 계산 ---
print()
print("=" * 50)
print("5단계: CSV 데이터 통계 계산")
print("=" * 50)
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    scores = []
    for row in reader:
        scores.append(int(row["점수"]))

print(f"  학생 수: {len(scores)}명")
print(f"  평균 점수: {sum(scores) / len(scores):.1f}")
print(f"  최고 점수: {max(scores)}")
print(f"  최저 점수: {min(scores)}")

# 정리
os.remove(csv_path)
os.remove(csv_path2)
os.rmdir(temp_dir)
print()
print("CSV 파일 처리 예제를 성공적으로 완료했습니다!")
