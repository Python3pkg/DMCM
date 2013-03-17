from django.db import models


class Log(models.Model):
    level = models.CharField(max_length=10)
    msg = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['-datetime']
