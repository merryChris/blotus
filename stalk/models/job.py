from django.db import models
from lolly import Lolly

class Job(Lolly):
    job_id = models.CharField(max_length=40)
    project = models.CharField(max_length=20, null=True)
    spider = models.CharField(max_length=20, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'job'
        unique_together = ('job_id', 'project', 'spider')
