import sys
import operator as op
import re
import os

class Ernie:
    
    def __init__(self):
        self.variables = {}
        self.ops = {">":op.gt, "<":op.lt, "==":op.eq, "!=":op.ne,">=":op.ge, "<=":op.le}
        self.keys = ["-", "list", "add", "remove", "find","replace","input_int", "length" ,"input_str", "call", "use", "if", "while", "set", "func", "math", "say", 'swap']
        self.funcs = {}

    def run(self, code):
        code = code.split("\n")
        while True:
            try:
                code.remove("")
            except:
                break
        new = []
        for x in code:
            if x.startswith(" "):
                new.append(' '.join(x.split()))
            else:
                new.append(x)
        if "" not in new:
            new.append("")
        self.execute(self.parse(new))
         
    def parse(self, code):
        length = len(code)-1
        on = 0
        while on != length:
            if not code[on].split():
                break
            if code[on].split()[0] not in self.keys:
                print "Invalid Syntax: \""+ code[on]+ "\" line: ", str(on+1)
                exit()
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
                self.funcs[name] = c
            else:
                on += 1
        return code

    def execute(self, code):
        length = len(code)-1
        on = 0
        while on != length:
            if code[on].startswith("say"):
                data = code[on].split()
                print self.typecheck(' '.join(data[1:]))

            if code[on].startswith("set"):
                data = code[on].split()
                if data[2] != "=":
                    print "Syntax Error: \""+code[on]+"\" line: ", str(on+1)
                self.variables[data[1]] = self.typecheck(data[3])

            if code[on].startswith("use"):
                try:
                    data = code[on].split()[1]
                except:
                    print "Invalid Syntax: \""+ code[on]+ "\" line: ", str(on+1)
                    break
                if not os.path.exists(data):
                    print "No Such File: \""+ code[on]+ "\" line: ", str(on+1)
                    break
                else:
                    with open(data, 'rb') as file:
                        self.run(file.read())
            
            if code[on].startswith("swap"):
                data = code[on].split()
                if data[1] not in self.variables:
                    print "Undefined: \""+ code[on]+ "\" line: ", str(on+1);break
                else:
                    d = self.variables[data[1]]
                    if isinstance(d, int):
                        try:
                            self.variables[data[1]] = int(d)
                        except:
                            print "Value Error: \""+ code[on]+ "\" line: ", str(on+1);break
                    else:
                        self.variables[data[1]] = str(d)

            if code[on].startswith("call"):
                try:
                    function = self.typecheck(code[on].split()[1])
                except:
                    print "Invalid Syntax: \""+ code[on]+ "\" line: ", str(on+1)
                    break
                if function not in self.funcs:
                    print "Invalid Call: \""+ code[on]+ "\" line: ", str(on+1)
                    break
                else:
                    data = self.funcs[function]
                    self.run('\n'.join(data))

            if code[on].startswith("math"):
                data = code[on].split()
                stuff = data[3:]
                out = []
                for x in stuff:
                    if x == "+" or x == "/" or x == "%" or x == "*" or x == "-" or x == "//" or x == "**":
                        out.append(x)
                        continue
                    try:
                        int(x)
                        out.append(x)
                    except:
                        if x in self.variables:
                            out.append(str(self.variables[x]))
                        else:
                            print "Syntax Error: \""+code[on]+"\" line: ", str(on+1), x
                            exit()
            
                result = eval(''.join(out))
                self.variables[data[1]] = result
            
            if code[on].startswith("if"):
                data = code[on].split()
                data[1] = self.typecheck(data[1])
                data[3] = self.typecheck(data[3])     
                if self.ops[data[2]](data[1], data[3]):
                    code_ = '\n'.join(self.funcs[data[4]])
                    self.run(code_)
                

            if code[on].startswith("while"):
                data = code[on].split()
                var1 = data[1]
                var2 = data[3]
                while True:
                    data[1] = self.typecheck(var1)
                    data[3] = self.typecheck(var2) 
                    if self.ops[data[2]](data[1], data[3]):
                        code_ = '\n'.join(self.funcs[data[4]])
                        self.run(code_)
                    else:
                        break
            
            if code[on].startswith("add"):
                data = code[on].split()
                if data[2] not in self.variables:
                    print "Undefined: \""+code[on]+"\" line: ", str(on+1); break
                else:
                
                    self.variables[data[2]].append(self.typecheck(data[1]))


            if code[on].startswith("input_str"):
                data = code[on].split()
                if len(data) < 4:
                    print "Syntax Error: \""+code[on]+"\" line: ", str(on+1)
                    break
                if data[2] != "=":
                    print "Syntax Error: \""+code[on]+"\" line: ", str(on+1);break
                var = data[1]
                string = self.typecheck(' '.join(data[3:]))
                if isinstance(string, int):
                    print "Type Error: \""+code[on]+"\" line: ", str(on+1), string
                    break
                data = raw_input(string)
                try:
                    data = int(data)
                except:
                    print "Type Error: \""+code[on]+"\" line: ", str(on+1)
                    break
                else:
                    self.variables[var] = data
            
            if code[on].startswith("input_int"):
                data = code[on].split()
                if len(data) < 4:
                    print "Syntax Error: \""+code[on]+"\" line: ", str(on+1)
                    break
                if data[2] != "=":
                    print "Syntax Error: \""+code[on]+"\" line: ", str(on+1);break
                var = data[1]
                string = self.typecheck(' '.join(data[3:]))
                data = raw_input(string)
                self.variables[var] = data
            
            if code[on].startswith("find"):
                data = code[on].split()
                if data[2] != "=":
                    print "Syntax Error: \""+code[on]+"\" line: ", str(on+1);break
                var = data[1]
                check = str(self.typecheck(data[3]))
                string = str(self.typecheck(data[4]))
                if string.find(check):
                    out = "True"
                else:
                    out = "False"

                self.variables[var] = out
            
            if code[on].startswith("replace"):
                data = code[on].split()
                if data[2] != "=":
                    print "Syntax Error: \""+code[on]+"\" line: ", str(on+1);break
                var = data[1]
                check = str(self.typecheck(data[3]))
                string = str(self.typecheck(data[4]))
                new = str(self.typecheck(data[5]))
                self.variables[var] = string.replace(check, new)

            if code[on].startswith("list"):
                if not code[on].startswith("[") and not code[on].endswith("]"):
                    print "Syntax Error: \""+code[on]+"\" line: ", str(on+1);break
                data = code[on].split()
                if data[2] != "=":
                    print "Syntax Error: \""+code[on]+"\" line: ", str(on+1);break
                
                var = data[1]
                try:
                    self.variables[var] = eval(data[3])
                except:
                    print "Syntax Error: \""+code[on]+"\" line: ", str(on+1);break
            
            
            if code[on].startswith("length"):
                data = code[on].split()
                if data[2] != "=":
                    print "Syntax Error: \""+code[on]+"\" line: ", str(on+1);break
                var = data[1]
                self.variables[var] = len(self.typecheck(data[3]))
            
            on += 1

    def typecheck(self, data):
        try:
            return int(data)
        except:
            if data.startswith('"'):
                data = data[0:].strip()
                try:
                    return re.findall('"(.*?)"', data)[0]
                except:
                    return re.findall('"(.*?)', data)[0]
            elif "[" in data:
                data = data.split("[")
                if data[0] not in self.variables:
                    print "Undefined: \""+str(data)+"\""
                    exit()
                else:
                    num = data[1].strip("]")
                    try:
                        num = int(num)
                    except:
                        print "Type Error \""+str(data)+"\""
                        exit()
                    else:
                        return self.variables[data[0]][num]
            
            else:
                if data in self.variables:
                    return self.variables[data]
                else:
                    print "Undefined: \""+data+"\""
                    exit()
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: ./", sys.argv[0], "file.ern"
    else:
        with open(sys.argv[1], 'rb') as file:
            Ernie().run(file.read())
