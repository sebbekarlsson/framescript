from bs4 import BeautifulSoup
from jinja2 import Template
from framescript.utils import get_outer_component


COMPONENT_TEMPLATE = Template(open(
    'js_templates/component.js').read())
COMPONENT_EVENT_LISTENER_TEMPLATE = Template(open(
    'js_templates/component_event_listener.js').read())
COMPONENT_CONSTRUCTOR_TEMPLATE = Template(open(
    'js_templates/component_constructor.js').read())
COMPONENT_STATE_CHANGED_TEMPLATE = Template(open(
    'js_templates/component_stateChanged.js').read())


class Transpiler(object):

    def __init__(self):
        self.out_js = ''
        self.out_html = ''
        self.pre = []
        self.styles = {}
        self.components = {}

    def visit(self, node):
        _name = node.__class__.__name__

        if _name == 'Component':
            return self.visit_component(node)
        elif _name == 'Compound':
            return self.visit_compound(node)
        elif _name == 'EventListener':
            return self.visit_event_listener(node)
        elif _name == 'Style':
            return self.visit_style(node)
        elif _name == 'Constructor':
            return self.visit_constructor(node)
        elif _name == 'StateChanged':
            return self.visit_state_changed(node)
        elif _name == 'TemplateString':
            return self.visit_template_string(node)
        elif _name == 'Render':
            return self.visit_render(node)

        return ''

    def finalize(self):
        return self.out_html

    def visit_component(self, component):
        self.components[component.name] = component

        rendered = COMPONENT_TEMPLATE.render(
            component=component,
            component_name=get_outer_component(component).name,
            component_body=self.visit(component.compound)
        )

        return rendered

    def visit_compound(self, compound):
        out = ''
        for node in compound.ast_nodes:
            if node.__class__.__name__ != 'Render':
                out += self.visit(node)
            else:
                self.visit(node)

        return out

    def visit_event_listener(self, event_listener):
        return COMPONENT_EVENT_LISTENER_TEMPLATE.render(
            event_name=event_listener.event_name,
            variable_name=event_listener.variable_name,
            code=self.visit(event_listener.template_string) + ';'
        )

    def visit_template_string(self, template_string):
        return template_string.value.replace('me.', '_this.')

    def visit_style(self, style):
        self.styles[style.component.name] = self.visit(style.template_string)
        return ''

    def visit_constructor(self, constructor):
        return COMPONENT_CONSTRUCTOR_TEMPLATE.render(
            code=self.visit_template_string(constructor.template_string)
        )

    def visit_state_changed(self, state_changed):
        return COMPONENT_STATE_CHANGED_TEMPLATE.render(
            variable_name=state_changed.variable_name,
            code=self.visit_template_string(state_changed.template_string)
        )

    def visit_render(self, render, ret=False, suffix=None):
        html = self.visit(render.template_string)
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.findAll()
        render.component.render = render
        outer_component = get_outer_component(render.component)

        tags[0]['fs-id'] = render.component.hashname

        if suffix is not None:
            tags[0]['fs-id-suffix'] = str(suffix)

        if render.component.name in self.styles:
            tags[0]['style'] = self.styles[render.component.name]

        index = 0
        for tag in tags:
            if tag.name == 'component':
                component_name = tag.get('cname')
                wanted_component = self.components[component_name]
                tag.append(BeautifulSoup(
                    self.visit_render(wanted_component.render, ret=True, suffix=index),
                    'html.parser'
                ))
                index += 1
            elif tag.get('element'):
                tag['fs-id'] = outer_component.hashname + '_' + tag.get('element')

        html = str(soup)

        if ret or render.component.component:
            return html
        else:
            self.out_html += html
