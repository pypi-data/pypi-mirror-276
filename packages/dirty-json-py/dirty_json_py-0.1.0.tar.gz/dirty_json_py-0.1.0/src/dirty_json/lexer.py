import re
from collections import deque

class Lexer:
    LEX_KV = 0
    LEX_KVLIST = 1
    LEX_VLIST = 2
    LEX_BOOLEAN = 3
    LEX_COVALUE = 4
    LEX_CVALUE = 5
    LEX_FLOAT = 6
    LEX_INT = 7
    LEX_KEY = 8
    LEX_LIST = 9
    LEX_OBJ = 10
    LEX_QUOTE = 11
    LEX_RB = 12
    LEX_RCB = 13
    LEX_TOKEN = 14
    LEX_VALUE = 15

    LEX_COLON = -1
    LEX_COMMA = -2
    LEX_LCB = -3
    LEX_LB = -4
    LEX_DOT = -5

    def __init__(self):
        self.lex_map = {
            ":": {"type": self.LEX_COLON},
            ",": {"type": self.LEX_COMMA},
            "{": {"type": self.LEX_LCB},
            "}": {"type": self.LEX_RCB},
            "[": {"type": self.LEX_LB},
            "]": {"type": self.LEX_RB},
            ".": {"type": self.LEX_DOT}
        }

        self.lex_spc = [
            (re.compile(r"\s*:\s*"), self.LEX_COLON),
            (re.compile(r"\s*,\s*"), self.LEX_COMMA),
            (re.compile(r"\s*{\s*"), self.LEX_LCB),
            (re.compile(r"\s*}\s*"), self.LEX_RCB),
            (re.compile(r"\s*\[\s*"), self.LEX_LB),
            (re.compile(r"\s*\]\s*"), self.LEX_RB),
            (re.compile(r"\s*\.\s*"), self.LEX_DOT)
        ]

    def parse_string(self, s):
        s = s.replace(r"\/", "/")
        return bytes(s, "utf-8").decode("unicode_escape")

    def get_lexer(self, string):
        tokens = deque()
        col = 0
        row = 0

        def add_token(type, value, single=False):
            nonlocal col
            token_length = len(str(value)) if not isinstance(value, int) else len(str(value))
            tokens.append({"type": type, "value": value, "row": row, "col": col, "single": single})
            col += token_length

        patterns = [
            (re.compile(r'"((?:\\.|[^"])*?)($|")'), lambda m: add_token(self.LEX_QUOTE, self.parse_string(m.group(1)))),
            (re.compile(r"'((?:\\.|[^'])*?)($|'|(\",?[ \t]*\n))"), lambda m: add_token(self.LEX_QUOTE, self.parse_string(m.group(1)), single=True)),
            (re.compile(r"[\-0-9]*\.[0-9]*([eE][\+\-]?)?[0-9]*(?:\s*)"), lambda m: add_token(self.LEX_FLOAT, float(m.group(0)))),
            (re.compile(r"\-?[0-9]+([eE][\+\-]?)[0-9]*(?:\s*)"), lambda m: add_token(self.LEX_FLOAT, float(m.group(0)))),
            (re.compile(r"\-?[0-9]+(?:\s*)"), lambda m: add_token(self.LEX_INT, int(m.group(0))))
        ]

        for pattern, lex_type in self.lex_spc:
            patterns.append((pattern, lambda m, lex_type=lex_type: add_token(lex_type, m.group(0))))

        patterns.append((re.compile(r"\s"), lambda m: None if m.group(0) != "\n" else (col := 0, row := row + 1)))
        patterns.append((re.compile(r"\S[ \t]*"), lambda m: add_token(self.LEX_TOKEN, m.group(0))))

        pos = 0
        while pos < len(string):
            for pattern, action in patterns:
                match = pattern.match(string, pos)
                if match:
                    action(match)
                    pos = match.end()
                    break
            else:
                pos += 1

        return tokens

    def lex_string(self, s, emit):
        tokens = self.get_lexer(s)
        while tokens:
            emit(tokens.popleft())

    def get_all_tokens(self, s):
        tokens = []
        self.lex_string(s, tokens.append)
        return tokens
