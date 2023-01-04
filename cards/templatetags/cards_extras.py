from django import template 
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def get_contrast_color(value):
    red, green, blue = tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))
    
    if (red * 0.299 + green * 0.587 + blue * 0.114) > 150:
        return '#000000'
    else:
        return '#FFFFFF'