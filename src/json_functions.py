from json_function_registration import json_func

from datetime import datetime

"""
Containing handy methods to be referenced by json
"""

@json_func
def current_year():
    return datetime.today().year