from framescript.utils import get_outer_component


class Render(object):

    def __init__(self, template_string, component=None):
        self.template_string = template_string
        self.component = component
        outer_comp = get_outer_component(self.component)
        outer_comp.elements += self.template_string.tags
