import json
import re
import warnings
from collections import deque
from .parser import Parser


class DirtyJSON:
    def __init__(self):
        self.parser = Parser()

    def parse(self, text, config=None):
        fallback = True
        duplicate_keys = False

        if config:
            if "fallback" in config and config["fallback"] is False:
                fallback = False
            duplicate_keys = "duplicateKeys" in config and config["duplicateKeys"] is True

        try:
            return self.parser.parse(text, duplicate_keys)
        except Exception as e:
            if not fallback:
                raise e

            try:
                json_data = json.loads(text)
                warnings.warn(
                    f"dirty-json got valid JSON that failed with the custom parser. "
                    f"We're returning the valid JSON, but please file a bug report here: "
                    f"https://github.com/bitnom/dirty-json-py/issues  -- the JSON that caused the failure was: {text}"
                )
                return json_data
            except json.JSONDecodeError:
                raise e
