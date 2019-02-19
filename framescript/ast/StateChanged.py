class StateChanged(object):

    def __init__(self, variable_name, template_string, component=None):
        self.variable_name = variable_name
        self.template_string = template_string
        self.component = component
