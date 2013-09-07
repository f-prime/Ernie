import sys
import lexer

if len(sys.argv) < 2:
    print "Usage: ./ernie <file.ern>"
else:
    with open(sys.argv[1], 'rb') as file:
        lexer.lex(file.read())

