class EventListener(object):

    def __init__(
        self,
        event_name,
        variable_name,
        template_string,
        component=None
    ):
        self.event_name = event_name
        self.variable_name = variable_name
        self.template_string = template_string
        self.component = component
