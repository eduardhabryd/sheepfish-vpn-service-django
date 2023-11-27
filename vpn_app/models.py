from django.db import models
from django.contrib.auth import get_user_model


class Site(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    page_views = models.IntegerField(default=0)
    data_sent = models.FloatField(default=0)
    data_received = models.FloatField(default=0)
    last_view = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-last_view']
