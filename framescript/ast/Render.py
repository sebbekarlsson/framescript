from framescript.utils import get_outer_component


class Render(object):

    def __init__(self, template_string, component=None):
        self.template_string = template_string
        self.component = component
        outer_comp = get_outer_component(self.component)

        for t in filter(lambda x: x.get('element'), template_string.tags):
            outer_comp.elements.append(dict(
                name=t['element'],
                classname=self.component.hashname + '-' + t['element']
            ))
