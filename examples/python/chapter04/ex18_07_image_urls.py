"""
예제 18-07: 이미지 URL 수집
HTML에서 모든 <img> 태그를 찾아 이미지 URL(src)과
대체 텍스트(alt)를 추출합니다.
"""

from html.parser import HTMLParser
from urllib.parse import urljoin

# 이미지가 포함된 HTML
HTML_CONTENT = """<!DOCTYPE html>
<html>
<body>
    <header>
        <img src="/images/logo.png" alt="사이트 로고" width="200">
    </header>

    <main>
        <h1>바이브 코딩 갤러리</h1>

        <section class="gallery">
            <figure>
                <img src="/images/vibe-coding-intro.jpg" alt="바이브 코딩 소개 이미지">
                <figcaption>바이브 코딩의 기본 개념</figcaption>
            </figure>

            <figure>
                <img src="https://cdn.example.com/photos/ai-assistant.png" alt="AI 어시스턴트 화면">
                <figcaption>AI 어시스턴트와 대화하는 모습</figcaption>
            </figure>

            <figure>
                <img src="/images/terminal-screenshot.png" alt="터미널 스크린샷" width="800" height="600">
                <figcaption>CLI에서 코딩하는 화면</figcaption>
            </figure>

            <figure>
                <img src="https://cdn.example.com/photos/code-result.gif" alt="코드 실행 결과">
                <figcaption>실시간 코드 생성 과정</figcaption>
            </figure>

            <figure>
                <img src="/images/project-complete.webp" alt="프로젝트 완성">
                <figcaption>완성된 프로젝트</figcaption>
            </figure>
        </section>
    </main>
</body>
</html>"""

BASE_URL = "https://www.vibecoding-example.com"


class ImageExtractor(HTMLParser):
    """HTML에서 모든 이미지 정보를 추출하는 파서"""

    def __init__(self, base_url=""):
        super().__init__()
        self.base_url = base_url
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            attrs_dict = dict(attrs)
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "(대체 텍스트 없음)")
            width = attrs_dict.get("width", "")
            height = attrs_dict.get("height", "")

            # 상대 경로를 절대 경로로 변환
            if self.base_url and not src.startswith(("http://", "https://")):
                full_url = urljoin(self.base_url, src)
            else:
                full_url = src

            self.images.append({
                "src": src,
                "full_url": full_url,
                "alt": alt,
                "width": width,
                "height": height,
            })


# 실행
print("=" * 50)
print("예제 18-07: 이미지 URL 수집")
print("=" * 50)

extractor = ImageExtractor(base_url=BASE_URL)
extractor.feed(HTML_CONTENT)

print(f"\n총 {len(extractor.images)}개의 이미지를 발견했습니다:\n")

for i, img in enumerate(extractor.images, 1):
    print(f"이미지 {i}:")
    print(f"  원본 경로: {img['src']}")
    print(f"  절대 URL:  {img['full_url']}")
    print(f"  대체 텍스트: {img['alt']}")
    if img["width"] or img["height"]:
        print(f"  크기: {img['width']}x{img['height']}")
    print()

# 확장자별 분류
print("--- 확장자별 분류 ---\n")
extensions = {}
for img in extractor.images:
    src = img["src"]
    ext = src.rsplit(".", 1)[-1] if "." in src else "알 수 없음"
    extensions.setdefault(ext, []).append(img["alt"])

for ext, images in sorted(extensions.items()):
    print(f".{ext} ({len(images)}개):")
    for alt in images:
        print(f"  - {alt}")

# 외부/내부 이미지 분류
print("\n--- 호스팅 위치별 분류 ---\n")
internal = [img for img in extractor.images
            if not img["src"].startswith("http")]
external = [img for img in extractor.images
            if img["src"].startswith("http")]

print(f"내부 이미지 ({len(internal)}개):")
for img in internal:
    print(f"  - {img['alt']}: {img['full_url']}")

print(f"\n외부 이미지 ({len(external)}개):")
for img in external:
    print(f"  - {img['alt']}: {img['src']}")
