#!/usr/bin/env python3
"""
예제 29-03: 메모 기능
- 텍스트 파일 기반 메모 저장, 검색, 삭제
- 태그(#) 지원으로 메모 분류
- /tmp/ 디렉토리에 메모 저장
"""

import os
import json
from datetime import datetime
from pathlib import Path


# ── 설정 ─────────────────────────────────────────────────────────────────

MEMO_DIR = Path("/tmp/personal_assistant_memos")
MEMO_INDEX_FILE = MEMO_DIR / "_index.json"


# ── 메모 관리 클래스 ─────────────────────────────────────────────────────

class MemoManager:
    """텍스트 파일 기반 메모 관리 클래스"""

    def __init__(self, memo_dir=MEMO_DIR):
        """
        메모 관리자를 초기화합니다.

        Args:
            memo_dir: 메모 파일을 저장할 디렉토리 경로
        """
        self.memo_dir = Path(memo_dir)
        self.memo_dir.mkdir(parents=True, exist_ok=True)
        self.index = self._load_index()

    def _load_index(self):
        """메모 인덱스 파일을 불러옵니다."""
        index_file = self.memo_dir / "_index.json"
        if index_file.exists():
            try:
                with open(index_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"memos": [], "next_id": 1}
        return {"memos": [], "next_id": 1}

    def _save_index(self):
        """메모 인덱스 파일을 저장합니다."""
        index_file = self.memo_dir / "_index.json"
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)

    def _extract_tags(self, content):
        """메모 내용에서 #태그를 추출합니다."""
        tags = []
        for word in content.split():
            if word.startswith("#") and len(word) > 1:
                # '#' 제거하고 태그만 저장
                tag = word.lstrip("#").rstrip(".,!?;:")
                if tag:
                    tags.append(tag)
        return list(set(tags))  # 중복 제거

    # ── 메모 CRUD ────────────────────────────────────────────

    def create(self, title, content, tags=None):
        """
        새 메모를 생성합니다.

        Args:
            title: 메모 제목
            content: 메모 내용
            tags: 태그 목록 (선택, None이면 내용에서 자동 추출)

        Returns:
            dict: 생성된 메모 메타데이터
        """
        memo_id = self.index["next_id"]
        self.index["next_id"] += 1

        # 내용에서 태그 자동 추출 (명시적 태그가 없는 경우)
        if tags is None:
            tags = self._extract_tags(content)

        # 파일명 생성 (ID_제목.txt)
        safe_title = title.replace(" ", "_").replace("/", "_")[:30]
        filename = f"memo_{memo_id:04d}_{safe_title}.txt"
        filepath = self.memo_dir / filename

        # 메모 파일 작성
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        memo_text = f"제목: {title}\n"
        memo_text += f"작성일: {created_at}\n"
        if tags:
            memo_text += f"태그: {', '.join('#' + t for t in tags)}\n"
        memo_text += f"{'-' * 40}\n"
        memo_text += content
        memo_text += "\n"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(memo_text)

        # 인덱스에 메타데이터 추가
        meta = {
            "id": memo_id,
            "title": title,
            "filename": filename,
            "tags": tags,
            "created_at": created_at,
            "updated_at": created_at,
            "char_count": len(content),
        }
        self.index["memos"].append(meta)
        self._save_index()

        print(f"  [메모 저장] #{memo_id} '{title}' ({len(content)}자)")
        return meta

    def read(self, memo_id):
        """
        메모를 읽어옵니다.

        Args:
            memo_id: 메모 ID

        Returns:
            str 또는 None: 메모 내용
        """
        meta = self._find_meta(memo_id)
        if not meta:
            print(f"  [오류] 메모 #{memo_id}을(를) 찾을 수 없습니다.")
            return None

        filepath = self.memo_dir / meta["filename"]
        if not filepath.exists():
            print(f"  [오류] 메모 파일이 존재하지 않습니다: {filepath}")
            return None

        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    def update(self, memo_id, new_content=None, new_title=None):
        """
        메모를 수정합니다.

        Args:
            memo_id: 수정할 메모 ID
            new_content: 새로운 내용 (None이면 변경 안 함)
            new_title: 새로운 제목 (None이면 변경 안 함)

        Returns:
            bool: 수정 성공 여부
        """
        meta = self._find_meta(memo_id)
        if not meta:
            print(f"  [오류] 메모 #{memo_id}을(를) 찾을 수 없습니다.")
            return False

        # 메타데이터 업데이트
        if new_title:
            meta["title"] = new_title
        if new_content:
            meta["tags"] = self._extract_tags(new_content)
            meta["char_count"] = len(new_content)

        meta["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 파일 다시 작성
        filepath = self.memo_dir / meta["filename"]
        title = meta["title"]
        tags = meta["tags"]
        content = new_content or self._read_content_only(filepath)

        memo_text = f"제목: {title}\n"
        memo_text += f"작성일: {meta['created_at']}\n"
        memo_text += f"수정일: {meta['updated_at']}\n"
        if tags:
            memo_text += f"태그: {', '.join('#' + t for t in tags)}\n"
        memo_text += f"{'-' * 40}\n"
        memo_text += content
        memo_text += "\n"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(memo_text)

        self._save_index()
        print(f"  [메모 수정] #{memo_id} '{title}' 수정 완료")
        return True

    def delete(self, memo_id):
        """
        메모를 삭제합니다.

        Args:
            memo_id: 삭제할 메모 ID

        Returns:
            bool: 삭제 성공 여부
        """
        meta = self._find_meta(memo_id)
        if not meta:
            print(f"  [오류] 메모 #{memo_id}을(를) 찾을 수 없습니다.")
            return False

        # 파일 삭제
        filepath = self.memo_dir / meta["filename"]
        if filepath.exists():
            os.remove(filepath)

        # 인덱스에서 제거
        self.index["memos"] = [m for m in self.index["memos"] if m["id"] != memo_id]
        self._save_index()

        print(f"  [메모 삭제] #{memo_id} '{meta['title']}' 삭제 완료")
        return True

    # ── 검색 기능 ────────────────────────────────────────────

    def search(self, keyword):
        """
        키워드로 메모를 검색합니다 (제목 + 내용).

        Args:
            keyword: 검색어

        Returns:
            list: 일치하는 메모 메타데이터 목록
        """
        keyword_lower = keyword.lower()
        results = []

        for meta in self.index["memos"]:
            # 제목 검색
            if keyword_lower in meta["title"].lower():
                results.append(meta)
                continue

            # 내용 검색
            filepath = self.memo_dir / meta["filename"]
            if filepath.exists():
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                if keyword_lower in content.lower():
                    results.append(meta)

        return results

    def search_by_tag(self, tag):
        """
        태그로 메모를 검색합니다.

        Args:
            tag: 태그 이름 (# 없이)

        Returns:
            list: 태그가 일치하는 메모 메타데이터 목록
        """
        tag_lower = tag.lower().lstrip("#")
        return [
            m for m in self.index["memos"]
            if tag_lower in [t.lower() for t in m.get("tags", [])]
        ]

    def list_all(self):
        """모든 메모 목록을 반환합니다."""
        return sorted(self.index["memos"], key=lambda m: m["created_at"], reverse=True)

    def list_tags(self):
        """사용된 모든 태그를 반환합니다."""
        all_tags = {}
        for meta in self.index["memos"]:
            for tag in meta.get("tags", []):
                all_tags[tag] = all_tags.get(tag, 0) + 1
        return sorted(all_tags.items(), key=lambda x: x[1], reverse=True)

    # ── 내부 헬퍼 함수 ───────────────────────────────────────

    def _find_meta(self, memo_id):
        """ID로 메모 메타데이터를 찾습니다."""
        for m in self.index["memos"]:
            if m["id"] == memo_id:
                return m
        return None

    def _read_content_only(self, filepath):
        """메모 파일에서 헤더를 제외한 본문만 추출합니다."""
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 구분선('-' * 40) 이후가 본문
        content_start = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("-" * 10):
                content_start = i + 1
                break

        return "".join(lines[content_start:]).strip()


# ── 출력 함수들 ──────────────────────────────────────────────────────────

def display_memo_list(memos, title="메모 목록"):
    """메모 목록을 보기 좋게 출력합니다."""
    print()
    print(f"  ── {title} ({len(memos)}건) ──")

    if not memos:
        print("  등록된 메모가 없습니다.")
        print()
        return

    for m in memos:
        tags_str = " ".join(f"#{t}" for t in m.get("tags", []))
        print(f"  [{m['id']:>3}] {m['title']}")
        print(f"       {m['created_at'][:10]} | {m['char_count']}자 | {tags_str}")
    print()


def display_memo_content(content, meta=None):
    """메모 전체 내용을 출력합니다."""
    if content is None:
        return

    print()
    print("  " + "=" * 45)
    if meta:
        print(f"  메모 #{meta['id']}: {meta['title']}")
    print("  " + "=" * 45)
    for line in content.split("\n"):
        print(f"  {line}")
    print("  " + "=" * 45)
    print()


def display_tag_cloud(tags):
    """태그 목록을 출력합니다."""
    print()
    print("  ── 태그 목록 ──")
    if not tags:
        print("  사용된 태그가 없습니다.")
    else:
        for tag, count in tags:
            bar = "*" * count
            print(f"  #{tag:<10} {bar} ({count}개)")
    print()


# ── 메인 데모 ────────────────────────────────────────────────────────────

def main():
    """메모 기능 데모를 실행합니다."""
    print("=" * 55)
    print("  개인 비서 - 메모 기능 데모")
    print("=" * 55)

    # 기존 데모 데이터 초기화
    import shutil
    if MEMO_DIR.exists():
        shutil.rmtree(MEMO_DIR)

    manager = MemoManager()

    # ── 1. 메모 생성 ──
    print("\n--- [1단계] 메모 생성 ---")

    m1 = manager.create(
        "프로젝트 아이디어",
        "AI를 활용한 코드 리뷰 자동화 도구를 만들어보자.\n"
        "주요 기능:\n"
        "- Git diff 분석\n"
        "- 코드 품질 점검\n"
        "- 개선 사항 제안\n\n"
        "#프로젝트 #AI #코드리뷰"
    )

    m2 = manager.create(
        "Python 학습 노트",
        "오늘 배운 내용:\n"
        "1. 데코레이터 패턴\n"
        "2. 컨텍스트 매니저 (with 문)\n"
        "3. 제너레이터 함수\n\n"
        "내일은 asyncio를 공부할 예정\n\n"
        "#파이썬 #학습 #프로그래밍"
    )

    m3 = manager.create(
        "회의 메모 - 2분기 계획",
        "참석자: 김팀장, 이대리, 박사원\n\n"
        "논의 사항:\n"
        "- 신규 프로젝트 일정 확정 (3월 시작)\n"
        "- 인력 충원 계획 (2명)\n"
        "- 기술 스택 결정: Python + FastAPI\n\n"
        "결정 사항:\n"
        "- 다음 주 금요일까지 상세 계획서 작성\n"
        "- 매주 월요일 진행 상황 공유\n\n"
        "#회의 #업무 #계획"
    )

    m4 = manager.create(
        "읽을 책 목록",
        "1. 클린 코드 (로버트 마틴)\n"
        "2. 리팩터링 (마틴 파울러)\n"
        "3. 프로그래머의 뇌 (펠리너 헤르만스)\n"
        "4. 함께 자라기 (김창준)\n\n"
        "#독서 #학습"
    )

    m5 = manager.create(
        "맛집 기록 - 강남",
        "강남역 근처 점심 맛집:\n"
        "- 설빙: 팥빙수 맛있음\n"
        "- 명동교자: 칼국수 추천\n"
        "- 본죽: 전복죽 추천\n\n"
        "#맛집 #강남"
    )

    # ── 2. 메모 목록 조회 ──
    print("\n--- [2단계] 전체 메모 목록 ---")
    all_memos = manager.list_all()
    display_memo_list(all_memos)

    # ── 3. 메모 읽기 ──
    print("\n--- [3단계] 메모 읽기 ---")
    content = manager.read(m1["id"])
    display_memo_content(content, m1)

    # ── 4. 키워드 검색 ──
    print("\n--- [4단계] 키워드 검색 ---")

    print("  검색어: 'Python'")
    results = manager.search("Python")
    display_memo_list(results, "'Python' 검색 결과")

    print("  검색어: '계획'")
    results = manager.search("계획")
    display_memo_list(results, "'계획' 검색 결과")

    # ── 5. 태그 검색 ──
    print("\n--- [5단계] 태그 검색 ---")
    tagged = manager.search_by_tag("학습")
    display_memo_list(tagged, "#학습 태그 검색 결과")

    # ── 6. 태그 클라우드 ──
    print("\n--- [6단계] 태그 클라우드 ---")
    tags = manager.list_tags()
    display_tag_cloud(tags)

    # ── 7. 메모 수정 ──
    print("\n--- [7단계] 메모 수정 ---")
    manager.update(
        m4["id"],
        new_content=(
            "1. 클린 코드 (로버트 마틴) - 읽는 중\n"
            "2. 리팩터링 (마틴 파울러)\n"
            "3. 프로그래머의 뇌 (펠리너 헤르만스)\n"
            "4. 함께 자라기 (김창준)\n"
            "5. 바이브 코딩 입문 (추가!)\n\n"
            "#독서 #학습 #바이브코딩"
        )
    )

    updated_content = manager.read(m4["id"])
    display_memo_content(updated_content, manager._find_meta(m4["id"]))

    # ── 8. 메모 삭제 ──
    print("\n--- [8단계] 메모 삭제 ---")
    manager.delete(m5["id"])

    # 최종 목록 확인
    print("\n--- [최종] 남은 메모 목록 ---")
    remaining = manager.list_all()
    display_memo_list(remaining, "최종 메모 목록")

    # 통계 정보
    print("  ── 메모 통계 ──")
    total_chars = sum(m["char_count"] for m in remaining)
    print(f"  총 메모 수: {len(remaining)}개")
    print(f"  총 글자 수: {total_chars}자")
    print(f"  저장 위치: {MEMO_DIR}")
    print()

    # 실제 파일 목록 표시
    print("  ── 저장된 파일 목록 ──")
    for f in sorted(MEMO_DIR.iterdir()):
        if f.name != "_index.json":
            print(f"  - {f.name} ({f.stat().st_size} bytes)")
    print()
    print("  메모 기능 데모가 완료되었습니다!")


if __name__ == "__main__":
    main()
