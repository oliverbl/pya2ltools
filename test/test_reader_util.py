from pathlib import Path
import unittest

from pya2ltools.a2l.reader.token import Lexer


class TestReaderUtil(unittest.TestCase):
    def tearDown(self):
        Path("test.a2l").unlink()

    def test_read_file(self):
        content = """ASAP2_VERSION 1 71
/begin PROJECT ASAP2_Example ""
"""
        with open("test.a2l", "w") as f:
            f.write(content)

        tokens = Lexer.from_file(Path("test.a2l"))
        expected = [
            "ASAP2_VERSION",
            " ",
            "1",
            " ",
            "71",
            "\n",
            "/begin",
            " ",
            "PROJECT",
            " ",
            "ASAP2_Example",
            " ",
            '""',
            "\n",
        ]
        self.assertEqual(expected, tokens.tokens)

    def test_read_file_with_comment(self):
        content = """ASAP2_VERSION 1 71
/begin PROJECT ASAP2_Example "" // comment
"""
        with open("test.a2l", "w") as f:
            f.write(content)

        tokens = Lexer.from_file(Path("test.a2l"))
        expected = [
            "ASAP2_VERSION",
            " ",
            "1",
            " ",
            "71",
            "\n",
            "/begin",
            " ",
            "PROJECT",
            " ",
            "ASAP2_Example",
            " ",
            '""',
            " ",
            "//",
            " ",
            "comment",
            "\n",
        ]
        self.assertEqual(expected, tokens.tokens)


def test_split_and_preserve_delimiter(self):
    
        t = Lexer.split_and_preserve_delimiter('"" // comment', "//", 0, 0)
        expected = ['"" ', "//", " comment"]
        self.assertEqual(expected, t)

        t2 = Lexer.split_and_preserve_delimiter(' comment', " ", 0, 0)
        expected = [" ", "comment"]
        self.assertEqual(expected, t2)

        t3 = Lexer.split_and_preserve_delimiter('/begin PROJECT ASAP2_Example "" // comment', "//", 0, 0)
        expected = ['/begin PROJECT ASAP2_Example "" ', "//", " comment"]
        self.assertEqual(expected, t3)
        t4 = Lexer.split_and_preserve_delimiter('//', " ", 0, 0)
        expected = ["//"]
        self.assertEqual(expected, t4)