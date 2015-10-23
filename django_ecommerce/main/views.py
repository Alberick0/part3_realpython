from datetime import date, timedelta
from django.shortcuts import render_to_response, RequestContext

from payments.models import User
from main.models import MarketingItem, StatusReport, Announcement


def index(request):
    uid = request.session.get('user')

    # main landing page

    if uid is None:
        marketing_items = MarketingItem.objects.all()
        return render_to_response('main/index.html',
                                  {'marketing_items': marketing_items})
    else:
        status = StatusReport.objects.all().order_by('-when')[:20]
        announce_date = date.today() - timedelta(days=30)
        announce = Announcement.objects.filter(
            when__gt=announce_date).order_by('-when')
        # the above grabs and order all the announcements in the last 30 days

        return render_to_response(
            'main/user.html', {'user': User.get_by_id(uid),
                               'reports': status,
                               'announce': announce},
            context_instance=RequestContext(request))
        # context was added because our template includes csrf_token


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
