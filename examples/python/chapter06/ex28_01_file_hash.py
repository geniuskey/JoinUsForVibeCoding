"""
예제 28-1: 파일 해시 비교
- hashlib을 사용하여 MD5 및 SHA256 해시를 계산합니다.
- 두 파일의 해시를 비교하여 동일 여부를 판단합니다.
- 파일 동기화 도구의 핵심 기반: 파일 변경 감지에 활용됩니다.
"""

import hashlib
import os
import tempfile


def calculate_hash(file_path: str, algorithm: str = "sha256", chunk_size: int = 8192) -> str:
    """
    파일의 해시값을 계산합니다.

    Args:
        file_path: 해시를 계산할 파일 경로
        algorithm: 해시 알고리즘 ("md5" 또는 "sha256")
        chunk_size: 한 번에 읽을 바이트 수 (대용량 파일 대응)

    Returns:
        16진수 해시 문자열
    """
    # 지원하는 알고리즘 선택
    if algorithm == "md5":
        hasher = hashlib.md5()
    elif algorithm == "sha256":
        hasher = hashlib.sha256()
    else:
        raise ValueError(f"지원하지 않는 알고리즘: {algorithm}")

    # 파일을 청크 단위로 읽으며 해시 업데이트
    # 대용량 파일도 메모리 부담 없이 처리 가능
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()


def compare_files_by_hash(file1: str, file2: str, algorithm: str = "sha256") -> bool:
    """
    두 파일의 해시를 비교하여 동일 여부를 판단합니다.

    Args:
        file1: 첫 번째 파일 경로
        file2: 두 번째 파일 경로
        algorithm: 사용할 해시 알고리즘

    Returns:
        두 파일이 동일하면 True, 다르면 False
    """
    hash1 = calculate_hash(file1, algorithm)
    hash2 = calculate_hash(file2, algorithm)
    return hash1 == hash2


def get_directory_hashes(directory: str, algorithm: str = "sha256") -> dict:
    """
    디렉토리 내 모든 파일의 해시를 계산하여 딕셔너리로 반환합니다.

    Args:
        directory: 스캔할 디렉토리 경로
        algorithm: 해시 알고리즘

    Returns:
        {상대경로: 해시값} 형태의 딕셔너리
    """
    hashes = {}

    for root, _dirs, files in os.walk(directory):
        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            # 디렉토리 기준 상대 경로를 키로 사용
            relative_path = os.path.relpath(filepath, directory)
            hashes[relative_path] = calculate_hash(filepath, algorithm)

    return hashes


if __name__ == "__main__":
    print("=" * 60)
    print("  파일 해시 비교 도구 데모")
    print("=" * 60)

    # 임시 디렉토리에 테스트 파일 생성
    demo_dir = tempfile.mkdtemp(prefix="hash_demo_", dir="/tmp")
    print(f"\n[준비] 데모 디렉토리: {demo_dir}")

    # 테스트 파일 3개 생성
    file_a = os.path.join(demo_dir, "파일A.txt")
    file_b = os.path.join(demo_dir, "파일B.txt")
    file_c = os.path.join(demo_dir, "파일C.txt")

    with open(file_a, "w", encoding="utf-8") as f:
        f.write("안녕하세요, 바이브 코딩!\n동기화 테스트 파일입니다.\n")

    with open(file_b, "w", encoding="utf-8") as f:
        f.write("안녕하세요, 바이브 코딩!\n동기화 테스트 파일입니다.\n")

    with open(file_c, "w", encoding="utf-8") as f:
        f.write("이 파일은 내용이 다릅니다.\n")

    # --- 1. 개별 파일 해시 계산 ---
    print("\n--- 1. 개별 파일 해시 계산 ---")

    for name, path in [("파일A", file_a), ("파일B", file_b), ("파일C", file_c)]:
        md5 = calculate_hash(path, "md5")
        sha256 = calculate_hash(path, "sha256")
        print(f"\n  [{name}] {os.path.basename(path)}")
        print(f"    MD5   : {md5}")
        print(f"    SHA256: {sha256}")

    # --- 2. 파일 비교 ---
    print("\n--- 2. 파일 해시 비교 ---")

    result_ab = compare_files_by_hash(file_a, file_b)
    print(f"\n  파일A vs 파일B (동일 내용): {'동일함' if result_ab else '다름'}")

    result_ac = compare_files_by_hash(file_a, file_c)
    print(f"  파일A vs 파일C (다른 내용): {'동일함' if result_ac else '다름'}")

    # --- 3. 디렉토리 전체 해시 ---
    print("\n--- 3. 디렉토리 전체 파일 해시 ---")

    # 하위 디렉토리도 포함하는 테스트
    sub_dir = os.path.join(demo_dir, "하위폴더")
    os.makedirs(sub_dir)
    sub_file = os.path.join(sub_dir, "설정.txt")
    with open(sub_file, "w", encoding="utf-8") as f:
        f.write("설정 파일 내용\n")

    dir_hashes = get_directory_hashes(demo_dir)
    print(f"\n  디렉토리: {demo_dir}")
    print(f"  총 파일 수: {len(dir_hashes)}개\n")

    for rel_path, hash_value in dir_hashes.items():
        print(f"    {rel_path}")
        print(f"      SHA256: {hash_value[:32]}...")

    # --- 4. MD5 vs SHA256 속도 비교 ---
    print("\n--- 4. 알고리즘별 해시값 길이 비교 ---")

    md5_hash = calculate_hash(file_a, "md5")
    sha256_hash = calculate_hash(file_a, "sha256")
    print(f"\n  MD5    ({len(md5_hash)}자): {md5_hash}")
    print(f"  SHA256 ({len(sha256_hash)}자): {sha256_hash}")
    print(f"\n  * SHA256이 더 길고 안전하지만, 단순 변경 감지에는 MD5도 충분합니다.")

    # 정리
    import shutil
    shutil.rmtree(demo_dir)
    print(f"\n[정리] 데모 디렉토리 삭제 완료")
    print("\n" + "=" * 60)
