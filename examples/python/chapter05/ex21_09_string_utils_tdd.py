"""
예제 21-09: 실습 - TDD로 문자열 유틸리티 만들기
- capitalize_words, reverse_string, is_palindrome 등의 함수를
  TDD 방식으로 개발합니다
- 테스트를 먼저 작성하고, 구현을 작성하는 과정을 보여줍니다
"""

import unittest


# ============================================================
# 문자열 유틸리티 함수들 (TDD로 개발)
# ============================================================

def capitalize_words(text):
    """각 단어의 첫 글자를 대문자로 변환합니다.

    예: "hello world" → "Hello World"
    """
    if not text:
        return ""
    return " ".join(word.capitalize() for word in text.split())


def reverse_string(text):
    """문자열을 뒤집습니다.

    예: "hello" → "olleh"
    """
    if not isinstance(text, str):
        raise TypeError("문자열만 입력 가능합니다")
    return text[::-1]


def is_palindrome(text):
    """회문(팰린드롬)인지 확인합니다.
    대소문자와 공백을 무시합니다.

    예: "토마토" → True, "level" → True
    """
    if not isinstance(text, str):
        raise TypeError("문자열만 입력 가능합니다")
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def count_vowels(text):
    """영문 모음(a, e, i, o, u)의 개수를 셉니다.
    대소문자를 구분하지 않습니다.
    """
    if not isinstance(text, str):
        raise TypeError("문자열만 입력 가능합니다")
    vowels = set("aeiouAEIOU")
    return sum(1 for char in text if char in vowels)


def truncate(text, max_length, suffix="..."):
    """문자열을 지정된 길이로 자릅니다.
    길이를 초과하면 suffix를 붙입니다.

    예: truncate("Hello World", 8) → "Hello..."
    """
    if not isinstance(text, str):
        raise TypeError("문자열만 입력 가능합니다")
    if max_length < len(suffix):
        raise ValueError(f"max_length는 {len(suffix)} 이상이어야 합니다")
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def snake_to_camel(text):
    """snake_case를 camelCase로 변환합니다.

    예: "hello_world" → "helloWorld"
    """
    if not text:
        return ""
    parts = text.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


# ============================================================
# 테스트 클래스들 (TDD - 테스트 먼저!)
# ============================================================

class TestCapitalizeWords(unittest.TestCase):
    """capitalize_words 함수 테스트"""

    def test_basic(self):
        """기본 동작: 각 단어 첫 글자 대문자"""
        self.assertEqual(capitalize_words("hello world"), "Hello World")

    def test_single_word(self):
        """단어 하나"""
        self.assertEqual(capitalize_words("python"), "Python")

    def test_already_capitalized(self):
        """이미 대문자인 경우"""
        self.assertEqual(capitalize_words("Hello World"), "Hello World")

    def test_all_uppercase(self):
        """모두 대문자인 경우"""
        self.assertEqual(capitalize_words("HELLO WORLD"), "Hello World")

    def test_empty_string(self):
        """빈 문자열"""
        self.assertEqual(capitalize_words(""), "")

    def test_multiple_spaces(self):
        """여러 단어"""
        self.assertEqual(
            capitalize_words("the quick brown fox"),
            "The Quick Brown Fox"
        )


class TestReverseString(unittest.TestCase):
    """reverse_string 함수 테스트"""

    def test_basic(self):
        """기본 뒤집기"""
        self.assertEqual(reverse_string("hello"), "olleh")

    def test_korean(self):
        """한국어 뒤집기"""
        self.assertEqual(reverse_string("안녕"), "녕안")

    def test_empty(self):
        """빈 문자열"""
        self.assertEqual(reverse_string(""), "")

    def test_single_char(self):
        """글자 하나"""
        self.assertEqual(reverse_string("a"), "a")

    def test_palindrome(self):
        """회문은 뒤집어도 같습니다"""
        self.assertEqual(reverse_string("abcba"), "abcba")

    def test_type_error(self):
        """문자열이 아닌 입력"""
        with self.assertRaises(TypeError):
            reverse_string(123)


class TestIsPalindrome(unittest.TestCase):
    """is_palindrome 함수 테스트"""

    def test_english_palindrome(self):
        """영어 회문"""
        self.assertTrue(is_palindrome("level"))
        self.assertTrue(is_palindrome("madam"))
        self.assertTrue(is_palindrome("racecar"))

    def test_korean_palindrome(self):
        """한국어 회문"""
        self.assertTrue(is_palindrome("토마토"))
        self.assertTrue(is_palindrome("기러기"))

    def test_not_palindrome(self):
        """회문이 아닌 경우"""
        self.assertFalse(is_palindrome("hello"))
        self.assertFalse(is_palindrome("python"))

    def test_case_insensitive(self):
        """대소문자 무시"""
        self.assertTrue(is_palindrome("Level"))
        self.assertTrue(is_palindrome("Madam"))

    def test_with_spaces(self):
        """공백 무시"""
        self.assertTrue(is_palindrome("nurses run"))

    def test_single_char(self):
        """글자 하나는 항상 회문"""
        self.assertTrue(is_palindrome("a"))

    def test_empty(self):
        """빈 문자열은 회문"""
        self.assertTrue(is_palindrome(""))


class TestCountVowels(unittest.TestCase):
    """count_vowels 함수 테스트"""

    def test_basic(self):
        """기본 모음 세기"""
        self.assertEqual(count_vowels("hello"), 2)  # e, o

    def test_all_vowels(self):
        """모든 모음"""
        self.assertEqual(count_vowels("aeiou"), 5)

    def test_no_vowels(self):
        """모음 없음"""
        self.assertEqual(count_vowels("rhythm"), 0)

    def test_case_insensitive(self):
        """대소문자 무시"""
        self.assertEqual(count_vowels("HELLO"), 2)

    def test_empty(self):
        """빈 문자열"""
        self.assertEqual(count_vowels(""), 0)

    def test_korean(self):
        """한국어 (영문 모음 없음)"""
        self.assertEqual(count_vowels("안녕하세요"), 0)


class TestTruncate(unittest.TestCase):
    """truncate 함수 테스트"""

    def test_no_truncation_needed(self):
        """자르지 않아도 되는 경우"""
        self.assertEqual(truncate("hello", 10), "hello")

    def test_exact_length(self):
        """정확히 맞는 길이"""
        self.assertEqual(truncate("hello", 5), "hello")

    def test_truncation(self):
        """자르기 필요"""
        self.assertEqual(truncate("Hello World", 8), "Hello...")

    def test_custom_suffix(self):
        """커스텀 접미사"""
        self.assertEqual(
            truncate("Hello World", 9, suffix="~"),
            "Hello Wo~"
        )

    def test_too_small_max_length(self):
        """max_length가 suffix보다 짧으면 에러"""
        with self.assertRaises(ValueError):
            truncate("Hello", 2, suffix="...")


class TestSnakeToCamel(unittest.TestCase):
    """snake_to_camel 함수 테스트"""

    def test_basic(self):
        """기본 변환"""
        self.assertEqual(snake_to_camel("hello_world"), "helloWorld")

    def test_multiple_words(self):
        """여러 단어"""
        self.assertEqual(
            snake_to_camel("my_variable_name"),
            "myVariableName"
        )

    def test_single_word(self):
        """단어 하나 (변화 없음)"""
        self.assertEqual(snake_to_camel("hello"), "hello")

    def test_empty(self):
        """빈 문자열"""
        self.assertEqual(snake_to_camel(""), "")

    def test_two_words(self):
        """두 단어"""
        self.assertEqual(snake_to_camel("get_name"), "getName")


if __name__ == "__main__":
    print("=" * 60)
    print("예제 21-09: TDD로 문자열 유틸리티 만들기")
    print("=" * 60)
    print()
    print("구현한 함수 목록:")
    print("  1. capitalize_words() : 각 단어의 첫 글자를 대문자로")
    print("  2. reverse_string()   : 문자열 뒤집기")
    print("  3. is_palindrome()    : 회문 확인")
    print("  4. count_vowels()     : 영문 모음 세기")
    print("  5. truncate()         : 문자열 잘라내기")
    print("  6. snake_to_camel()   : snake_case → camelCase 변환")
    print()
    print("TDD 과정:")
    print("  1. 각 함수의 테스트를 먼저 작성했습니다")
    print("  2. 테스트를 통과하는 구현을 작성했습니다")
    print("  3. 모든 테스트가 통과하는지 확인합니다")
    print()

    # 사용 예시
    print("-" * 60)
    print("사용 예시:")
    print("-" * 60)
    print(f'  capitalize_words("hello world")  → "{capitalize_words("hello world")}"')
    print(f'  reverse_string("안녕하세요")      → "{reverse_string("안녕하세요")}"')
    print(f'  is_palindrome("토마토")          → {is_palindrome("토마토")}')
    print(f'  count_vowels("hello")            → {count_vowels("hello")}')
    print(f'  truncate("Hello World", 8)       → "{truncate("Hello World", 8)}"')
    print(f'  snake_to_camel("hello_world")    → "{snake_to_camel("hello_world")}"')
    print()

    print("-" * 60)
    print("테스트 실행 결과:")
    print("-" * 60)

    unittest.main(verbosity=2)
