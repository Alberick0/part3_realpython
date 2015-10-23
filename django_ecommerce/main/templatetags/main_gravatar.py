from django import template
from urllib.parse import urlencode
import hashlib

register = template.Library()


@register.simple_tag
def gravatar_img(email, size=140):
    url = get_url(email, size)

    return ''''<img class="img-circle" src="%s" height="%s"
     width="%s" 12 alt="user.avatar" />''' % (url, size, size)


def get_url(email, size=140):
    default = 'http://upload.wikimedia.org/wikipedia/en/9/9b/' \
              'Yoda_Empire_Strikes_Back.png'

    # query params, urlencode provides character scaping
    query_params = urlencode([('s', str(size)),  # size of image to return
                              ('d', default)])  # default image in case

    grava_url = 'http://www.gravatar.com/avatar/'

    return (grava_url + hashlib.md5(  # email is required to be hashed
        email.lower().encode('utf-8')).hexdigest() + '?' + query_params)


if __name__ == '__main__':
    print(gravatar_img('jeanalberick@gmail.com'))
