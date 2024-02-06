from django import template


register = template.Library()


@register.filter(name="clear_if_placeholder", is_safe=True)
def clearIfPlaceholder(value):
    if "placeholder_" in value:
        return ""
    else:
        return value
