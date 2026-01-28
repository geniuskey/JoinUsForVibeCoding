"""
예제 27-09: 테이블 출력 (ANSI 코드로 깔끔한 테이블 출력)

rich 라이브러리 없이 ANSI 이스케이프 코드를 사용하여
터미널에서 깔끔한 테이블을 출력하는 방법을 구현합니다.
"""

import random
import os


# ANSI 이스케이프 코드 정의
class Color:
    """ANSI 색상 코드를 관리합니다."""

    # 텍스트 색상
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # 밝은 색상
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_CYAN = "\033[96m"

    # 배경 색상
    BG_BLUE = "\033[44m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_RED = "\033[41m"
    BG_CYAN = "\033[46m"

    # 스타일
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"

    @classmethod
    def is_supported(cls):
        """현재 터미널이 ANSI 코드를 지원하는지 확인합니다."""
        return os.environ.get("TERM") != "dumb" and hasattr(os, "isatty")

    @classmethod
    def colorize(cls, text, color):
        """텍스트에 색상을 적용합니다."""
        return f"{color}{text}{cls.RESET}"


class Table:
    """터미널에서 깔끔한 테이블을 출력합니다."""

    # 테이블 테두리 문자 (유니코드 박스 드로잉)
    BORDER_SINGLE = {
        "tl": "+", "tr": "+", "bl": "+", "br": "+",
        "h": "-", "v": "|",
        "lj": "+", "rj": "+", "tj": "+", "bj": "+", "cj": "+",
    }

    BORDER_DOUBLE = {
        "tl": "+", "tr": "+", "bl": "+", "br": "+",
        "h": "=", "v": "|",
        "lj": "+", "rj": "+", "tj": "+", "bj": "+", "cj": "+",
    }

    BORDER_UNICODE = {
        "tl": "\u250c", "tr": "\u2510", "bl": "\u2514", "br": "\u2518",
        "h": "\u2500", "v": "\u2502",
        "lj": "\u251c", "rj": "\u2524", "tj": "\u252c", "bj": "\u2534", "cj": "\u253c",
    }

    def __init__(self, title=None, border_style="unicode"):
        self.title = title
        self.columns = []  # [(name, width, align, color)]
        self.rows = []
        self.footer = None

        if border_style == "unicode":
            self.border = self.BORDER_UNICODE
        elif border_style == "double":
            self.border = self.BORDER_DOUBLE
        else:
            self.border = self.BORDER_SINGLE

    def add_column(self, name, width=None, align="right", color=None):
        """컬럼을 추가합니다."""
        if width is None:
            width = max(len(name) + 2, 8)
        self.columns.append({
            "name": name,
            "width": width,
            "align": align,
            "color": color,
        })

    def add_row(self, *values, highlight=False, color=None):
        """행을 추가합니다."""
        self.rows.append({
            "values": values,
            "highlight": highlight,
            "color": color,
        })

    def set_footer(self, *values):
        """하단 합계 행을 설정합니다."""
        self.footer = values

    def _format_cell(self, value, col_info, row_color=None):
        """셀 값을 포맷합니다."""
        width = col_info["width"]
        align = col_info["align"]
        color = row_color or col_info.get("color")

        # 숫자 포맷
        if isinstance(value, (int, float)):
            if isinstance(value, float):
                text = f"{value:,.1f}"
            else:
                text = f"{value:,}"
        else:
            text = str(value)

        # 너비에 맞게 정렬
        if len(text) > width:
            text = text[:width - 2] + ".."

        if align == "right":
            text = text.rjust(width)
        elif align == "center":
            text = text.center(width)
        else:
            text = text.ljust(width)

        # 색상 적용
        if color:
            text = Color.colorize(text, color)

        return text

    def _draw_line(self, left, middle, right, fill):
        """테두리 선을 그립니다."""
        parts = []
        for i, col in enumerate(self.columns):
            parts.append(fill * (col["width"] + 2))
        return left + middle.join(parts) + right

    def render(self):
        """테이블을 렌더링합니다."""
        lines = []
        b = self.border

        # 제목
        if self.title:
            total_width = sum(c["width"] + 3 for c in self.columns) - 1
            title_line = Color.colorize(
                f" {self.title} ".center(total_width),
                Color.BOLD + Color.BRIGHT_CYAN
            )
            lines.append(title_line)

        # 상단 테두리
        lines.append(self._draw_line(b["tl"], b["tj"], b["tr"], b["h"]))

        # 헤더
        header_cells = []
        for col in self.columns:
            name = col["name"].center(col["width"])
            header_cells.append(f" {Color.colorize(name, Color.BOLD + Color.BRIGHT_YELLOW)} ")
        lines.append(b["v"] + b["v"].join(header_cells) + b["v"])

        # 헤더 구분선
        lines.append(self._draw_line(b["lj"], b["cj"], b["rj"], b["h"]))

        # 데이터 행
        for i, row in enumerate(self.rows):
            cells = []
            for j, col in enumerate(self.columns):
                value = row["values"][j] if j < len(row["values"]) else ""
                row_color = row.get("color")

                # 행 하이라이트
                if row["highlight"]:
                    row_color = Color.BRIGHT_GREEN

                cell_text = self._format_cell(value, col, row_color)
                cells.append(f" {cell_text} ")
            lines.append(b["v"] + b["v"].join(cells) + b["v"])

        # 하단 합계 행
        if self.footer:
            lines.append(self._draw_line(b["lj"], b["cj"], b["rj"], b["h"]))
            footer_cells = []
            for j, col in enumerate(self.columns):
                value = self.footer[j] if j < len(self.footer) else ""
                cell_text = self._format_cell(value, col, Color.BOLD + Color.BRIGHT_CYAN)
                footer_cells.append(f" {cell_text} ")
            lines.append(b["v"] + b["v"].join(footer_cells) + b["v"])

        # 하단 테두리
        lines.append(self._draw_line(b["bl"], b["bj"], b["br"], b["h"]))

        return "\n".join(lines)

    def print(self):
        """테이블을 출력합니다."""
        print(self.render())


def create_status_badge(status):
    """상태 배지를 생성합니다."""
    badges = {
        "완료": Color.colorize(" 완료 ", Color.BRIGHT_GREEN),
        "진행중": Color.colorize(" 진행 ", Color.BRIGHT_YELLOW),
        "대기": Color.colorize(" 대기 ", Color.DIM),
        "오류": Color.colorize(" 오류 ", Color.BRIGHT_RED),
        "상승": Color.colorize(" +상승", Color.BRIGHT_GREEN),
        "하락": Color.colorize(" -하락", Color.BRIGHT_RED),
        "유지": Color.colorize(" =유지", Color.YELLOW),
    }
    return badges.get(status, status)


if __name__ == "__main__":
    random.seed(42)

    # 1. 기본 판매 테이블
    print()
    table1 = Table(title="월별 판매 현황")
    table1.add_column("월", width=6, align="center")
    table1.add_column("매출(만원)", width=12)
    table1.add_column("건수", width=8)
    table1.add_column("객단가", width=10)
    table1.add_column("전월비", width=8, align="center")

    monthly_data = [
        (1, 4520, 156, 28974, ""),
        (2, 3890, 134, 29030, "하락"),
        (3, 5210, 178, 29270, "상승"),
        (4, 4870, 165, 29515, "하락"),
        (5, 6340, 215, 29488, "상승"),
        (6, 5980, 198, 30202, "하락"),
    ]

    total_sales = 0
    total_count = 0
    for month, sales, count, avg, trend in monthly_data:
        total_sales += sales
        total_count += count
        badge = create_status_badge(trend) if trend else "-"
        # 최고 매출 행 하이라이트
        highlight = (sales == max(d[1] for d in monthly_data))
        table1.add_row(f"{month}월", sales, count, avg, badge, highlight=highlight)

    table1.set_footer("합계", total_sales, total_count,
                      total_sales * 10000 // total_count, "-")
    table1.print()

    # 2. 카테고리별 현황 테이블
    print()
    table2 = Table(title="카테고리별 실적 요약")
    table2.add_column("카테고리", width=10, align="center")
    table2.add_column("상품수", width=8)
    table2.add_column("총매출", width=12)
    table2.add_column("평균단가", width=10)
    table2.add_column("점유율", width=8)
    table2.add_column("상태", width=8, align="center")

    cat_data = [
        ("전자기기", 45, 15800000, 48200, 52.3, "상승"),
        ("사무용품", 30, 8900000, 33500, 29.5, "유지"),
        ("액세서리", 25, 5500000, 18700, 18.2, "하락"),
    ]

    for cat, items, sales, avg_price, share, status in cat_data:
        badge = create_status_badge(status)
        color = None
        if status == "상승":
            color = Color.GREEN
        elif status == "하락":
            color = Color.RED
        table2.add_row(cat, items, sales, avg_price, f"{share}%", badge, color=color)

    table2.set_footer("합계", 100, 30200000, "-", "100%", "-")
    table2.print()

    # 3. 지역별 순위 테이블
    print()
    table3 = Table(title="지역별 매출 순위")
    table3.add_column("순위", width=4, align="center")
    table3.add_column("지역", width=8, align="center")
    table3.add_column("매출", width=12)
    table3.add_column("건수", width=6)
    table3.add_column("점유율", width=8)

    region_data = [
        (1, "서울", 12500000, 95, "31.2%"),
        (2, "경기", 9800000, 76, "24.5%"),
        (3, "부산", 6200000, 48, "15.5%"),
        (4, "인천", 5800000, 44, "14.5%"),
        (5, "대구", 5700000, 42, "14.3%"),
    ]

    for rank, region, sales, count, share in region_data:
        highlight = (rank <= 3)
        table3.add_row(rank, region, sales, count, share, highlight=highlight)

    table3.print()

    # 4. 심플한 ASCII 테이블 (ANSI 미지원 환경용)
    print()
    table4 = Table(title="최근 주문 내역", border_style="single")
    table4.add_column("주문번호", width=10, align="center")
    table4.add_column("상품", width=14, align="left")
    table4.add_column("수량", width=6)
    table4.add_column("금액", width=10)

    orders = [
        ("ORD-0198", "무선 키보드", 2, 68000),
        ("ORD-0199", "블루투스 마우스", 1, 29000),
        ("ORD-0200", "USB 허브", 3, 54000),
        ("ORD-0201", "헤드셋", 1, 55000),
        ("ORD-0202", "마우스패드", 5, 65000),
    ]

    for order_id, product, qty, amount in orders:
        table4.add_row(order_id, product, qty, amount)

    table4.set_footer("", "합계", sum(o[2] for o in orders), sum(o[3] for o in orders))
    table4.print()
