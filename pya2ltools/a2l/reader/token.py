from typing import Self

WHITESPACE_TOKENS = ["", " ", "\t", "\n"]


class Tokens:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self._index = 0

    @staticmethod
    def split_and_preserve_delimiter(text: str, delimiter: str) -> list[str]:
        tokens = []
        for e in text.split(delimiter):
            if e:
                tokens.append(e)
            tokens.append(delimiter)
        return tokens[:-1]

    @staticmethod
    def from_file(path: str) -> Self:
        tokens = []
        with path.open("r", encoding="utf-8-sig") as f:
            lines = f.readlines()
        for line in lines:
            temp = line.strip()
            temp = Tokens.split_and_preserve_delimiter(temp, delimiter="//")
            for t in temp:
                tokens += Tokens.split_and_preserve_delimiter(t, delimiter=" ")
            tokens += ["\n"]
        return Tokens(tokens)

    def _skip_comments_and_whitespaces(self, index) -> int:
        while (
            self.tokens[index] in WHITESPACE_TOKENS
            or self.tokens[index] == "//"
            or self.tokens[index] == "/*"
        ):
            if self.tokens[index] in WHITESPACE_TOKENS:
                index += 1
            if self.tokens[index] == "/*":
                while self.tokens[index] != "*/":
                    index += 1
                index = index + 1
            if self.tokens[index] == "//":
                while self.tokens[index] != "\n":
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
        return self.tokens[self._find_next_index(index)]

    def __len__(self):
        return max(len(self.tokens) - self._index, 0)

    def return_tokens_until(self, search_string: str) -> list[str]:
        search_tokens = Tokens.split_and_preserve_delimiter(
            search_string, delimiter=" "
        )
        for i in range(len(self)):
            end = self._index + i + len(search_tokens)
            if self.tokens[self._index + i : end] == search_tokens:
                tokens = self.tokens[self._index : end]
                self._index = self._skip_comments_and_whitespaces(end)
                return tokens
        return None

    def __str__(self):
        return str(self.tokens[self._index : self._index + 10])
