import json
from django import template



register=template.Library()


@register.filter(name='jsonify')
def jsonify(data):
 
    if isinstance(data,dict):
        return data
    else:
         return json.loads(data)
@register.filter(name='stringify')
def stringify(data):

    if isinstance(data,dict):
        return json.dumps(data)
    else:
        return data