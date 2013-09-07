from parser import parse
from interpreter import execute

def lex(code):
    code = code.strip().split("\n")
    for x in range(code.count("")):
        code.remove("")
    code.append("")
    execute(parse(code))
    

