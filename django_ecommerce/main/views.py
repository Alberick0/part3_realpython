from django.shortcuts import render_to_response, RequestContext

from payments.models import User
from main.models import MarketingItem, StatusReport


def index(request):
    uid = request.session.get('user')

    # main landing page
    marketing_items = MarketingItem.objects.all()

    if uid is None:
        return render_to_response('main/index.html',
                                  {'marketing_items': marketing_items})
    else:
        status = StatusReport.objects.all().order_by('-when')[:20]

        return render_to_response(
            'main/user.html', {'user': User.get_by_id(uid),
                               'reports': status
                               },
            context_instance=RequestContext(request)
        )


def report(request):
    if request.method == 'POST':
        status = request.POST.get('status', '')

        # update the database with the status
        if status:
            uid = request.session.get('user')
            user = User.get_by_id(uid)
            StatusReport(user=user, status=status).save()

        # always return something
        return index(request)
