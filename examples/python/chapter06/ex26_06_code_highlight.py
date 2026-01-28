"""
예제 26-06: 코드 하이라이팅

코드 블록을 HTML <pre><code> 태그로 변환하며,
키워드, 문자열, 주석 등에 색상 스타일을 적용합니다.
표준 라이브러리(re, html)만 사용합니다.
"""

import re
import html as html_module
import os


# 언어별 키워드 정의
LANGUAGE_KEYWORDS = {
    "python": {
        "keywords": [
            "def", "class", "if", "elif", "else", "for", "while",
            "return", "import", "from", "as", "try", "except",
            "finally", "with", "yield", "lambda", "pass", "break",
            "continue", "raise", "and", "or", "not", "in", "is",
            "True", "False", "None", "async", "await", "print",
        ],
        "comment": r"#.*$",
        "string": r'(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|f"(?:[^"\\]|\\.)*"|f\'(?:[^\'\\]|\\.)*\')',
        "number": r"\b\d+(?:\.\d+)?\b",
        "decorator": r"@\w+",
        "builtin": ["len", "range", "str", "int", "float", "list", "dict", "set", "tuple", "type", "isinstance"],
    },
    "javascript": {
        "keywords": [
            "function", "const", "let", "var", "if", "else", "for",
            "while", "return", "class", "import", "export", "from",
            "new", "this", "try", "catch", "finally", "throw",
            "async", "await", "true", "false", "null", "undefined",
            "typeof", "instanceof", "switch", "case", "default",
            "break", "continue", "of", "in",
        ],
        "comment": r"//.*$",
        "string": r'(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|`(?:[^`\\]|\\.)*`)',
        "number": r"\b\d+(?:\.\d+)?\b",
        "builtin": ["console", "document", "window", "Array", "Object", "Promise", "Math", "JSON"],
    },
    "bash": {
        "keywords": [
            "if", "then", "else", "fi", "for", "do", "done",
            "while", "case", "esac", "function", "return", "exit",
            "echo", "read", "local", "export", "source", "in",
        ],
        "comment": r"#.*$",
        "string": r'(?:"(?:[^"\\]|\\.)*"|\'[^\']*\')',
        "number": r"\b\d+\b",
        "builtin": ["cd", "ls", "pwd", "mkdir", "rm", "cp", "mv", "cat", "grep", "find", "pip", "python", "node"],
    },
}


def highlight_code(code: str, language: str = "text") -> str:
    """코드에 구문 하이라이팅을 적용하여 HTML을 생성합니다.

    Args:
        code: 소스 코드 문자열
        language: 프로그래밍 언어 이름

    Returns:
        하이라이팅이 적용된 HTML 문자열
    """
    # HTML 특수 문자 이스케이프
    escaped = html_module.escape(code)

    # 지원하지 않는 언어는 이스케이프만 적용
    if language not in LANGUAGE_KEYWORDS:
        return _wrap_code_block(escaped, language)

    lang_config = LANGUAGE_KEYWORDS[language]
    result = escaped

    # 1단계: 문자열 보호 (플레이스홀더로 임시 대체)
    string_placeholders = {}
    counter = [0]

    def replace_string(match):
        placeholder = f"__STR_{counter[0]}__"
        string_placeholders[placeholder] = f'<span class="hl-string">{match.group(0)}</span>'
        counter[0] += 1
        return placeholder

    if "string" in lang_config:
        result = re.sub(lang_config["string"], replace_string, result)

    # 2단계: 주석 하이라이팅 (플레이스홀더로 보호)
    comment_placeholders = {}

    def replace_comment(match):
        placeholder = f"__CMT_{counter[0]}__"
        comment_placeholders[placeholder] = f'<span class="hl-comment">{match.group(0)}</span>'
        counter[0] += 1
        return placeholder

    if "comment" in lang_config:
        result = re.sub(lang_config["comment"], replace_comment, result, flags=re.MULTILINE)

    # 3단계: 데코레이터 (Python)
    if "decorator" in lang_config:
        result = re.sub(
            lang_config["decorator"],
            r'<span class="hl-decorator">\g<0></span>',
            result
        )

    # 4단계: 숫자 하이라이팅
    if "number" in lang_config:
        result = re.sub(
            lang_config["number"],
            r'<span class="hl-number">\g<0></span>',
            result
        )

    # 5단계: 빌트인 함수 하이라이팅
    if "builtin" in lang_config:
        for builtin in lang_config["builtin"]:
            pattern = r"\b" + re.escape(builtin) + r"\b"
            result = re.sub(
                pattern,
                f'<span class="hl-builtin">{builtin}</span>',
                result
            )

    # 6단계: 키워드 하이라이팅
    for keyword in lang_config["keywords"]:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        result = re.sub(
            pattern,
            f'<span class="hl-keyword">{keyword}</span>',
            result
        )

    # 7단계: 플레이스홀더 복원 (주석 -> 문자열 순)
    for placeholder, replacement in comment_placeholders.items():
        result = result.replace(placeholder, replacement)
    for placeholder, replacement in string_placeholders.items():
        result = result.replace(placeholder, replacement)

    return _wrap_code_block(result, language)


def _wrap_code_block(code_html: str, language: str) -> str:
    """코드 HTML을 pre/code 태그로 감쌉니다.

    Args:
        code_html: 코드 HTML
        language: 언어 이름

    Returns:
        완성된 코드 블록 HTML
    """
    lang_label = language if language != "text" else ""
    header = ""
    if lang_label:
        header = f'<div class="code-header"><span class="code-lang">{lang_label}</span></div>\n'

    return (
        f'<div class="code-block">\n'
        f'{header}'
        f'<pre><code class="language-{language}">{code_html}</code></pre>\n'
        f'</div>'
    )


def get_highlight_css() -> str:
    """코드 하이라이팅용 CSS 스타일을 반환합니다.

    Returns:
        CSS 문자열
    """
    return """\
/* 코드 하이라이팅 스타일 (다크 테마) */
.code-block {
    margin: 16px 0;
    border-radius: 8px;
    overflow: hidden;
    background: #1e1e1e;
}
.code-header {
    background: #2d2d2d;
    padding: 4px 12px;
    font-size: 12px;
    color: #888;
    border-bottom: 1px solid #333;
}
.code-lang {
    text-transform: uppercase;
    letter-spacing: 1px;
}
pre {
    margin: 0;
    padding: 16px;
    overflow-x: auto;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 14px;
    line-height: 1.5;
}
pre code {
    color: #d4d4d4;
}
.hl-keyword   { color: #569cd6; font-weight: bold; }
.hl-string    { color: #ce9178; }
.hl-comment   { color: #6a9955; font-style: italic; }
.hl-number    { color: #b5cea8; }
.hl-builtin   { color: #dcdcaa; }
.hl-decorator { color: #c586c0; }
"""


# 데모용 코드 샘플
SAMPLES = {
    "python": '''\
# 바이브 코딩으로 만든 인사 프로그램
def greet(name, language="ko"):
    """다국어 인사 함수"""
    greetings = {
        "ko": f"안녕하세요, {name}님!",
        "en": f"Hello, {name}!",
    }
    return greetings.get(language, greetings["ko"])

# 실행
for i in range(3):
    message = greet("바이브 코더")
    print(message)  # True가 아닌 문자열 출력
''',
    "javascript": '''\
// 블로그 글 로더
const loadPost = async (slug) => {
    const url = `/api/posts/${slug}`;
    try {
        const response = await fetch(url);
        const data = response.json();
        console.log("글 로드 완료:", data.title);
        return data;
    } catch (error) {
        console.log("오류 발생:", error);
        return null;
    }
};

const posts = ["hello-world", "vibe-coding"];
''',
    "bash": '''\
#!/bin/bash
# 블로그 빌드 스크립트

echo "블로그 빌드를 시작합니다..."

# 출력 디렉토리 생성
mkdir -p output/posts
mkdir -p output/static

# 마크다운 파일 변환
for file in content/posts/*.md; do
    echo "변환 중: $file"
    python convert.py "$file"
done

echo "빌드가 완료되었습니다!"
exit 0
''',
}


if __name__ == "__main__":
    print("=" * 60)
    print("  코드 하이라이팅 데모")
    print("=" * 60)
    print()

    all_code_blocks = []

    for language, code in SAMPLES.items():
        print(f"[{language.upper()} 코드 하이라이팅]")
        print("-" * 50)

        highlighted = highlight_code(code.strip(), language)
        all_code_blocks.append(highlighted)

        # 콘솔에는 적용된 클래스 태그 미리보기 표시
        # 주요 하이라이팅 포인트 표시
        keyword_count = highlighted.count('class="hl-keyword"')
        string_count = highlighted.count('class="hl-string"')
        comment_count = highlighted.count('class="hl-comment"')
        number_count = highlighted.count('class="hl-number"')
        builtin_count = highlighted.count('class="hl-builtin"')

        print(f"  키워드: {keyword_count}개")
        print(f"  문자열: {string_count}개")
        print(f"  주석: {comment_count}개")
        print(f"  숫자: {number_count}개")
        print(f"  빌트인: {builtin_count}개")
        print(f"  HTML 크기: {len(highlighted)} bytes")
        print()

    # HTML 데모 파일 생성
    output_path = "/tmp/my-vibe-blog/output/code-highlight-demo.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    css = get_highlight_css()
    code_sections = "\n\n".join(all_code_blocks)

    full_html = f"""\
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>코드 하이라이팅 데모</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        h1 {{ color: #333; }}
        {css}
    </style>
</head>
<body>
    <h1>코드 하이라이팅 데모</h1>
    <p>표준 라이브러리만으로 구현한 구문 하이라이팅입니다.</p>
    {code_sections}
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"데모 HTML이 저장되었습니다: {output_path}")
    print(f"파일 크기: {os.path.getsize(output_path)} bytes")
    print()
    print("코드 하이라이팅 데모가 완료되었습니다!")
