from django.db import models


# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=100)
    publish_date = models.DateTimeField(auto_now=True)

    def poll_items(self):
        pass


class PollItem(models.Model):
    poll = models.ForeignKey(Poll, related_name='items')
    name = models.CharField(max_length=30)
    text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0
    )

    class Meta:
        ordering = ['-text']
