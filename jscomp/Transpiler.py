from bs4 import BeautifulSoup
from jinja2 import Template


COMPONENT_TEMPLATE = Template(open(
    'js_templates/component.js').read())
COMPONENT_EVENT_LISTENER_TEMPLATE = Template(open(
    'js_templates/component_event_listener.js').read())
COMPONENT_CONSTRUCTOR_TEMPLATE = Template(open(
    'js_templates/component_constructor.js').read())

DATA_SYNC = '''
    var _keys = Object.keys(_this.state);
    for (var i = 0; i < _keys.length; i++) {
        var k = _keys[i];
        var query = 'component__COMPONENT_NAME__attribute__' + k;
        var element = document.getElementById(query);
        element.innerHTML = _this.state[k];
    };
'''


def get_outer_component(component):
    if component.component:
        return get_outer_component(component.component)
    else:
        return component


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
            code=self.visit(event_listener.template_string) + ';' +
            DATA_SYNC.replace(
                'COMPONENT_NAME',
                get_outer_component(event_listener.component).name
            )
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

    def visit_render(self, render, ret=False):
        if render.component.component and not ret:
            self.pre.append(dict(name=render.component.name, render=render))
            return ''

        html = self.visit(render.template_string)
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.findAll()
        component = render.component
        component_name = get_outer_component(render.component).name

        for tag in tags:
            sync = tag.get('sync')

            if sync:
                tag['id'] = 'component__' + component_name +\
                    '__attribute__' + sync
                del tag['sync']

        tags[0]['id'] = 'component__' + component.name

        text = str(soup)

        if ret:
            return text

        self.out_html += text

        return text
