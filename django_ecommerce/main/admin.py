from django.contrib import admin
from .models import StatusReport, Announcement, MarketingItem


admin.site.register(StatusReport)
admin.site.register(Announcement)
admin.site.register(MarketingItem)
