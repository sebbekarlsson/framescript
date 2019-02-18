from jscomp.Token import Token


class Lexer(object):

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def good(self):
        return self.current_char != '\0' and self.pos < len(self.text) - 1

    def get_next_token(self):
        while self.good():
            if self.current_char == ' ' or ord(self.current_char) == 10\
                    and self.current_char == '\0':
                self.skip_whitespace()

            if self.current_char.isalnum() and not self.current_char.isdigit():
                return Token('ID', self.parse_id())

            if self.current_char == '=':
                token = Token('EQUALS', self.current_char)
                self.advance()
                return token

            if self.current_char == '[':
                token = Token('LBRACKET', self.current_char)
                self.advance()
                return token

            if self.current_char == ']':
                token = Token('RBRACKET', self.current_char)
                self.advance()
                return token

            if self.current_char == '{':
                token = Token('LBRACE', self.current_char)
                self.advance()
                return token

            if self.current_char == '}':
                token = Token('RBRACE', self.current_char)
                self.advance()
                return token

            if self.current_char == ':':
                token = Token('COLON', self.current_char)
                self.advance()
                return token

            if self.current_char == ';':
                token = Token('SEMI', self.current_char)
                self.advance()
                return token

            if self.current_char == '<':
                if self.peek() == '%':
                    return Token(
                        'TEMPLATE_STRING',
                        self.parse_template_string()
                    )
                else:
                    token = Token('LESS_THAN', self.current_char)
                    self.advance()
                    return token

            if self.current_char == '\'' or self.current_char == '"':
                return Token('STRING', self.parse_string())

            self.advance()

        return Token('EOF', '\0')

    def parse_id(self):
        value = ''

        while self.current_char.isalnum() or self.current_char == '_':
            value += self.current_char
            self.advance()

        return value

    def peek(self):
        return self.text[min(self.pos + 1, len(self.text) - 1)]

    def parse_template_string(self):
        value = ''
        self.advance()
        self.advance()

        while self.good():
            if self.current_char == '%':
                if self.peek() == '>':
                    break

            value += self.current_char
            self.advance()

        return value

    def parse_string(self):
        value = ''
        string_char = self.current_char
        self.advance()

        while self.good() and self.current_char != string_char:
            value += self.current_char
            self.advance()

        self.advance()

        return value

    def advance(self):
        if self.good():
            self.pos += 1
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        self.advance()

        while self.current_char == ' ' or ord(self.current_char) == 10 and\
                self.good():
            self.advance()
