from framescript.ast.TemplateString import TemplateString
from framescript.ast.EventListener import EventListener
from framescript.ast.StateChanged import StateChanged
from framescript.ast.Constructor import Constructor
from framescript.ast.Component import Component
from framescript.ast.Compound import Compound
from framescript.ast.Render import Render
from framescript.ast.Import import Import
from framescript.ast.Style import Style


class UnexpectedTokenException(Exception):
    pass


class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type, help=None):
        if token_type != self.current_token.type:
            raise UnexpectedTokenException(
                '[{}]: Line {}, expected {} but got {}'.format(
                    self.lexer.filename,
                    self.lexer.line,
                    token_type,
                    self.current_token.type
                ) + (('\n' + help) if help else '')
            )
        else:
            self.current_token = self.lexer.get_next_token()

    def parse(self):
        return self.parse_compound(None)

    def parse_event_listener(self, component):
        self.eat('ID')  # listen
        event_name = self.current_token.value
        self.eat('ID')  # name
        self.eat('ID', help='Use: "listen <event> `as` <variable_name>"')  # as
        variable_name = self.current_token.value
        self.eat('ID')  # variable_name
        template_string = TemplateString(self.current_token.value)
        self.eat('TEMPLATE_STRING')

        return EventListener(
            event_name,
            variable_name,
            template_string,
            component
        )

    def parse_style(self, component):
        self.eat('ID')  # style
        template_string = TemplateString(self.current_token.value)
        self.eat('TEMPLATE_STRING')

        return Style(template_string=template_string, component=component)

    def parse_import(self, component):
        self.eat('ID')  # import
        import_string = self.current_token.value
        self.eat('STRING')  # string

        return Import(import_string)

    def parse_constructor(self, component):
        self.eat('ID')  # constructor
        template_string = TemplateString(self.current_token.value)
        self.eat('TEMPLATE_STRING')

        return Constructor(
            template_string=template_string, component=component)

    def parse_state_changed(self, component):
        self.eat('ID')  # stateChanged
        self.eat('ID', help='Use: "stateChanged `as` <variable_name>"')  # as
        variable_name = self.current_token.value
        self.eat('ID')  # name
        template_string = TemplateString(self.current_token.value)
        self.eat('TEMPLATE_STRING')

        return StateChanged(
            variable_name=variable_name,
            template_string=template_string,
            component=component
        )

    def parse_render(self, component):
        self.eat('ID')
        template_string = TemplateString(self.current_token.value)
        self.eat('TEMPLATE_STRING')

        return Render(template_string, component)

    def parse_compound(self, component):
        return Compound(self.parse_statement_list(component))

    def parse_statement_list(self, component):
        nodes = []

        nodes.append(self.parse_statement(component))

        if not self.current_token.type == 'SEMI':
            raise UnexpectedTokenException('[{}]: Line {}, Missing `;`'.format(
                self.lexer.filename,
                self.lexer.line))

        while self.current_token.type == 'SEMI':
            self.eat('SEMI')
            statement = self.parse_statement(component)

            nodes.append(statement)

        return nodes

    def parse_statement(self, component):
        if self.current_token.type == 'ID':
            if self.current_token.value == 'listen':
                return self.parse_event_listener(component)
            elif self.current_token.value == 'style':
                return self.parse_style(component)
            elif self.current_token.value == 'constructor':
                return self.parse_constructor(component)
            elif self.current_token.value == 'stateChanged':
                return self.parse_state_changed(component)
            elif self.current_token.value == 'component':
                return self.parse_component(component)
            elif self.current_token.value == 'import':
                return self.parse_import(component)
            else:
                return self.parse_render(component)

    def parse_component(self, component):
        component = Component(None, None, False, component)
        self.eat('ID')
        self.eat('LBRACKET')
        component.name = self.current_token.value
        self.eat('ID')
        self.eat('RBRACKET')

        if self.current_token.type == 'ABSTRACT':
            component.abstract = True
            self.eat('ABSTRACT')

        self.eat('LBRACE')
        component.compound = self.parse_compound(component)
        self.eat('RBRACE')

        return component
