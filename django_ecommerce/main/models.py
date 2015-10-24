from django.db import models


class MarketingItem(models.Model):
    img = models.CharField(max_length=255)
    heading = models.CharField(max_length=300)
    caption = models.TextField()
    button_link = models.URLField(null=True, default='register')
    button_title = models.CharField(max_length=20, default='View details')


class StatusReport(models.Model):
    # if foreign key we can reference a model with a string
    user = models.ForeignKey('payments.User')  # done this way to avoid cir ref
    when = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200)


class Announcement(models.Model):
    when = models.DateTimeField(auto_now=True)
    img = models.CharField(max_length=25, null=True)
    vid = models.URLField(null=True, blank=True)
    info = models.TextField()

    # class Meta:
    #     verbose_name_plural = "Announcements"  # fixes typo in admin


class Badge(models.Model):
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    desc = models.TextField()

    class Meta:
        ordering = ('name',)
