# Chapter 28: 프로젝트 4 - 파일 동기화 도구

두 폴더의 파일을 비교하고, 변경된 것만 골라서 자동으로 맞춰주는 도구가 있다면 얼마나 편리할까요? USB에 백업하거나, 작업 폴더와 공유 폴더를 일치시키거나, 여러 장치 간에 파일을 동기화하는 상황은 누구에게나 익숙합니다. 이 장에서는 파이썬 표준 라이브러리만으로 **파일 동기화 도구**를 단계별로 만들어 봅니다. 파일 해시 비교, 변경 감지, 동기화 실행, 충돌 처리, 로깅, CLI 인터페이스까지 -- 실무에서 바로 쓸 수 있는 완성형 도구를 AI와 함께 바이브 코딩으로 완성합니다.

---

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- `hashlib`을 사용하여 파일의 **해시값**을 계산하고 비교할 수 있다
- 두 디렉토리를 스캔하여 **추가/수정/삭제된 파일**을 자동으로 감지할 수 있다
- 소스 디렉토리를 기준으로 대상 디렉토리를 **단방향 동기화**할 수 있다
- 양방향 동기화 시 발생하는 **충돌을 감지하고 해결**할 수 있다
- `logging` 모듈로 동기화 작업을 **체계적으로 기록**할 수 있다
- `argparse`로 **CLI 인터페이스**를 만들어 터미널에서 도구를 사용할 수 있다
- AI에게 점진적으로 요구사항을 전달하며 **프로젝트를 확장**하는 경험을 쌓을 수 있다

---

## 28.1 프로젝트 개요

### 무엇을 만드는가?

두 디렉토리 사이의 파일을 비교하고 동기화하는 명령줄 도구를 만듭니다. 핵심 기능은 다음과 같습니다:

| 기능 | 설명 |
|------|------|
| **파일 해시 비교** | SHA256 해시로 파일 내용의 동일 여부를 정확히 판단 |
| **변경 감지** | 추가, 수정, 삭제된 파일을 자동으로 분류 |
| **단방향 동기화** | 소스 디렉토리 기준으로 대상 디렉토리를 맞춤 |
| **충돌 처리** | 양쪽 모두 변경된 파일에 대한 해결 전략 제공 |
| **로그 기록** | 모든 동기화 작업을 콘솔과 파일에 기록 |
| **CLI 인터페이스** | 터미널에서 scan, compare, sync 명령으로 사용 |

### 사용하는 표준 라이브러리

이 프로젝트는 외부 패키지 없이 파이썬 표준 라이브러리만 사용합니다:

```
hashlib   - 파일 해시 계산 (SHA256, MD5)
os        - 파일/디렉토리 경로 처리
shutil    - 파일 복사 및 삭제
pathlib   - 현대적인 경로 처리
argparse  - 명령줄 인자 파싱
logging   - 로그 기록
json      - 설정/보고서 직렬화
dataclasses - 데이터 구조 정의
```

### 개발 순서

프로젝트를 6단계로 나누어 점진적으로 기능을 추가합니다. 각 단계에서 AI에게 구체적인 프롬프트를 작성하여 코드를 생성합니다.

```
단계 1: 파일 해시 비교      → 기반 기술 확보
단계 2: 변경 파일 감지      → 비교 로직 구현
단계 3: 동기화 로직         → 핵심 기능 구현
단계 4: 충돌 처리           → 고급 기능 추가
단계 5: 로그 기록           → 운영 품질 향상
단계 6: CLI 인터페이스      → 사용자 인터페이스 완성
```

> **Tip:** 바이브 코딩에서 프로젝트를 진행할 때는 한번에 모든 것을 요청하지 마세요. 이처럼 단계를 나누고, 각 단계의 결과를 확인한 뒤 다음 단계를 요청하는 것이 훨씬 좋은 결과를 가져옵니다. 이를 **반복적(iterative) 개발**이라고 합니다.

---

## 28.2 단계 1: 파일 해시 비교

### AI에게 보내는 프롬프트

```
파일 동기화 도구를 만들고 싶어. 첫 번째 단계로 파일의 해시값을
계산하고 비교하는 기능이 필요해.

요구사항:
1. hashlib으로 MD5와 SHA256 해시를 계산하는 함수
2. 대용량 파일도 메모리 부담 없이 처리 (청크 단위 읽기)
3. 두 파일의 해시를 비교하여 동일 여부를 판단하는 함수
4. 디렉토리 내 모든 파일의 해시를 한번에 계산하는 함수
5. 파이썬 표준 라이브러리만 사용해줘
```

### 핵심 개념: 파일 해시란?

파일의 해시(hash)란 파일 내용을 고정 길이의 문자열로 변환한 "지문"과 같습니다. 파일 내용이 1바이트라도 다르면 완전히 다른 해시값이 나옵니다. 이 특성 덕분에 두 파일의 내용이 같은지 빠르게 판단할 수 있습니다.

```
파일 내용: "안녕하세요"  →  SHA256: a1b2c3d4e5...  (64자)
파일 내용: "안녕하세요!" →  SHA256: f6g7h8i9j0...  (64자, 완전히 다름!)
```

### 예제 코드

**예제 28-1: 파일 해시 비교**

```python
# examples/python/chapter06/ex28_01_file_hash.py
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
```

이 코드에서 주목해야 할 핵심 포인트를 살펴보겠습니다:

1. **청크 단위 읽기**: `f.read(chunk_size)`로 파일을 조각내어 읽습니다. 수 GB짜리 파일도 8KB씩 읽으므로 메모리 걱정이 없습니다.
2. **바이너리 모드**: `"rb"`로 파일을 열어야 합니다. 해시는 바이트 단위로 계산하기 때문입니다.
3. **상대 경로 키**: `os.path.relpath()`로 디렉토리 기준 상대 경로를 키로 사용합니다. 이렇게 해야 서로 다른 위치의 디렉토리를 비교할 수 있습니다.

**실행:**

```bash
$ python examples/python/chapter06/ex28_01_file_hash.py
```

**결과:**

```
============================================================
  파일 해시 비교 도구 데모
============================================================

--- 1. 개별 파일 해시 계산 ---

  [파일A] 파일A.txt
    MD5   : 81bc7c554c1baf745ab667e369a2eed9
    SHA256: 609bdaea22426168032554eee612aabd1f31404ce671ffeb0d6731a579882e3f

  [파일B] 파일B.txt
    MD5   : 81bc7c554c1baf745ab667e369a2eed9
    SHA256: 609bdaea22426168032554eee612aabd1f31404ce671ffeb0d6731a579882e3f

  [파일C] 파일C.txt
    MD5   : 6621b8639ac3896de0c2f1f7cc6bbd69
    SHA256: 07c3729638f6a295422d6577f6ad496b8d41b7bf11d451c24ca64a0827041f87

--- 2. 파일 해시 비교 ---

  파일A vs 파일B (동일 내용): 동일함
  파일A vs 파일C (다른 내용): 다름

--- 3. 디렉토리 전체 파일 해시 ---

  총 파일 수: 4개

    파일A.txt
      SHA256: 609bdaea22426168032554eee612aabd...
    파일B.txt
      SHA256: 609bdaea22426168032554eee612aabd...
    파일C.txt
      SHA256: 07c3729638f6a295422d6577f6ad496b...
    하위폴더/설정.txt
      SHA256: b476f93fdf61fb5c5d60825f65c38e62...

--- 4. 알고리즘별 해시값 길이 비교 ---

  MD5    (32자): 81bc7c554c1baf745ab667e369a2eed9
  SHA256 (64자): 609bdaea22426168032554eee612aabd1f31404ce671ffeb0d6731a579882e3f

  * SHA256이 더 길고 안전하지만, 단순 변경 감지에는 MD5도 충분합니다.
```

결과를 보면, 파일A와 파일B는 내용이 동일하므로 MD5와 SHA256 모두 같은 해시값을 가집니다. 반면 파일C는 내용이 다르므로 완전히 다른 해시값이 나옵니다. 하위 폴더의 파일도 상대 경로(`하위폴더/설정.txt`)로 정확히 추적됩니다.

> **Note:** MD5는 32자, SHA256은 64자입니다. SHA256이 더 안전하고 충돌 가능성이 낮지만, 단순 변경 감지 용도로는 MD5도 충분합니다. 이 프로젝트에서는 안전성을 위해 SHA256을 기본으로 사용합니다.

---

## 28.3 단계 2: 변경 파일 감지

### AI에게 보내는 프롬프트

```
파일 해시 비교 기능이 완성되었어. 다음 단계로 두 디렉토리를
비교하여 변경된 파일을 감지하는 기능을 만들어줘.

요구사항:
1. 소스/대상 디렉토리를 스캔하여 파일 정보를 수집하는 함수
2. 파일 정보는 dataclass로: 상대경로, 크기, 수정시간, 해시값
3. 비교 결과도 dataclass로: 추가/수정/삭제/변경없음 목록
4. 변경 사항 요약 문자열과 has_changes 속성 포함
5. 앞서 만든 해시 함수를 활용해줘
```

### 핵심 개념: 변경 감지 로직

두 디렉토리를 비교할 때 파일은 4가지 상태 중 하나에 해당합니다:

```
소스에만 있음     → 추가(added) 필요
대상에만 있음     → 삭제(deleted) 대상
양쪽에 있고 다름  → 수정(modified) 필요
양쪽에 있고 같음  → 변경 없음(unchanged)
```

이를 집합 연산으로 구현하면 깔끔합니다:

```python
source_paths = set(source_files.keys())
target_paths = set(target_files.keys())

added    = source_paths - target_paths   # 소스에만 존재
deleted  = target_paths - source_paths   # 대상에만 존재
common   = source_paths & target_paths   # 양쪽 모두 존재 → 해시 비교
```

### 예제 코드

**예제 28-2: 변경 파일 감지**

```python
# examples/python/chapter06/ex28_02_detect_changes.py
import hashlib
import os
from dataclasses import dataclass, field
from pathlib import Path


def file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """파일의 SHA256 해시를 계산합니다."""
    hasher = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


@dataclass
class FileInfo:
    """파일의 메타데이터를 담는 데이터 클래스"""
    relative_path: str       # 기준 디렉토리로부터의 상대 경로
    size: int                # 파일 크기 (바이트)
    modified_time: float     # 마지막 수정 시간 (타임스탬프)
    hash_value: str          # SHA256 해시값


@dataclass
class ChangeReport:
    """두 디렉토리 비교 결과를 담는 데이터 클래스"""
    added: list = field(default_factory=list)      # 소스에만 존재하는 파일
    modified: list = field(default_factory=list)    # 양쪽 모두 존재하나 내용이 다른 파일
    deleted: list = field(default_factory=list)     # 대상에만 존재하는 파일
    unchanged: list = field(default_factory=list)   # 동일한 파일

    def summary(self) -> str:
        """변경 사항 요약 문자열을 반환합니다."""
        lines = []
        lines.append(f"  추가된 파일: {len(self.added)}개")
        lines.append(f"  수정된 파일: {len(self.modified)}개")
        lines.append(f"  삭제된 파일: {len(self.deleted)}개")
        lines.append(f"  변경 없음:   {len(self.unchanged)}개")
        return "\n".join(lines)

    @property
    def has_changes(self) -> bool:
        """변경 사항이 있는지 여부"""
        return bool(self.added or self.modified or self.deleted)


def scan_directory(directory: str) -> dict:
    """
    디렉토리를 스캔하여 모든 파일의 정보를 수집합니다.

    Returns:
        {상대경로: FileInfo} 형태의 딕셔너리
    """
    file_map = {}
    base_path = Path(directory)

    for file_path in sorted(base_path.rglob("*")):
        if file_path.is_file():
            rel_path = str(file_path.relative_to(base_path))
            stat = file_path.stat()
            file_map[rel_path] = FileInfo(
                relative_path=rel_path,
                size=stat.st_size,
                modified_time=stat.st_mtime,
                hash_value=file_hash(str(file_path)),
            )

    return file_map


def detect_changes(source_dir: str, target_dir: str) -> ChangeReport:
    """
    소스 디렉토리와 대상 디렉토리를 비교하여 변경 사항을 감지합니다.
    """
    report = ChangeReport()

    source_files = scan_directory(source_dir)
    target_files = scan_directory(target_dir)

    source_paths = set(source_files.keys())
    target_paths = set(target_files.keys())

    # 1. 추가된 파일: 소스에만 존재
    for path in sorted(source_paths - target_paths):
        report.added.append(source_files[path])

    # 2. 삭제된 파일: 대상에만 존재
    for path in sorted(target_paths - source_paths):
        report.deleted.append(target_files[path])

    # 3. 양쪽 모두 존재하는 파일: 해시 비교로 수정 여부 판단
    for path in sorted(source_paths & target_paths):
        src_info = source_files[path]
        tgt_info = target_files[path]

        if src_info.hash_value != tgt_info.hash_value:
            report.modified.append(src_info)
        else:
            report.unchanged.append(src_info)

    return report
```

이 코드에서 주목할 구조적 특징은 다음과 같습니다:

1. **`@dataclass`의 활용**: `FileInfo`와 `ChangeReport`를 데이터클래스로 정의하여 코드를 깔끔하게 유지합니다. `field(default_factory=list)`를 사용하면 가변 기본값 문제를 피할 수 있습니다.
2. **`@property`**: `has_changes`를 프로퍼티로 만들어 `report.has_changes`처럼 자연스럽게 사용할 수 있습니다.
3. **`pathlib.Path.rglob("*")`**: 하위 디렉토리까지 재귀적으로 탐색합니다.

**실행:**

```bash
$ python examples/python/chapter06/ex28_02_detect_changes.py
```

**결과:**

```
============================================================
  변경 파일 감지 도구 데모
============================================================

--- 시나리오 1: 초기 상태 (변경 없음) ---
  추가된 파일: 0개
  수정된 파일: 0개
  삭제된 파일: 0개
  변경 없음:   5개
  변경 필요: 아니오

--- 시나리오 2: 소스에 새 파일 추가 ---
  추가된 파일: 1개
  수정된 파일: 0개
  삭제된 파일: 0개
  변경 없음:   5개

  [+] 추가된 파일:
      + src/new_feature.py (69 바이트)

--- 시나리오 3: 소스의 기존 파일 수정 ---
  추가된 파일: 1개
  수정된 파일: 1개
  삭제된 파일: 0개
  변경 없음:   4개

  [~] 수정된 파일:
      ~ config.json (57 바이트)

--- 시나리오 4: 소스에서 파일 삭제 ---
  추가된 파일: 1개
  수정된 파일: 1개
  삭제된 파일: 1개
  변경 없음:   3개

  [-] 삭제된 파일:
      - docs/guide.txt
```

데모는 4가지 시나리오를 통해 변경 감지가 정확히 동작하는 것을 보여줍니다. 소스에 파일을 추가하고, 수정하고, 삭제하는 변화를 자동으로 감지합니다.

> **Tip:** AI에게 "데모 코드도 포함해줘"라고 요청하면 이렇게 다양한 시나리오를 자동으로 만들어줍니다. 데모 코드는 기능 검증과 사용 방법 문서화를 동시에 수행하므로 매우 유용합니다.

---

## 28.4 단계 3: 동기화 로직

### AI에게 보내는 프롬프트

```
변경 감지 기능이 잘 동작해. 이제 실제로 파일을 동기화하는
로직을 만들어줘.

요구사항:
1. 소스 → 대상 단방향 동기화 (소스 기준으로 대상을 맞춤)
2. 추가된 파일: 소스에서 대상으로 복사
3. 수정된 파일: 소스 파일로 대상 파일 덮어쓰기
4. 삭제된 파일: 대상에서 제거 (옵션으로 on/off)
5. dry_run 모드: 실제 변경 없이 시뮬레이션만 수행
6. 결과를 SyncResult dataclass로 반환
7. 빈 하위 디렉토리 자동 정리
```

### 핵심 개념: 단방향 동기화

단방향 동기화(one-way sync)는 소스 디렉토리를 "진실의 원천(source of truth)"으로 삼아 대상 디렉토리를 소스와 동일하게 맞추는 방식입니다.

```
소스 디렉토리 (원본)          대상 디렉토리 (사본)
├── README.md (v2)    ──→    ├── README.md (v2)     [수정 반영]
├── config.json       ──→    ├── config.json         [새로 복사]
├── src/app.py        ──→    ├── src/app.py          [동일: 건너뜀]
├── src/utils.py      ──→    ├── src/utils.py        [새로 복사]
                             ├── old_file.txt        [삭제됨]
```

`dry_run` 모드가 중요한 이유는, 실수로 파일을 삭제하거나 덮어쓰는 사고를 방지할 수 있기 때문입니다. 항상 먼저 시뮬레이션을 돌려보고, 결과를 확인한 뒤 실제 동기화를 수행하는 습관을 들이세요.

### 예제 코드

**예제 28-3: 동기화 로직**

```python
# examples/python/chapter06/ex28_03_sync_logic.py
import hashlib
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path


def file_hash(file_path: str) -> str:
    """파일의 SHA256 해시를 계산합니다."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


@dataclass
class SyncResult:
    """동기화 결과를 담는 데이터 클래스"""
    copied: list = field(default_factory=list)     # 복사된(추가/수정) 파일
    deleted: list = field(default_factory=list)     # 삭제된 파일
    skipped: list = field(default_factory=list)     # 건너뛴(동일) 파일
    errors: list = field(default_factory=list)      # 오류 발생 파일

    def summary(self) -> str:
        lines = [
            f"  복사됨: {len(self.copied)}개",
            f"  삭제됨: {len(self.deleted)}개",
            f"  건너뜀: {len(self.skipped)}개",
            f"  오류:   {len(self.errors)}개",
        ]
        return "\n".join(lines)


def scan_files(directory: str) -> dict:
    """디렉토리 내 모든 파일의 {상대경로: 해시} 딕셔너리를 반환합니다."""
    result = {}
    base = Path(directory)
    for file_path in sorted(base.rglob("*")):
        if file_path.is_file():
            rel = str(file_path.relative_to(base))
            result[rel] = file_hash(str(file_path))
    return result


def sync_directories(
    source_dir: str,
    target_dir: str,
    delete_extra: bool = True,
    dry_run: bool = False,
) -> SyncResult:
    """
    소스 디렉토리를 기준으로 대상 디렉토리를 동기화합니다.

    Args:
        source_dir: 소스(원본) 디렉토리
        target_dir: 대상(사본) 디렉토리
        delete_extra: True이면 소스에 없는 대상 파일을 삭제
        dry_run: True이면 실제 작업 없이 시뮬레이션만 수행
    """
    result = SyncResult()

    source_files = scan_files(source_dir)
    target_files = scan_files(target_dir)

    source_paths = set(source_files.keys())
    target_paths = set(target_files.keys())

    # 1단계: 추가/수정 파일 복사 (소스 → 대상)
    for rel_path in sorted(source_paths):
        src_full = os.path.join(source_dir, rel_path)
        tgt_full = os.path.join(target_dir, rel_path)

        if rel_path not in target_files:
            action = "추가"
        elif source_files[rel_path] != target_files[rel_path]:
            action = "수정"
        else:
            result.skipped.append(rel_path)
            continue

        try:
            if not dry_run:
                os.makedirs(os.path.dirname(tgt_full), exist_ok=True)
                shutil.copy2(src_full, tgt_full)
            result.copied.append((rel_path, action))
        except Exception as e:
            result.errors.append((rel_path, str(e)))

    # 2단계: 소스에 없는 파일 삭제 (옵션)
    if delete_extra:
        for rel_path in sorted(target_paths - source_paths):
            tgt_full = os.path.join(target_dir, rel_path)
            try:
                if not dry_run:
                    os.remove(tgt_full)
                result.deleted.append(rel_path)
            except Exception as e:
                result.errors.append((rel_path, str(e)))

        # 빈 디렉토리 정리
        if not dry_run:
            _cleanup_empty_dirs(target_dir)

    return result


def _cleanup_empty_dirs(directory: str):
    """빈 하위 디렉토리를 재귀적으로 삭제합니다."""
    for root, dirs, files in os.walk(directory, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
            except OSError:
                pass
```

핵심 로직을 정리하면 다음과 같습니다:

| 단계 | 작업 | 조건 |
|------|------|------|
| **1단계** | 소스 파일을 대상으로 복사 | 대상에 없거나 해시가 다른 경우 |
| **2단계** | 대상의 불필요한 파일 삭제 | `delete_extra=True`이고 소스에 없는 경우 |
| **3단계** | 빈 디렉토리 정리 | 삭제 후 비어있는 폴더 제거 |

`shutil.copy2()`는 파일 내용뿐 아니라 수정 시간 등 메타데이터도 함께 복사하므로, 동기화 후에도 원본과 동일한 타임스탬프를 유지합니다.

**실행:**

```bash
$ python examples/python/chapter06/ex28_03_sync_logic.py
```

**결과:**

```
============================================================
  디렉토리 동기화 도구 데모
============================================================

--- 시나리오 1: 시뮬레이션 (dry-run) ---
  * 실제 파일 변경 없이 어떤 작업이 수행될지 미리 확인합니다.

  복사됨: 4개
  삭제됨: 1개
  건너뜀: 1개
  오류:   0개

  [시뮬레이션] 복사된 파일:
    ~ [수정] README.md
    + [추가] config.json
    + [추가] data/sample.txt
    + [추가] src/utils.py

  [시뮬레이션] 삭제된 파일:
    - [삭제] old_file.txt

  [시뮬레이션] 건너뛴 파일:
    = [동일] src/app.py

  대상 디렉토리 파일 수 (변경 전): 3개

--- 시나리오 2: 실제 동기화 실행 ---
  * 소스 → 대상 방향으로 완전 동기화를 수행합니다.

  복사됨: 4개
  삭제됨: 1개
  건너뜀: 1개
  오류:   0개

  대상 디렉토리 파일 수 (동기화 후): 5개

--- 시나리오 3: 재동기화 (변경 없음 확인) ---
  * 이미 동기화된 상태에서 다시 실행하면 모든 파일을 건너뜁니다.

  복사됨: 0개
  삭제됨: 0개
  건너뜀: 5개
  오류:   0개
```

시나리오 1에서 `dry_run=True`로 시뮬레이션을 수행한 뒤, 시나리오 2에서 실제 동기화를 실행합니다. 시나리오 3에서 이미 동기화된 상태를 다시 확인하면, 모든 파일이 건너뜀 처리되어 불필요한 작업이 수행되지 않음을 검증합니다.

> **Warning:** `delete_extra=True` 옵션을 사용할 때는 주의하세요. 대상 디렉토리에만 존재하는 파일이 영구 삭제됩니다. 중요한 데이터가 있을 수 있으므로 반드시 먼저 `dry_run=True`로 시뮬레이션을 돌려 확인하세요.

---

## 28.5 단계 4: 충돌 처리

### AI에게 보내는 프롬프트

```
단방향 동기화는 잘 동작해. 이제 양방향 동기화 시 발생하는
충돌을 처리하는 기능을 추가해줘.

요구사항:
1. 양쪽 모두 변경된 파일을 '충돌'로 감지
2. 마지막 동기화 시점의 해시를 기준으로 양쪽 변경 여부 판단
3. 충돌 해결 전략을 Enum으로 정의:
   - NEWER_WINS: 최신 수정 파일 우선
   - LARGER_WINS: 더 큰 파일 우선
   - SOURCE_WINS: 항상 소스 우선
   - TARGET_WINS: 항상 대상 우선
   - BACKUP_BOTH: 양쪽 백업 후 소스 적용
4. 충돌 이력을 JSON으로 저장
5. ConflictInfo dataclass에 해결 정보 포함
```

### 핵심 개념: 양방향 동기화와 충돌

단방향 동기화에서는 소스가 항상 "정답"이므로 충돌이 발생하지 않습니다. 하지만 양방향 동기화에서는 **양쪽 모두 같은 파일을 수정했을 때** 어느 쪽을 적용해야 할지 결정해야 합니다. 이것이 바로 **충돌(conflict)**입니다.

```
마지막 동기화 시점:     소스: "원본"    대상: "원본"    (동일)
         ↓
양쪽에서 각각 수정:     소스: "수정A"   대상: "수정B"   (충돌!)
```

충돌을 감지하려면 **마지막 동기화 시점의 해시**를 기억해야 합니다. 이 기준 해시와 현재 해시를 비교하여 한쪽만 변경되었는지, 양쪽 모두 변경되었는지 판단합니다.

### 예제 코드

**예제 28-4: 충돌 처리**

```python
# examples/python/chapter06/ex28_04_conflict_handler.py
import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path


class ConflictStrategy(Enum):
    """충돌 해결 전략"""
    NEWER_WINS = "newer_wins"           # 최신 수정 파일 우선
    LARGER_WINS = "larger_wins"         # 더 큰 파일 우선
    SOURCE_WINS = "source_wins"         # 항상 소스 우선
    TARGET_WINS = "target_wins"         # 항상 대상 우선
    BACKUP_BOTH = "backup_both"         # 양쪽 모두 백업 후 소스 적용


@dataclass
class ConflictInfo:
    """충돌 정보를 담는 데이터 클래스"""
    relative_path: str
    source_modified: float
    target_modified: float
    source_size: int
    target_size: int
    source_hash: str
    target_hash: str
    resolution: str = ""
    resolved_by: str = ""

    def to_dict(self) -> dict:
        """JSON 직렬화를 위한 딕셔너리 변환"""
        return {
            "파일": self.relative_path,
            "소스_수정시간": datetime.fromtimestamp(self.source_modified).isoformat(),
            "대상_수정시간": datetime.fromtimestamp(self.target_modified).isoformat(),
            "소스_크기": self.source_size,
            "대상_크기": self.target_size,
            "해결_방법": self.resolution,
            "적용_기준": self.resolved_by,
        }


def detect_conflicts(source_dir: str, target_dir: str,
                     last_sync_hashes: dict = None) -> list:
    """
    양방향 동기화 시 충돌을 감지합니다.

    양쪽 모두 변경된 파일이 충돌입니다.
    last_sync_hashes: 마지막 동기화 시점의 해시 딕셔너리.
    이 값이 None이면 양쪽 해시가 다른 모든 공통 파일을 충돌로 간주합니다.
    """
    conflicts = []
    src_base = Path(source_dir)
    tgt_base = Path(target_dir)

    src_files = {str(p.relative_to(src_base)) for p in src_base.rglob("*") if p.is_file()}
    tgt_files = {str(p.relative_to(tgt_base)) for p in tgt_base.rglob("*") if p.is_file()}

    for rel_path in sorted(src_files & tgt_files):
        src_full = os.path.join(source_dir, rel_path)
        tgt_full = os.path.join(target_dir, rel_path)

        src_hash = file_hash(src_full)
        tgt_hash = file_hash(tgt_full)

        # 해시가 동일하면 충돌 아님
        if src_hash == tgt_hash:
            continue

        # last_sync_hashes가 있으면, 양쪽 모두 변경되었는지 확인
        if last_sync_hashes and rel_path in last_sync_hashes:
            base_hash = last_sync_hashes[rel_path]
            src_changed = (src_hash != base_hash)
            tgt_changed = (tgt_hash != base_hash)
            if not (src_changed and tgt_changed):
                continue

        src_stat = os.stat(src_full)
        tgt_stat = os.stat(tgt_full)

        conflicts.append(ConflictInfo(
            relative_path=rel_path,
            source_modified=src_stat.st_mtime,
            target_modified=tgt_stat.st_mtime,
            source_size=src_stat.st_size,
            target_size=tgt_stat.st_size,
            source_hash=src_hash,
            target_hash=tgt_hash,
        ))

    return conflicts


def resolve_conflict(
    conflict: ConflictInfo,
    source_dir: str,
    target_dir: str,
    strategy: ConflictStrategy,
    backup_dir: str = None,
) -> ConflictInfo:
    """주어진 전략에 따라 충돌을 해결합니다."""
    src_path = os.path.join(source_dir, conflict.relative_path)
    tgt_path = os.path.join(target_dir, conflict.relative_path)

    if strategy == ConflictStrategy.NEWER_WINS:
        if conflict.source_modified >= conflict.target_modified:
            shutil.copy2(src_path, tgt_path)
            conflict.resolution = "소스 파일 적용 (더 최신)"
            conflict.resolved_by = "newer_wins -> source"
        else:
            shutil.copy2(tgt_path, src_path)
            conflict.resolution = "대상 파일 적용 (더 최신)"
            conflict.resolved_by = "newer_wins -> target"

    elif strategy == ConflictStrategy.LARGER_WINS:
        if conflict.source_size >= conflict.target_size:
            shutil.copy2(src_path, tgt_path)
            conflict.resolution = "소스 파일 적용 (더 큰 파일)"
            conflict.resolved_by = "larger_wins -> source"
        else:
            shutil.copy2(tgt_path, src_path)
            conflict.resolution = "대상 파일 적용 (더 큰 파일)"
            conflict.resolved_by = "larger_wins -> target"

    elif strategy == ConflictStrategy.SOURCE_WINS:
        shutil.copy2(src_path, tgt_path)
        conflict.resolution = "소스 파일 적용 (소스 우선 정책)"
        conflict.resolved_by = "source_wins"

    elif strategy == ConflictStrategy.TARGET_WINS:
        shutil.copy2(tgt_path, src_path)
        conflict.resolution = "대상 파일 적용 (대상 우선 정책)"
        conflict.resolved_by = "target_wins"

    elif strategy == ConflictStrategy.BACKUP_BOTH:
        if backup_dir is None:
            backup_dir = os.path.join(os.path.dirname(source_dir), "_conflict_backups")
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(conflict.relative_path)
        name, ext = os.path.splitext(base_name)

        src_backup = os.path.join(backup_dir, f"{name}_source_{timestamp}{ext}")
        shutil.copy2(src_path, src_backup)

        tgt_backup = os.path.join(backup_dir, f"{name}_target_{timestamp}{ext}")
        shutil.copy2(tgt_path, tgt_backup)

        shutil.copy2(src_path, tgt_path)
        conflict.resolution = f"양쪽 백업 후 소스 적용 (백업: {backup_dir})"
        conflict.resolved_by = "backup_both -> source applied"

    return conflict


def save_conflict_report(conflicts: list, report_path: str):
    """충돌 이력을 JSON 파일로 저장합니다."""
    report = {
        "생성시간": datetime.now().isoformat(),
        "총_충돌수": len(conflicts),
        "충돌_목록": [c.to_dict() for c in conflicts],
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
```

`file_hash` 함수는 이전 예제와 동일한 패턴입니다 (전체 코드는 예제 파일 참조).

각 충돌 해결 전략의 특징을 표로 정리하면 다음과 같습니다:

| 전략 | 기준 | 적합한 상황 |
|------|------|------------|
| **NEWER_WINS** | 수정 시간 | 최신 작업이 중요한 경우 |
| **LARGER_WINS** | 파일 크기 | 더 많은 내용이 가치있는 경우 |
| **SOURCE_WINS** | 소스 우선 | 소스가 항상 기준인 경우 |
| **TARGET_WINS** | 대상 우선 | 대상의 로컬 수정을 보존할 경우 |
| **BACKUP_BOTH** | 양쪽 백업 | 데이터 손실을 절대 원하지 않는 경우 |

**실행:**

```bash
$ python examples/python/chapter06/ex28_04_conflict_handler.py
```

**결과:**

```
============================================================
  양방향 동기화 충돌 처리 데모
============================================================

--- 1. 충돌 감지 ---

  감지된 충돌: 3건

  충돌 1: 문서.txt
    소스 - 수정: 02:22:27, 크기: 55B, 해시: 1e1ea4bebe2892f5...
    대상 - 수정: 02:22:27, 크기: 40B, 해시: bdea07d1455c61d5...
  충돌 2: 설정.json
    소스 - 수정: 02:22:27, 크기: 50B, 해시: af93af04c834e67f...
    대상 - 수정: 02:22:27, 크기: 34B, 해시: 610b6746a3a1a9a5...
  충돌 3: 코드/메인.py
    소스 - 수정: 02:22:27, 크기: 66B, 해시: 0ba8f84a955c100a...
    대상 - 수정: 02:22:27, 크기: 45B, 해시: 48261ace8d7dbdb2...

--- 2. 전략별 충돌 해결 ---

  충돌 1 (문서.txt): 최신 파일 우선 전략 적용
    결과: 대상 파일 적용 (더 최신)

  충돌 2 (설정.json): 큰 파일 우선 전략 적용
    결과: 소스 파일 적용 (더 큰 파일)

  충돌 3 (코드/메인.py): 양쪽 백업 후 적용 전략 적용
    결과: 양쪽 백업 후 소스 적용

--- 3. 충돌 보고서 저장 ---

  총 충돌 수: 3건

  보고서 내용:
{
    "생성시간": "2026-01-28T02:22:27.854092",
    "총_충돌수": 3,
    "충돌_목록": [
        {
            "파일": "문서.txt",
            "소스_수정시간": "2026-01-28T02:22:27.425328",
            "대상_수정시간": "2026-01-28T02:22:27.626328",
            "소스_크기": 55,
            "대상_크기": 40,
            "해결_방법": "대상 파일 적용 (더 최신)",
            "적용_기준": "newer_wins -> target"
        },
        ...
    ]
}

--- 4. 백업 파일 확인 ---

  백업 파일 수: 2개
    - 메인_source_20260128_022227.py (66 바이트)
    - 메인_target_20260128_022227.py (45 바이트)
```

데모에서 3건의 충돌이 감지되었고, 각각 다른 전략으로 해결되었습니다. `BACKUP_BOTH` 전략을 적용한 `코드/메인.py`는 양쪽 버전이 모두 백업 디렉토리에 안전하게 보관되었습니다.

> **Note:** 충돌 보고서를 JSON으로 저장하면 나중에 어떤 충돌이 발생했고 어떻게 해결되었는지 추적할 수 있습니다. 이는 실무에서 문제 발생 시 원인 분석에 매우 유용합니다.

---

## 28.6 단계 5: 로그 기록

### AI에게 보내는 프롬프트

```
동기화 기능이 거의 완성되었어. 이제 모든 작업을 체계적으로
기록하는 로깅 시스템을 추가해줘.

요구사항:
1. logging 모듈을 사용하는 SyncLogger 클래스
2. 콘솔 출력: INFO 이상 레벨, 간결한 포맷
3. 파일 로그: DEBUG 이상 레벨, 타임스탬프 포함 상세 포맷
4. 작업별 통계 카운터 (복사, 삭제, 건너뜀, 충돌, 오류)
5. start_sync / end_sync로 작업 시간 측정
6. 작업 유형별 메서드: log_copy, log_delete, log_skip, log_conflict, log_error
```

### 핵심 개념: 로깅 시스템 설계

프로그램이 "무엇을 했는지"를 기록하는 것은 디버깅과 운영에 필수입니다. `print()`를 사용할 수도 있지만, `logging` 모듈은 다음과 같은 강점을 제공합니다:

| 기능 | print() | logging |
|------|---------|---------|
| 레벨 구분 | X | DEBUG, INFO, WARNING, ERROR |
| 파일 출력 | 직접 구현 | 핸들러 추가만으로 가능 |
| 포맷 커스텀 | 직접 구현 | Formatter로 설정 |
| 필터링 | 불가 | 레벨별 자동 필터링 |
| 타임스탬프 | 직접 구현 | 포맷 문자열로 자동 |

이 프로젝트에서는 **두 개의 핸들러**를 사용합니다:
- **콘솔 핸들러**: INFO 이상만 표시 (사용자에게 핵심 정보만)
- **파일 핸들러**: DEBUG 이상 모두 기록 (문제 추적용 상세 로그)

### 예제 코드

**예제 28-5: 동기화 로그 기록**

```python
# examples/python/chapter06/ex28_05_sync_logger.py
import logging
import os
import time
from datetime import datetime


class SyncLogger:
    """
    동기화 작업 전용 로거 클래스

    - 콘솔: INFO 이상 레벨을 간결하게 출력
    - 파일: DEBUG 이상 레벨을 상세하게 기록
    - 통계 추적: 작업별 카운터 관리
    """

    def __init__(self, name: str = "file_sync", log_dir: str = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()

        # 통계 카운터
        self.stats = {
            "복사": 0,
            "삭제": 0,
            "건너뜀": 0,
            "충돌": 0,
            "오류": 0,
        }
        self.start_time = None

        # 콘솔 핸들러 설정 (INFO 이상)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            "  [%(levelname)-7s] %(message)s"
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

        # 파일 핸들러 설정 (DEBUG 이상)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"sync_{timestamp}.log")
            self.log_file = log_file

            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                "%(asctime)s [%(levelname)-7s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
        else:
            self.log_file = None

    def start_sync(self, source: str, target: str):
        """동기화 시작을 기록합니다."""
        self.start_time = time.time()
        self.logger.info("=" * 50)
        self.logger.info("동기화 작업 시작")
        self.logger.info(f"  소스: {source}")
        self.logger.info(f"  대상: {target}")
        self.logger.debug(f"시작 시간: {datetime.now().isoformat()}")

    def end_sync(self):
        """동기화 완료를 기록합니다."""
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.logger.info("-" * 50)
        self.logger.info("동기화 작업 완료")
        self.logger.info(f"  소요 시간: {elapsed:.2f}초")
        self.logger.info(f"  복사: {self.stats['복사']}건 | "
                         f"삭제: {self.stats['삭제']}건 | "
                         f"건너뜀: {self.stats['건너뜀']}건")
        if self.stats["충돌"] > 0:
            self.logger.warning(f"  충돌: {self.stats['충돌']}건")
        if self.stats["오류"] > 0:
            self.logger.error(f"  오류: {self.stats['오류']}건")
        self.logger.info("=" * 50)

    def log_copy(self, rel_path: str, action: str = "복사"):
        """파일 복사를 기록합니다."""
        self.stats["복사"] += 1
        self.logger.info(f"[{action}] {rel_path}")
        self.logger.debug(f"  작업: {action}, 파일: {rel_path}")

    def log_delete(self, rel_path: str):
        """파일 삭제를 기록합니다."""
        self.stats["삭제"] += 1
        self.logger.info(f"[삭제] {rel_path}")

    def log_skip(self, rel_path: str, reason: str = "동일"):
        """파일 건너뛰기를 기록합니다."""
        self.stats["건너뜀"] += 1
        self.logger.debug(f"[건너뜀] {rel_path} (사유: {reason})")

    def log_conflict(self, rel_path: str, resolution: str):
        """충돌 해결을 기록합니다."""
        self.stats["충돌"] += 1
        self.logger.warning(f"[충돌] {rel_path} -> {resolution}")

    def log_error(self, rel_path: str, error: str):
        """오류를 기록합니다."""
        self.stats["오류"] += 1
        self.logger.error(f"[오류] {rel_path}: {error}")

    def log_scan(self, directory: str, file_count: int):
        """디렉토리 스캔 결과를 기록합니다."""
        self.logger.info(f"[스캔] {directory} ({file_count}개 파일)")
```

`SyncLogger` 클래스의 설계 포인트를 정리합니다:

1. **레벨 분리**: `log_skip()`은 `DEBUG`로 기록하여 콘솔에는 표시되지 않습니다. 변경 없는 파일이 수백 개일 때 콘솔이 지저분해지는 것을 방지합니다.
2. **통계 카운터**: 각 메서드 호출 시 자동으로 카운터가 증가하므로, `end_sync()`에서 정확한 요약을 출력합니다.
3. **핸들러 초기화**: `self.logger.handlers.clear()`로 기존 핸들러를 제거합니다. 이렇게 하지 않으면 로거를 여러 번 생성할 때 핸들러가 중복 등록되어 같은 메시지가 여러 번 출력됩니다.

**실행:**

```bash
$ python examples/python/chapter06/ex28_05_sync_logger.py
```

**결과:**

```
============================================================
  동기화 로그 기록 도구 데모
============================================================

--- 동기화 실행 (로그 기록 활성화) ---

  [INFO   ] ==================================================
  [INFO   ] 동기화 작업 시작
  [INFO   ]   소스: /tmp/.../source
  [INFO   ]   대상: /tmp/.../target
  [INFO   ] [스캔] /tmp/.../source (5개 파일)
  [INFO   ] [스캔] /tmp/.../target (3개 파일)
  [INFO   ] [수정] README.md
  [INFO   ] [추가] config.json
  [INFO   ] [추가] src/new_module.py
  [INFO   ] [추가] src/utils.py
  [INFO   ] [삭제] deprecated.txt
  [INFO   ] --------------------------------------------------
  [INFO   ] 동기화 작업 완료
  [INFO   ]   소요 시간: 0.02초
  [INFO   ]   복사: 4건 | 삭제: 1건 | 건너뜀: 1건
  [INFO   ] ==================================================

--- 로그 파일 내용 ---

  | 2026-01-28 02:22:35 [INFO   ] 동기화 작업 시작
  | 2026-01-28 02:22:35 [DEBUG  ] 시작 시간: 2026-01-28T02:22:35.215784
  | 2026-01-28 02:22:35 [INFO   ] [스캔] .../source (5개 파일)
  | 2026-01-28 02:22:35 [DEBUG  ]   스캔 완료: .../source, 파일 수: 5
  | 2026-01-28 02:22:35 [INFO   ] [수정] README.md
  | 2026-01-28 02:22:35 [DEBUG  ]   작업: 수정, 파일: README.md
  | 2026-01-28 02:22:35 [DEBUG  ] [건너뜀] src/app.py (사유: 해시 동일)
  ...

--- 최종 통계 ---

  작업 통계:
    복사    :   4 ####
    삭제    :   1 #
    건너뜀   :   1 #
    충돌    :   0
    오류    :   0
```

콘솔 출력에는 INFO 이상만 표시되어 깔끔합니다. 반면 로그 파일에는 DEBUG 레벨의 상세 정보(건너뛴 파일, 스캔 상세)까지 모두 기록됩니다. 문제가 발생했을 때 로그 파일을 열어 정확한 원인을 추적할 수 있습니다.

> **Tip:** 로그 레벨 체계를 기억하세요: `DEBUG < INFO < WARNING < ERROR < CRITICAL`. 콘솔에는 `INFO` 이상, 파일에는 `DEBUG` 이상을 기록하는 것이 일반적인 패턴입니다.

---

## 28.7 단계 6: CLI 인터페이스

### AI에게 보내는 프롬프트

```
마지막 단계야! 지금까지 만든 모든 기능을 하나로 통합하는
CLI 인터페이스를 만들어줘.

요구사항:
1. argparse로 서브커맨드 구조 (scan, compare, sync)
2. scan: 디렉토리 스캔 후 파일 목록 출력, JSON 저장 옵션
3. compare: 두 디렉토리 비교 후 차이점 출력
4. sync: 소스→대상 동기화 (--delete, --dry-run, --verbose, --log-file 옵션)
5. --version으로 버전 확인
6. 인자 없이 실행하면 데모 모드로 전환
7. 지금까지 만든 해시, 스캔, 동기화, 로깅 기능을 모두 통합
```

### 핵심 개념: 서브커맨드 패턴

`git`처럼 하나의 프로그램 안에 여러 명령어를 두는 패턴을 **서브커맨드(subcommand)**라고 합니다. `argparse`의 `add_subparsers()`로 이를 구현합니다.

```bash
$ file_sync scan ./my_folder              # 디렉토리 스캔
$ file_sync compare ./source ./target     # 두 디렉토리 비교
$ file_sync sync ./source ./target        # 동기화 실행
$ file_sync sync ./source ./target --delete --dry-run  # 시뮬레이션
```

각 서브커맨드에 `.set_defaults(func=handler_function)`을 설정하면, `args.func(args)`로 해당 핸들러를 자동 호출할 수 있습니다.

### 예제 코드

**예제 28-6: CLI 인터페이스**

```python
# examples/python/chapter06/ex28_06_sync_cli.py
import argparse
import hashlib
import json
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


# ========== 핵심 유틸리티 함수 ==========

def file_hash(path: str) -> str:
    """파일의 SHA256 해시를 계산합니다."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_directory(directory: str) -> dict:
    """디렉토리 내 모든 파일의 {상대경로: 해시} 딕셔너리를 반환합니다."""
    result = {}
    base = Path(directory)
    if not base.exists():
        return result
    for p in sorted(base.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(base))
            result[rel] = file_hash(str(p))
    return result


def setup_logger(verbose: bool = False, log_file: str = None) -> logging.Logger:
    """로거를 설정하고 반환합니다."""
    logger = logging.getLogger("sync_cli")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if verbose else logging.INFO)
    ch.setFormatter(logging.Formatter("  [%(levelname)-7s] %(message)s"))
    logger.addHandler(ch)

    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)-7s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        logger.addHandler(fh)

    return logger


# ========== 서브커맨드 구현 ==========

def cmd_scan(args):
    """scan 서브커맨드: 디렉토리를 스캔하여 파일 목록과 해시를 출력합니다."""
    logger = setup_logger(args.verbose)
    directory = os.path.abspath(args.directory)

    if not os.path.isdir(directory):
        logger.error(f"디렉토리가 존재하지 않습니다: {directory}")
        return 1

    logger.info(f"디렉토리 스캔: {directory}")
    files = scan_directory(directory)

    total_size = 0
    for rel_path, hash_value in files.items():
        full_path = os.path.join(directory, rel_path)
        size = os.path.getsize(full_path)
        total_size += size
        if args.verbose:
            logger.debug(f"  {rel_path} ({size}B) -> {hash_value[:16]}...")
        else:
            logger.info(f"  {rel_path} ({size}B)")

    logger.info(f"총 {len(files)}개 파일, {total_size:,} 바이트")

    if args.output:
        output_data = {
            "디렉토리": directory,
            "스캔시간": datetime.now().isoformat(),
            "파일수": len(files),
            "파일목록": files,
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        logger.info(f"스캔 결과 저장: {args.output}")

    return 0


def cmd_compare(args):
    """compare 서브커맨드: 두 디렉토리를 비교합니다."""
    logger = setup_logger(args.verbose)
    source = os.path.abspath(args.source)
    target = os.path.abspath(args.target)

    logger.info(f"소스: {source}")
    logger.info(f"대상: {target}")

    src_files = scan_directory(source)
    tgt_files = scan_directory(target)

    src_paths = set(src_files.keys())
    tgt_paths = set(tgt_files.keys())

    added = sorted(src_paths - tgt_paths)
    deleted = sorted(tgt_paths - src_paths)
    common = sorted(src_paths & tgt_paths)
    modified = [p for p in common if src_files[p] != tgt_files[p]]
    unchanged = [p for p in common if src_files[p] == tgt_files[p]]

    if added:
        logger.info(f"추가 필요 ({len(added)}개):")
        for p in added:
            logger.info(f"  + {p}")
    if modified:
        logger.info(f"수정 필요 ({len(modified)}개):")
        for p in modified:
            logger.info(f"  ~ {p}")
    if deleted:
        logger.info(f"삭제 대상 ({len(deleted)}개):")
        for p in deleted:
            logger.info(f"  - {p}")

    logger.info(f"요약: 추가 {len(added)} | 수정 {len(modified)} | "
                f"삭제 {len(deleted)} | 동일 {len(unchanged)}")
    return 0


def cmd_sync(args):
    """sync 서브커맨드: 소스를 기준으로 대상을 동기화합니다."""
    log_file = args.log_file if hasattr(args, "log_file") else None
    logger = setup_logger(args.verbose, log_file)
    source = os.path.abspath(args.source)
    target = os.path.abspath(args.target)

    os.makedirs(target, exist_ok=True)

    logger.info("=" * 50)
    logger.info("파일 동기화 시작")
    logger.info(f"  소스: {source}")
    logger.info(f"  대상: {target}")
    logger.info(f"  삭제 모드: {'활성' if args.delete else '비활성'}")
    logger.info(f"  시뮬레이션: {'예' if args.dry_run else '아니오'}")

    src_files = scan_directory(source)
    tgt_files = scan_directory(target)

    stats = {"복사": 0, "삭제": 0, "건너뜀": 0, "오류": 0}

    for rel_path, src_hash in sorted(src_files.items()):
        src_full = os.path.join(source, rel_path)
        tgt_full = os.path.join(target, rel_path)

        if rel_path not in tgt_files:
            action = "추가"
        elif src_hash != tgt_files[rel_path]:
            action = "수정"
        else:
            stats["건너뜀"] += 1
            logger.debug(f"[건너뜀] {rel_path}")
            continue

        try:
            if not args.dry_run:
                os.makedirs(os.path.dirname(tgt_full), exist_ok=True)
                shutil.copy2(src_full, tgt_full)
            stats["복사"] += 1
            prefix = "[시뮬레이션] " if args.dry_run else ""
            logger.info(f"{prefix}[{action}] {rel_path}")
        except Exception as e:
            stats["오류"] += 1
            logger.error(f"[오류] {rel_path}: {e}")

    if args.delete:
        for rel_path in sorted(set(tgt_files.keys()) - set(src_files.keys())):
            tgt_full = os.path.join(target, rel_path)
            try:
                if not args.dry_run:
                    os.remove(tgt_full)
                stats["삭제"] += 1
                prefix = "[시뮬레이션] " if args.dry_run else ""
                logger.info(f"{prefix}[삭제] {rel_path}")
            except Exception as e:
                stats["오류"] += 1
                logger.error(f"[오류] {rel_path}: {e}")

    logger.info("동기화 완료")
    logger.info(f"  복사: {stats['복사']} | 삭제: {stats['삭제']} | "
                f"건너뜀: {stats['건너뜀']} | 오류: {stats['오류']}")
    logger.info("=" * 50)
    return 0


# ========== CLI 파서 구성 ==========

def create_parser() -> argparse.ArgumentParser:
    """명령줄 인자 파서를 생성합니다."""
    parser = argparse.ArgumentParser(
        prog="file_sync",
        description="파일 동기화 도구 - 바이브 코딩으로 만든 CLI 도구",
        epilog="예제: %(prog)s sync ./source ./target --delete --verbose",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    subparsers = parser.add_subparsers(
        title="명령어", description="사용 가능한 명령어", dest="command"
    )

    # --- scan 서브커맨드 ---
    scan_parser = subparsers.add_parser("scan", help="디렉토리를 스캔합니다")
    scan_parser.add_argument("directory", help="스캔할 디렉토리 경로")
    scan_parser.add_argument("-o", "--output", help="결과를 JSON 파일로 저장")
    scan_parser.add_argument("-v", "--verbose", action="store_true", help="상세 출력")
    scan_parser.set_defaults(func=cmd_scan)

    # --- compare 서브커맨드 ---
    compare_parser = subparsers.add_parser("compare", help="두 디렉토리를 비교합니다")
    compare_parser.add_argument("source", help="소스 디렉토리")
    compare_parser.add_argument("target", help="대상 디렉토리")
    compare_parser.add_argument("-v", "--verbose", action="store_true", help="상세 출력")
    compare_parser.set_defaults(func=cmd_compare)

    # --- sync 서브커맨드 ---
    sync_parser = subparsers.add_parser("sync", help="디렉토리를 동기화합니다")
    sync_parser.add_argument("source", help="소스 디렉토리")
    sync_parser.add_argument("target", help="대상 디렉토리")
    sync_parser.add_argument("-d", "--delete", action="store_true",
                             help="소스에 없는 대상 파일을 삭제")
    sync_parser.add_argument("-n", "--dry-run", action="store_true",
                             help="시뮬레이션만 수행")
    sync_parser.add_argument("-v", "--verbose", action="store_true", help="상세 출력")
    sync_parser.add_argument("--log-file", help="로그 파일 경로")
    sync_parser.set_defaults(func=cmd_sync)

    return parser
```

### 사용 방법

완성된 CLI 도구의 사용법을 정리합니다.

**디렉토리 스캔:**

```bash
# 기본 스캔
$ python ex28_06_sync_cli.py scan ./my_folder

# 상세 출력 (해시값 포함)
$ python ex28_06_sync_cli.py scan ./my_folder --verbose

# 결과를 JSON으로 저장
$ python ex28_06_sync_cli.py scan ./my_folder --output scan_result.json
```

**두 디렉토리 비교:**

```bash
$ python ex28_06_sync_cli.py compare ./source ./target
```

**동기화 실행:**

```bash
# 시뮬레이션 (실제 변경 없음)
$ python ex28_06_sync_cli.py sync ./source ./target --delete --dry-run

# 실제 동기화 (삭제 포함, 로그 파일 저장)
$ python ex28_06_sync_cli.py sync ./source ./target --delete --log-file sync.log --verbose
```

**실행:**

```bash
$ python examples/python/chapter06/ex28_06_sync_cli.py
```

**결과 (데모 모드에서 발췌):**

```
============================================================
  파일 동기화 CLI 도구 데모
============================================================

------------------------------------------------------------
  데모 1: scan 명령어
  $ file_sync scan /tmp/.../source --verbose
------------------------------------------------------------

  [INFO   ] 디렉토리 스캔: /tmp/.../source
  [DEBUG  ]   README.md (25B) -> a4185a52925fe576...
  [DEBUG  ]   config.json (19B) -> e0e77b70ca77d0be...
  [DEBUG  ]   docs/guide.md (12B) -> af4b2b835604bdfe...
  [DEBUG  ]   src/main.py (16B) -> d578dc9205d09715...
  [DEBUG  ]   src/utils.py (19B) -> 908d11b98ea0991c...
  [INFO   ] 총 5개 파일, 91 바이트

------------------------------------------------------------
  데모 2: compare 명령어
  $ file_sync compare /tmp/.../source /tmp/.../target
------------------------------------------------------------

  [INFO   ] 소스: /tmp/.../source
  [INFO   ] 대상: /tmp/.../target
  [INFO   ] 추가 필요 (3개):
  [INFO   ]   + config.json
  [INFO   ]   + docs/guide.md
  [INFO   ]   + src/utils.py
  [INFO   ] 수정 필요 (1개):
  [INFO   ]   ~ README.md
  [INFO   ] 삭제 대상 (1개):
  [INFO   ]   - old_data.txt
  [INFO   ] 요약: 추가 3 | 수정 1 | 삭제 1 | 동일 1

------------------------------------------------------------
  데모 3: sync --dry-run (시뮬레이션)
------------------------------------------------------------

  [INFO   ] ==================================================
  [INFO   ] 파일 동기화 시작
  [INFO   ]   삭제 모드: 활성
  [INFO   ]   시뮬레이션: 예
  [INFO   ] [시뮬레이션] [수정] README.md
  [INFO   ] [시뮬레이션] [추가] config.json
  [INFO   ] [시뮬레이션] [추가] docs/guide.md
  [INFO   ] [시뮬레이션] [추가] src/utils.py
  [INFO   ] [시뮬레이션] [삭제] old_data.txt
  [INFO   ] 동기화 완료
  [INFO   ]   복사: 4 | 삭제: 1 | 건너뜀: 1 | 오류: 0
  [INFO   ] ==================================================

------------------------------------------------------------
  데모 5: 도움말 (--help)
------------------------------------------------------------

usage: file_sync [-h] [--version] {scan,compare,sync} ...

파일 동기화 도구 - 바이브 코딩으로 만든 CLI 도구

명령어:
  사용 가능한 명령어

  {scan,compare,sync}
    scan               디렉토리를 스캔합니다
    compare            두 디렉토리를 비교합니다
    sync               디렉토리를 동기화합니다

예제: file_sync sync ./source ./target --delete --verbose
```

> **Tip:** `argparse`의 `epilog` 인자에 사용 예제를 넣으면 `--help` 출력 맨 아래에 표시됩니다. 사용자가 도구의 사용법을 빠르게 이해할 수 있도록 대표적인 실행 예제를 포함하세요.

---

## 28.8 전체 아키텍처 정리

6단계에 걸쳐 만든 파일 동기화 도구의 전체 구조를 정리해 봅시다.

### 모듈 구성도

```
파일 동기화 도구
├── [기반] 파일 해시 계산 (hashlib)
│   ├── calculate_hash()        - 개별 파일 해시
│   ├── compare_files_by_hash() - 두 파일 비교
│   └── get_directory_hashes()  - 디렉토리 전체 해시
│
├── [감지] 변경 파일 감지
│   ├── FileInfo (dataclass)    - 파일 메타데이터
│   ├── ChangeReport (dataclass)- 변경 사항 보고서
│   ├── scan_directory()        - 디렉토리 스캔
│   └── detect_changes()        - 변경 감지
│
├── [실행] 동기화 로직
│   ├── SyncResult (dataclass)  - 동기화 결과
│   ├── sync_directories()      - 단방향 동기화
│   └── _cleanup_empty_dirs()   - 빈 폴더 정리
│
├── [고급] 충돌 처리
│   ├── ConflictStrategy (Enum) - 5가지 해결 전략
│   ├── ConflictInfo (dataclass)- 충돌 정보
│   ├── detect_conflicts()      - 충돌 감지
│   ├── resolve_conflict()      - 충돌 해결
│   └── save_conflict_report()  - 보고서 저장
│
├── [운영] 로그 기록
│   └── SyncLogger (class)      - 콘솔+파일 이중 로깅
│       ├── start_sync() / end_sync()
│       ├── log_copy() / log_delete()
│       ├── log_skip() / log_conflict()
│       └── log_error() / log_scan()
│
└── [인터페이스] CLI
    ├── cmd_scan()              - scan 서브커맨드
    ├── cmd_compare()           - compare 서브커맨드
    ├── cmd_sync()              - sync 서브커맨드
    └── create_parser()         - argparse 설정
```

### 사용된 주요 기술 요약

| 기술 | 모듈/클래스 | 용도 |
|------|------------|------|
| **해시 계산** | `hashlib` | 파일 변경 감지의 핵심 |
| **파일 작업** | `os`, `shutil`, `pathlib` | 경로 처리, 파일 복사/삭제 |
| **데이터 구조** | `dataclasses` | FileInfo, SyncResult 등 |
| **열거형** | `enum.Enum` | 충돌 해결 전략 정의 |
| **직렬화** | `json` | 보고서 저장, 스캔 결과 내보내기 |
| **로깅** | `logging` | 콘솔+파일 이중 기록 |
| **CLI** | `argparse` | 서브커맨드, 옵션 처리 |
| **시간** | `time`, `datetime` | 수정 시간 비교, 타임스탬프 |

---

## 28.9 확장 아이디어

이 프로젝트를 더 발전시키고 싶다면, AI에게 다음과 같이 요청해 보세요:

### 1. 실시간 감시 모드

```
watchdog 패키지를 사용해서 소스 디렉토리를 실시간으로 감시하고,
파일이 변경될 때마다 자동으로 동기화하는 기능을 추가해줘.
```

### 2. 네트워크 동기화

```
소스 디렉토리가 원격 서버에 있는 경우를 지원해줘.
SSH/SFTP를 통해 원격 파일을 동기화하는 기능이 필요해.
```

### 3. 증분 동기화

```
마지막 동기화 시점의 상태를 JSON으로 저장하고,
다음 동기화 시에는 변경된 파일만 빠르게 처리하는
증분 동기화 기능을 추가해줘.
```

### 4. 필터 규칙

```
.gitignore처럼 특정 패턴의 파일을 동기화에서 제외하는
필터 기능을 추가해줘. 예를 들어 *.pyc, __pycache__,
.DS_Store 같은 파일을 자동으로 건너뛰게 해줘.
```

### 5. 압축 전송

```
큰 파일을 동기화할 때 gzip으로 압축한 뒤 복사하고,
대상에서 압축을 풀어서 저장하는 기능을 추가해줘.
네트워크 전송 시 대역폭을 절약할 수 있어.
```

> **Tip:** 확장 기능을 추가할 때도 한번에 모두 요청하지 말고, 하나씩 추가하면서 동작을 확인하세요. 바이브 코딩의 핵심은 **작은 단위로 반복적으로 발전시키는 것**입니다.

---

## 28.10 정리

이 장에서는 파이썬 표준 라이브러리만으로 완전한 파일 동기화 도구를 만들었습니다. 6단계에 걸친 점진적 개발 과정을 통해, 작은 기능에서 출발하여 실용적인 도구로 성장시키는 바이브 코딩의 핵심 패턴을 경험했습니다.

### 핵심 요약

| 단계 | 학습 내용 | 핵심 기술 |
|------|----------|----------|
| **1. 파일 해시** | 파일의 "지문"으로 동일 여부 판단 | `hashlib`, 청크 단위 읽기 |
| **2. 변경 감지** | 두 디렉토리 사이의 차이점 분석 | 집합 연산, `dataclasses` |
| **3. 동기화** | 실제 파일 복사/삭제 수행 | `shutil.copy2()`, dry-run |
| **4. 충돌 처리** | 양쪽 변경 시 해결 전략 적용 | `Enum`, 백업 메커니즘 |
| **5. 로그 기록** | 작업 이력 추적과 디버깅 | `logging`, 이중 핸들러 |
| **6. CLI** | 터미널에서 사용할 수 있는 인터페이스 | `argparse`, 서브커맨드 |

### 바이브 코딩 교훈

이 프로젝트를 통해 배운 바이브 코딩 패턴을 정리합니다:

1. **단계적 확장**: 한번에 모든 기능을 요청하지 않고, 기반부터 차근차근 쌓아 올립니다.
2. **구체적 프롬프트**: 각 단계에서 입력/출력/제약 조건을 명확하게 전달합니다.
3. **검증 후 진행**: 각 단계의 결과를 실행하여 확인한 뒤 다음 단계로 넘어갑니다.
4. **데이터 구조 먼저**: `dataclass`와 `Enum`으로 데이터 구조를 먼저 정의하면 코드가 깔끔해집니다.
5. **안전 장치**: `dry_run` 모드, 백업 기능, 로깅 등 실수를 방지하는 장치를 반드시 포함합니다.

> **Note:** 이 프로젝트에서 사용한 모든 모듈(`hashlib`, `os`, `shutil`, `argparse`, `logging`, `json`, `dataclasses`, `enum`, `pathlib`)은 파이썬 표준 라이브러리입니다. `pip install` 없이 어떤 환경에서도 바로 실행할 수 있습니다. 표준 라이브러리의 힘을 기억하세요!

---

### 연습 문제

1. **해시 알고리즘 추가**: `calculate_hash()` 함수에 SHA512 알고리즘을 추가해 보세요.

2. **필터 규칙 구현**: `sync_directories()` 함수에 `exclude_patterns` 인자를 추가하여, `*.pyc`, `__pycache__` 같은 패턴의 파일을 동기화에서 제외하도록 수정해 보세요.

3. **양방향 동기화**: 단방향 동기화(`sync_directories`)를 확장하여, 양쪽의 변경 사항을 모두 반영하고 충돌이 발생하면 사용자에게 선택을 요청하는 양방향 동기화 함수를 만들어 보세요.

4. **진행률 표시**: 파일이 많을 때 진행률을 표시하는 기능을 추가해 보세요. `현재/전체 (퍼센트%)` 형식으로 콘솔에 출력되도록 합니다.

5. **상태 저장**: 동기화 완료 후 현재 상태(모든 파일의 해시)를 JSON 파일로 저장하고, 다음 동기화 시 이 파일을 읽어서 변경된 파일만 빠르게 감지하는 증분 동기화를 구현해 보세요.

---

> 다음 장에서는 **프로젝트 5: 개인 대시보드**를 만들어 봅니다. 날씨, 일정, 메모, 알림을 하나의 화면에서 관리하는 개인 생산성 도구를 바이브 코딩으로 완성합니다.
