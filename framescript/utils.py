import datetime
import base64
import random


def get_random_hash():
    return base64.b64encode(
        datetime.datetime.utcnow().strftime('%s') +
        str(random.randint(0, 1024))
    )


def get_outer_component(component):
    if component.component:
        return get_outer_component(component.component)
    else:
        return component
