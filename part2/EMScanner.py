import re
from functools import reduce
from time import time
import argparse
import sys

sys.path.append("../part2/")
from tokens import tokens, Token, Lexeme
from typing import Callable, List, Tuple, Optional


class ScannerException(Exception):
    pass


class SOSScanner:
    def __init__(self, tokens: List[Tuple[Token, str, Callable[[Lexeme], Lexeme]]]) -> None:
        self.tokens = tokens

    def input_string(self, input_string: str) -> None:
        self.istring = input_string

    def token(self) -> Optional[Lexeme]:
        while True:
            if len(self.istring) == 0:
                return None
            matches = []
            for t in self.tokens:
                matches.append((t[0],
                                re.match(t[1], self.istring),
                                t[2]))

            matches = [m for m in matches if m[1] is not None]

            if len(matches) == 0:
                raise ScannerException()

            longest = matches[0]
            for m in matches[1:]:
                if len(m[1].group(0)) > len(longest[1].group(0)):
                    longest = m

            ret = longest[2](Lexeme(longest[0], longest[1].group(0)))

            chop = len(ret.value)
            self.istring = self.istring[chop:]

            if ret.token != Token.IGNORE:
                return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    f = open(args.file_name)
    f_contents = f.read()
    f.close()
    verbose = args.verbose
    s = SOSScanner(tokens)
    s.input_string(f_contents)
    start = time()
    while True:
        t = s.token()
        if t is None:
            break
        if (verbose):
            print(t)
    end = time()
    print("time to parse (seconds): ", str(end - start))
