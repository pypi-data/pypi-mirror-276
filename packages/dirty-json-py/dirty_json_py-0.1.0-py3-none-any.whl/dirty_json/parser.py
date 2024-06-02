from collections import deque
from .lexer import Lexer


class Parser:
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
        self.lexer = Lexer()

    def peek(self, arr):
        return arr[-1] if arr else None

    def last(self, arr, i):
        return arr[-(1 + i)] if len(arr) > i else None

    def is_type(self, obj, prop):
        return obj and "type" in obj and obj["type"] == prop

    def parse(self, text, dup_keys):
        stack = deque()
        tokens = deque()

        self.lexer.lex_string(text, tokens.append)

        if tokens[0]["type"] == self.LEX_LB and tokens[-1]["type"] != self.LEX_RB:
            tokens.append({"type": self.LEX_RB, "value": "]", "row": -1, "col": -1})

        if tokens[0]["type"] == self.LEX_LCB and tokens[-1]["type"] != self.LEX_RCB:
            tokens.append({"type": self.LEX_RCB, "value": "}", "row": -1, "col": -1})

        for token in tokens:
            stack.append(token)
            while self.reduce(stack):
                pass

        if len(stack) == 1 and stack[0]["type"] == self.LEX_KVLIST:
            stack = [{"type": self.LEX_OBJ, "value": stack[0]["value"]}]

        return self.compile_ost(stack[0], dup_keys)

    def reduce(self, stack):
        next_token = stack.pop()

        if next_token["type"] == self.LEX_KEY:
            if next_token["value"].strip() == "true":
                stack.append({"type": self.LEX_BOOLEAN, "value": "true"})
                return True
            if next_token["value"].strip() == "false":
                stack.append({"type": self.LEX_BOOLEAN, "value": "false"})
                return True
            if next_token["value"].strip() == "null":
                stack.append({"type": self.LEX_VALUE, "value": None})
                return True

        if next_token["type"] == self.LEX_TOKEN:
            if self.is_type(self.peek(stack), self.LEX_KEY):
                stack[-1]["value"] += next_token["value"]
                return True
            stack.append({"type": self.LEX_KEY, "value": next_token["value"]})
            return True

        if next_token["type"] == self.LEX_INT:
            if self.is_type(next_token, self.LEX_INT) and self.is_type(self.peek(stack), self.LEX_KEY):
                stack[-1]["value"] += next_token["value"]
                return True
            next_token["type"] = self.LEX_VALUE
            stack.append(next_token)
            return True

        if next_token["type"] == self.LEX_QUOTE:
            next_token["type"] = self.LEX_VALUE
            stack.append(next_token)
            return True

        if next_token["type"] == self.LEX_BOOLEAN:
            next_token["type"] = self.LEX_VALUE
            next_token["value"] = next_token["value"] == "true"
            stack.append(next_token)
            return True

        if next_token["type"] == self.LEX_FLOAT:
            next_token["type"] = self.LEX_VALUE
            stack.append(next_token)
            return True

        if next_token["type"] == self.LEX_VALUE:
            if self.is_type(self.peek(stack), self.LEX_COMMA):
                next_token["type"] = self.LEX_CVALUE
                stack.pop()
                stack.append(next_token)
                return True
            if self.is_type(self.peek(stack), self.LEX_COLON):
                next_token["type"] = self.LEX_COVALUE
                stack.pop()
                stack.append(next_token)
                return True
            if self.is_type(self.peek(stack), self.LEX_KEY) and self.is_type(self.last(stack, 1), self.LEX_VALUE):
                middle_val = stack.pop()
                stack[-1]["value"] += '"' + middle_val["value"] + '"'
                stack[-1]["value"] += next_token["value"]
                return True
            if self.is_type(self.peek(stack), self.LEX_KEY) and self.is_type(self.last(stack, 1), self.LEX_VLIST):
                middle_val = stack.pop()
                old_last_val = stack[-1]["value"].pop()
                old_last_val += '"' + middle_val["value"] + '"'
                old_last_val += next_token["value"]
                stack[-1]["value"].append(old_last_val)
                return True
            if self.is_type(self.peek(stack), self.LEX_KEY) and self.is_type(self.last(stack, 1), self.LEX_KVLIST):
                middle_val = stack.pop()
                old_last_val = stack[-1]["value"].pop()
                q_char = "'" if next_token["single"] else '"'
                old_last_val["value"] += q_char + middle_val["value"] + q_char
                old_last_val["value"] += next_token["value"]
                stack[-1]["value"].append(old_last_val)
                return True
            if self.is_type(self.peek(stack), self.LEX_KEY):
                key_value = stack.pop()["value"]
                next_token["value"] = key_value + next_token["value"]
                stack.append(next_token)
                return True

        if next_token["type"] == self.LEX_LIST:
            if self.is_type(next_token, self.LEX_LIST) and self.is_type(self.peek(stack), self.LEX_COMMA):
                next_token["type"] = self.LEX_CVALUE
                stack.pop()
                stack.append(next_token)
                return True
            if self.is_type(self.peek(stack), self.LEX_COLON):
                next_token["type"] = self.LEX_COVALUE
                stack.pop()
                stack.append(next_token)
                return True

        if next_token["type"] == self.LEX_OBJ:
            if self.is_type(self.peek(stack), self.LEX_COMMA):
                stack.pop()
                stack.append({"type": self.LEX_CVALUE, "value": next_token})
                return True
            if self.is_type(self.peek(stack), self.LEX_COLON):
                stack.pop()
                stack.append({"type": self.LEX_COVALUE, "value": next_token})
                return True
            if self.is_type(self.peek(stack), self.LEX_KEY):
                key = stack.pop()
                stack.append({"type": self.LEX_KV, "key": key["value"].strip(), "value": next_token})
                return True

        if next_token["type"] == self.LEX_CVALUE:
            if self.is_type(self.peek(stack), self.LEX_VLIST):
                stack[-1]["value"].append(next_token["value"])
                return True
            stack.append({"type": self.LEX_VLIST, "value": [next_token["value"]]})
            return True

        if next_token["type"] == self.LEX_VLIST:
            if self.is_type(self.peek(stack), self.LEX_VALUE):
                next_token["value"].insert(0, stack.pop()["value"])
                stack.append(next_token)
                return True
            if self.is_type(self.peek(stack), self.LEX_LIST):
                next_token["value"].insert(0, stack.pop()["value"])
                stack.append(next_token)
                return True
            if self.is_type(self.peek(stack), self.LEX_OBJ):
                next_token["value"].insert(0, stack.pop())
                stack.append(next_token)
                return True
            if self.is_type(self.peek(stack), self.LEX_KEY) and self.is_type(self.last(stack, 1), self.LEX_COMMA):
                l = stack.pop()
                stack.append({"type": self.LEX_VALUE, "value": l["value"]})
                while self.reduce(stack):
                    pass
                stack.append(next_token)
                return True
            if self.is_type(self.peek(stack), self.LEX_VLIST):
                stack[-1]["value"].append(next_token["value"][0])
                return True

        if next_token["type"] == self.LEX_COVALUE:
            if self.is_type(self.peek(stack), self.LEX_KEY) or self.is_type(self.peek(stack), self.LEX_VALUE) or self.is_type(self.peek(stack), self.LEX_VLIST):
                key = stack.pop()
                stack.append({"type": self.LEX_KV, "key": key["value"], "value": next_token["value"]})
                return True
            raise ValueError(f"Got a :value that can't be handled at line {next_token['row']}:{next_token['col']}")

        if next_token["type"] == self.LEX_KV:
            if self.is_type(self.last(stack, 0), self.LEX_COMMA) and self.is_type(self.last(stack, 1), self.LEX_KVLIST):
                stack[-2]["value"].append(next_token)
                stack.pop()
                return True
            stack.append({"type": self.LEX_KVLIST, "value": [next_token]})
            return True

        if next_token["type"] == self.LEX_KVLIST:
            if self.is_type(self.peek(stack), self.LEX_KVLIST):
                next_token["value"].extend(stack.pop()["value"])
                stack.append(next_token)
                return True

        if next_token["type"] == self.LEX_RB:
            if self.is_type(self.peek(stack), self.LEX_VLIST) and self.is_type(self.last(stack, 1), self.LEX_LB):
                l = stack.pop()
                stack.pop()
                stack.append({"type": self.LEX_LIST, "value": l["value"]})
                return True
            if self.is_type(self.peek(stack), self.LEX_LIST) and self.is_type(self.last(stack, 1), self.LEX_LB):
                l = stack.pop()
                stack.pop()
                stack.append({"type": self.LEX_LIST, "value": [l["value"]]})
                return True
            if self.is_type(self.peek(stack), self.LEX_LB):
                stack.pop()
                stack.append({"type": self.LEX_LIST, "value": []})
                return True
            if self.is_type(self.peek(stack), self.LEX_VALUE) and self.is_type(self.last(stack, 1), self.LEX_LB):
                val = stack.pop()["value"]
                stack.pop()
                stack.append({"type": self.LEX_LIST, "value": [val]})
                return True
            if self.is_type(self.peek(stack), self.LEX_OBJ) and self.is_type(self.last(stack, 1), self.LEX_LB):
                val = stack.pop()
                stack.pop()
                stack.append({"type": self.LEX_LIST, "value": [val]})
                return True
            if self.is_type(self.peek(stack), self.LEX_KEY) and self.is_type(self.last(stack, 1), self.LEX_COMMA):
                l = stack.pop()
                stack.append({"type": self.LEX_VALUE, "value": l["value"]})
                while self.reduce(stack):
                    pass
                stack.append({"type": self.LEX_RB})
                return True
            if self.is_type(self.peek(stack), self.LEX_COMMA) and (
                self.is_type(self.last(stack, 1), self.LEX_KEY)
                or self.is_type(self.last(stack, 1), self.LEX_OBJ)
                or self.is_type(self.last(stack, 1), self.LEX_VALUE)
            ):
                stack.pop()
                stack.append({"type": self.LEX_RB, "value": "]"})
                while self.reduce(stack):
                    pass
                return True
            if self.is_type(self.peek(stack), self.LEX_KEY) and self.is_type(self.last(stack, 1), self.LEX_LB):
                v = stack.pop()
                stack.pop()
                stack.append({"type": self.LEX_LIST, "value": [v["value"]]})
                return True
            if self.is_type(self.peek(stack), self.LEX_COMMA) and self.is_type(self.last(stack, 1), self.LEX_VLIST):
                stack.pop()
                stack.append({"type": self.LEX_RB})
                while self.reduce(stack):
                    pass
                return True

        if next_token["type"] == self.LEX_RCB:
            if self.is_type(self.peek(stack), self.LEX_KVLIST) and self.is_type(self.last(stack, 1), self.LEX_LCB):
                l = stack.pop()
                stack.pop()
                stack.append({"type": self.LEX_OBJ, "value": l["value"]})
                return True
            if self.is_type(self.peek(stack), self.LEX_LCB):
                stack.pop()
                stack.append({"type": self.LEX_OBJ, "value": None})
                return True
            if self.is_type(self.peek(stack), self.LEX_KEY) and self.is_type(self.last(stack, 1), self.LEX_COLON):
                l = stack.pop()
                stack.append({"type": self.LEX_VALUE, "value": l["value"]})
                while self.reduce(stack):
                    pass
                stack.append({"type": self.LEX_RCB})
                return True
            if self.is_type(self.peek(stack), self.LEX_COLON):
                stack.append({"type": self.LEX_VALUE, "value": None})
                while self.reduce(stack):
                    pass
                stack.append({"type": self.LEX_RCB})
                return True
            if self.is_type(self.peek(stack), self.LEX_COMMA):
                stack.pop()
                stack.append({"type": self.LEX_RCB})
                return True
            raise ValueError(f"Found }} that I can't handle at line {next_token['row']}:{next_token['col']}")

        if next_token["type"] == self.LEX_COMMA:
            if self.is_type(self.peek(stack), self.LEX_COMMA):
                return True
            if self.is_type(self.peek(stack), self.LEX_KEY):
                key = stack.pop()
                stack.append({"type": self.LEX_VALUE, "value": key["value"]})
                while self.reduce(stack):
                    pass
                stack.append(next_token)
                return True
            if self.is_type(self.peek(stack), self.LEX_COLON):
                stack.append({"type": self.LEX_VALUE, "value": None})
                while self.reduce(stack):
                    pass
                stack.append(next_token)
                return True

        stack.append(next_token)
        return False

    def compile_ost(self, tree, dup_keys):
        raw_types = ["boolean", "number", "string"]

        if type(tree) in [bool, int, float, str]:
            return tree

        if tree is None:
            return None

        if isinstance(tree, list):
            return [self.compile_ost(item, dup_keys) for item in tree]

        if self.is_type(tree, self.LEX_OBJ):
            result = {}
            if tree["value"] is None:
                return {}
            for item in tree["value"]:
                key = item["key"]
                val = self.compile_ost(item["value"], dup_keys)
                if isinstance(key, list):
                    key = ''.join(map(str, key))
                if dup_keys and key in result:
                    result[key] = {"value": result[key], "next": val}
                else:
                    result[key] = val
            return result

        if self.is_type(tree, self.LEX_LIST):
            return self.compile_ost(tree["value"], dup_keys)

        return tree["value"]
