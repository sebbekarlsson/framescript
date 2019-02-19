from bs4 import BeautifulSoup
from jinja2 import Template
from jscomp.utils import get_outer_component


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
        self.styles = []

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
        for c in self.pre:
            soup = BeautifulSoup(self.out_html, 'html.parser')
            el = soup.find('component', {'name': c['name']})
            el.append(BeautifulSoup(
                self.visit_render(c['render'], ret=True),
                'html.parser'
            ))
            self.out_html = str(soup)

        for s in self.styles:
            soup = BeautifulSoup(self.out_html, 'html.parser')
            el = soup.find('component', {'name': s['name']})

            if not el:
                el = soup.find(id='component__' + s['name'])
            else:
                el = el.find_all()[0]

            el['style'] = self.visit_template_string(
                s['style'].template_string)
            self.out_html = str(soup)

        return self.out_html

    def visit_component(self, component):
        rendered = COMPONENT_TEMPLATE.render(
            component=component,
            component_name=get_outer_component(component).name,
            component_body=self.visit(component.compound)
        )

        return rendered

    def visit_compound(self, compound):
        out = ''
        for node in compound.ast_nodes:
            output = self.visit(node)

            if node.__class__.__name__ != 'Render':
                out += output

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
        self.styles.append(dict(name=style.component.name, style=style))
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

    def visit_render(self, render, ret=False):
        if render.component.component and not ret:
            self.pre.append(dict(name=render.component.name, render=render))
            return ''

        html = self.visit(render.template_string)
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.findAll()
        component = render.component

        for tag in tags:
            element = tag.get('element')

            if element:
                tag['class'] = tag.get('class', ' ') + component.hashname\
                    + '-' + element

        tags[0]['id'] = 'component__' + component.name
        tags[0]['class'] = tags[0].get('class', '') + ' ' +\
            component.hashname

        text = str(soup)

        if ret:
            return text

        self.out_html += text

        return text
