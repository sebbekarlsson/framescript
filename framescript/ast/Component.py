from framescript.utils import get_random_hash


class Component(object):

    def __init__(self, name, compound, component=None):
        self.name = name
        self.compound = compound
        self.component = component
        self.hashname = get_random_hash().replace('=', '')
        self.elements = []

    def get_component_elements(self):
        return filter(lambda x: x.get('cname'), self.elements)
