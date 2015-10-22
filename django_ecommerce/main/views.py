from django.shortcuts import render_to_response

from payments.models import User
from main.models import MarketingItem


def index(request):
    uid = request.session.get('user')
    marketing_items = MarketingItem.objects.all()

    if uid is None:
        return render_to_response('main/index.html',
                                  {'marketing_items': marketing_items})
    else:
        return render_to_response(
            'main/user.html', {'user': User.get_by_id(uid),
                               'marketing_items': marketing_items}
        )
