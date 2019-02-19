from jscomp.Lexer import Lexer
from jscomp.Parser import Parser
from jscomp.Transpiler import Transpiler

import jsbeautifier

import argparse
import sys

from termcolor import colored


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input', type=str, help='Filename to transpile', required=True)
    parser.add_argument(
        '--output', type=str, help='Output filename', required=True)
    args = parser.parse_args()

    lexer = Lexer(open(args.input).read())
    parser = Parser(lexer)
    transpiler = Transpiler()

    print(colored('Creating AST tree...', 'green'))
    tree = parser.parse()
    print('AST tree is {} bytes.'.format(sys.getsizeof(tree)))

    print(colored('Generating Javascript...', 'green'))
    js = transpiler.visit(tree)

    print(colored('Generating HTML...', 'green'))
    html = transpiler.finalize()

    total_bytes = sys.getsizeof(js + html)

    print('Writing {} ...'.format(colored(args.output, attrs=['bold'])))
    open(args.output, 'w+').write('''
        {html}
        <script>{js}</script>
    '''.format(html=html, js=jsbeautifier.beautify(js)))
    print(colored('Done writing {}'.format(args.output), 'green'))
    print('({} bytes written)'.format(total_bytes))
