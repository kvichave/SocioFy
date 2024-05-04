# myproject/jinja2/environment.py

from django_jinja import library
from jinja2 import Environment

@library.global_function
def my_custom_filter(value):
    return value.upper()

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        # Add any global variables or functions here
    })
    return env
