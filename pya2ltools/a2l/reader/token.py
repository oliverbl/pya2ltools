from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Self

WHITESPACE_TOKENS = ["", " ", "\t", "\n"]


@dataclass()
class Token:
    content: str
    line: int
    pos: int
    filename: Path = None

    def __str__(self):
        return self.content

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, str):
            return self.content == __value
        if isinstance(__value, Token):
            return self.content == __value.content

    @property
    def location(self) -> str:
        return f"{self.filename}, line {self.line}:{self.pos}"


class Lexer:
    def __init__(self, tokens: list[str], filepath: Path):
        self.tokens: list[Token] = tokens
        self.filepath = filepath
        self._index = self._skip_comments_and_whitespaces(0)

    @staticmethod
    def split_and_preserve_delimiter(
        text: str, delimiter: str, line: int, pos: int
    ) -> list[Token]:
        tokens = []
        while True:
            index = text.find(delimiter)
            if index == -1:
                if text:
                    tokens.append(Token(text, line=line, pos=pos))
                break
            t = text[:index]
            if t:
                tokens.append(Token(t, line=line, pos=pos))
            tokens.append(Token(delimiter, line=line, pos=index + pos))
            pos += index + len(delimiter)
            text = text[index + len(delimiter) :]

        return tokens

    @staticmethod
    def get_left_and_right_whitespaces(text: str, line: int) -> tuple[str, str]:
        left = []
        right = []
        i = 0
        while i < len(text) and text[i] in WHITESPACE_TOKENS:
            left.append(Token(text[i], line, i))
            i += 1
        i = 0
        text = text.lstrip()
        while i < len(text) and text[-1 - i] in WHITESPACE_TOKENS:
            right.append(Token(text[-1 - i], line, len(text) - 1 - i))
            i += 1
        return left, right[::-1]

    @staticmethod
    def from_file(path: Path | str) -> Self:
        if isinstance(path, str):
            path = Path(path)
        tokens: list[Token] = []
        with path.open("r", encoding="utf-8-sig") as f:
            lines: list[str] = f.readlines()
        for no, line in enumerate(lines, start=1):
            left, right = Lexer.get_left_and_right_whitespaces(line, no)
            tokens += left

            temp = line.strip()
            index = len(line) - len(line.lstrip())
            temp = Lexer.split_and_preserve_delimiter(
                temp, delimiter="//", line=no, pos=index + 1
            )
            for t in temp:
                t2 = Lexer.split_and_preserve_delimiter(
                    t.content, delimiter=" ", line=no, pos=t.pos
                )
                tokens += t2
            tokens += right
        for t in tokens:
            t.filename = path
        return Lexer(tokens, filepath=path)

    def _skip_comments_and_whitespaces(self, index) -> int:
        while index < len(self.tokens) and (
            self.tokens[index].content in WHITESPACE_TOKENS
            or self.tokens[index].content == "//"
            or self.tokens[index].content == "/*"
        ):
            if self.tokens[index].content in WHITESPACE_TOKENS:
                index += 1
            if self.tokens[index].content == "/*":
                while self.tokens[index].content != "*/":
                    index += 1
                index = index + 1
            if self.tokens[index].content == "//":
                while self.tokens[index].content != "\n":
                    index += 1
                index = index + 1
        return index

    def _find_next_index(self, index) -> int:
        temp = self._index
        try:
            for _ in range(index):
                temp = self._skip_comments_and_whitespaces(temp + 1)
            return temp
        except IndexError:
            return len(self.tokens)

    # return tokens without whitespaces and comments
    def __getitem__(self, index):
        if isinstance(index, slice):
            if index.start is not None:
                self._index = self._find_next_index(index.start)
            return self
        return self.tokens[self._find_next_index(index)].content

    def __len__(self):
        return max(len(self.tokens) - self._index, 0)

    def return_tokens_until(self, search_string: str) -> list[str]:
        search_tokens = Lexer.split_and_preserve_delimiter(
            search_string, delimiter=" ", line=0, pos=0
        )
        for i in range(len(self)):
            end = self._index + i + len(search_tokens)
            if self.tokens[self._index + i : end] == search_tokens:
                tokens = self.tokens[self._index : end]
                self._index = self._skip_comments_and_whitespaces(end)
                return [t.content for t in tokens[:-3]]
        return None

    def __str__(self):
        return str(self.tokens[self._index - 10 : self._index + 20])

    def get(self, index: int) -> Token:
        return self.tokens[self._index + index]

    def get_keyword(self, index: int) -> Token:
        return self.tokens[self._find_next_index(index)]

    def get_pos(self, index: int) -> Token:
        token = self.tokens[self._index + index]
        return f"Line: {token.line}, Pos: {token.pos}, File: {self.filepath}"


class UnknownTokenError(Exception):
    def __init__(self, token: Token, expected: str | list[str] = None):
        if expected is None:
            expected = ""
        elif isinstance(expected, str):
            expected = f", expected: {expected}"
        elif isinstance(expected, Iterable):
            expected = f", expected one of: {' | '.join(expected)}"
        super().__init__(f"Unknown token {token.content}{expected} at {token.location}")


class MissingKeywordError(Exception):
    def __init__(self, missing_keyword: str, name: str, token: Token):
        super().__init__(
            f"Expected keyword {missing_keyword} when parsing {name} at {token.location}"
        )


class InvalidKeywordError(Exception):
    def __init__(self, invalid_keyword: str, name: str, token: Token):
        super().__init__(
            f"Invalid keyword {invalid_keyword} when parsing {name} at {token.location}"
        )


class InvalidTypeError(Exception):
    def __init__(self, expected_type: str, token: Token):
        super().__init__(
            f"Invalid type {token.content}, expected {expected_type} at {token.location}"
        )
