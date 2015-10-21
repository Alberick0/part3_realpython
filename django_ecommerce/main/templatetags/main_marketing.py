from django import template

register = template.Library()


# This register the func name as a new tag
@register.inclusion_tag('main/templatetags/circle_item.html',
                        takes_context=True)
# declares the HTML that #  is used
def marketing__circle_item(context):
    return context
