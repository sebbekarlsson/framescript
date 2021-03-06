from framescript.Lexer import Lexer
from framescript.Parser import Parser
from framescript.Transpiler import Transpiler

import sys
import jsbeautifier


if __name__ == '__main__':
    lexer = Lexer(open(sys.argv[1]).read())
    parser = Parser(lexer)
    transpiler = Transpiler()

    tree = parser.parse()

    x = transpiler.visit(tree)
    y = transpiler.finalize()

    print(y)
    print('<script>')
    print(jsbeautifier.beautify(x))
    print('</script>')
