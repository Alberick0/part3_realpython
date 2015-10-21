from django import template

register = template.Library()


# This register the func name as a new tag
@register.inclusion_tag('main/templatetags/circle_item.html')
# declares the HTML that #  is used
def circle_header_item(img_name='yoda.jpg', heading='yoda', caption='yoda',
                       button_link='register', button_title='View details'):
    return {
        'img': img_name,
        'heading': heading,
        'caption': caption,
        'button_link': button_link,
        'button_title': button_title
    }
