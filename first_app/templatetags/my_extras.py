from django import template

register = template.Library()

def cut(value,arg):
    """
    This cuts out value of "arg" from the string!
    """
    return value.replace(arg,'')

# you can use decoration(annotation) instead of this
register.filter('cut',cut)

@register.filter(name='cut_and_add')
def cut_and_add(value,arg):
    """
    This cut out all value of "arg" from the string and add it in the end!
    """
    return value.replace(arg,'') + arg
