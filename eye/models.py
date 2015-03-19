from django.db import models

class Log(models.Model):
    """
    Transfer original log to corresponding .pd file
    """
    log_path = models.CharField(max_length=200)
    log_name = models.CharField(max_length=100)
    category_key = models.CharField(max_length=100)
    index_time = models.IntegerField(default=0)
    index_type = models.IntegerField(default=8)
    index_sent = models.IntegerField(default=16)
    index_received = models.IntegerField(default=17)
    index_latency = models.IntegerField(default=18)

    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.log_name


class Domain(models.Model):
    """
    Divide a .pd file to domains which distinguished by "category, type, dimension"
    """
    pd_name = models.ForeignKey(Log)
    category_name = models.CharField(max_length=100)
    type_name = models.CharField(max_length=10)

    time_min = models.IntegerField(default=-1)
    time_max = models.IntegerField(default=-1)
    size_min = models.FloatField(default=-1)
    size_max = models.FloatField(default=-1)
    latency_min = models.FloatField(default=-1)
    latency_max = models.FloatField(default=-1)
    total = models.IntegerField(default=-1)
    domain_name = models.CharField(max_length=100,default='null')

    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.pd_name.log_name+"_"+self.category_name+"_"+self.type_name

