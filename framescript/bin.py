from framescript.Lexer import Lexer
from framescript.Parser import Parser
from framescript.Transpiler import Transpiler

from jsmin import jsmin
from htmlmin import minify as minify_html

import argparse
import sys

from termcolor import colored


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input', type=str, help='Filename to transpile', required=True)
    parser.add_argument(
        '--output', type=str, help='Output filename', required=True)
    parser.add_argument(
        '--minify',
        type=bool,
        help='If set, then Javascript and HTML will be minified',
        required=False
    )
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

    if args.minify:
        print('Minifying javascript...')
        js = jsmin(js)
        print('Minifying html...')
        html = minify_html(html)

    total_bytes = sys.getsizeof(js + html)

    print('Writing {} ...'.format(colored(args.output, attrs=['bold'])))
    open(args.output, 'w+').write('''
        {html}
        <script>{js}</script>
    '''.format(html=html, js=js))
    print(colored('Done writing {}'.format(args.output), 'green'))
    print('({} bytes written)'.format(total_bytes))
