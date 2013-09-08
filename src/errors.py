def syntax(code, line):
    print "Invalid Syntax: \""+ code+ "\" line: ", str(line+1)
    exit()

def typeerror(code, line):
    print "Type Error: \""+ code+ "\" line: ", str(line+1)
    exit()

def undefined(code):
    print "Undefined: "+code
    exit()

def invalidcall(code, line):
    print "Invalid Call: \""+ code+ "\" line: ", str(line+1)
    exit()

def nofile(code, line):
    print "File Nonexistant: \""+ code+ "\" line: ", str(line+1)
    exit()
