import re
from functools import reduce
from time import time
import argparse
import sys
sys.path.append("../part2/")
from tokens import tokens,Token,Lexeme
from typing import Callable,List,Tuple,Optional

class ScannerException(Exception):
    pass

class NGScanner:
    def __init__(self, tokens: List[Tuple[Token,str,Callable[[Lexeme],Lexeme]]]) -> None:
        self.tokens = tokens
        
        patterns = []
        self.token_map = {}
        
        for i, t in enumerate(tokens):
            group_name = f"{t[0].name}_{i}"
            patterns.append(f"(?P<{group_name}>{t[1]})")
            self.token_map[group_name] = (t[0], t[2])
            
        self.pattern = re.compile("|".join(patterns))
        
    def input_string(self, input_string:str) -> None:
        self.istring = input_string
        
    def token(self) -> Optional[Lexeme]:
        while True:
            if len(self.istring) == 0:
                return None
                
            match = self.pattern.match(self.istring)
            
            if match is None:
                raise ScannerException()
            
            matched_group = match.lastgroup
            matched_text = match.group(matched_group)
            
            token_type, action_func = self.token_map[matched_group]
            
            ret = action_func(Lexeme(token_type, matched_text))
            
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
    s = NGScanner(tokens)
    s.input_string(f_contents)
    start = time()
    while True:
        t = s.token()
        if t is None:
            break
        if (verbose):
            print(t)
    end = time()
    print("time to parse (seconds): ",str(end-start))
