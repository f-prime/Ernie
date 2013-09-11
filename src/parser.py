import data
import errors as error

def parse(code):
    length = len(code)-1
    on = 0
    while on != length:

        if not code[on].split():
            break
        if code[on].split()[0] not in data.keys:
            error.syntax(code[on], on)
        if code[on].startswith("-"):
            code.remove(code[on])
        if code[on].startswith("func"):
            name = code[on].split()[1]
            c = []
            code.remove(code[on])
            while code[on] != "endfunc":
                c.append(code[on])
                code.remove(code[on])
            code.remove(code[on])
            data.funcs[name] = c
        else:
            on += 1
    return code
