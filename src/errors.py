def syntax(code, line):
    print "Invalid Syntax: \""+ code+ "\" line: ", str(line+1)

def typeerror(code, line):
    print "Type Error: \""+ code+ "\" line: ", str(line+1)

def undefined(code):
    print "Undefined: "+code

def invalidcall(code, line):
    print "Invalid Call: \""+ code+ "\" line: ", str(line+1)

def nofile(code, line):
    print "File Nonexistant: \""+ code+ "\" line: ", str(line+1)
