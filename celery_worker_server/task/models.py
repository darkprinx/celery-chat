from django.db import models


class FinishedTask(models.Model):
    message = models.CharField(max_length=100)
