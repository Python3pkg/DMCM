from datetime import datetime, timedelta
from django.db import models

RECENT = timedelta(days=1)


class Log(models.Model):
    level = models.CharField(max_length=10)
    msg = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['-datetime']

    def recent(self):
        now = datetime.now()
        recent = self.datetime > (now - RECENT) 
        return recent
