from django.db import models
from django.contrib.postgres.fields import JSONField

AWS_REGIONS = (
    ('us-east-1', 'us-east-1'),
    ('us-east-2', 'us-east-2'),
    ('us-west-1', 'us-west-1'),
    ('us-west-2', 'us-west-2'),
    ('ap-south-1', 'ap-south-1'),
    ('ap-northeast-1', 'ap-northeast-1'),
    ('ap-northeast-2', 'ap-northeast-2'),
    ('ap-southeast-1', 'ap-southeast-1'),
    ('ap-southeast-2', 'ap-southeast-2'),
    ('eu-central-1', 'eu-central-1'),
    ('eu-west-1', 'eu-west-1'),
    ('eu-west-2', 'eu-west-2'),
)

TYPES = (
    ('private', 'private'),
    ('public', 'public'),
)


class s3Info(models.Model):
    label = models.CharField(max_length=50)
    shortcut = models.CharField(max_length=20)
    bucket_name = models.CharField(max_length=50, unique=True)
    bucket_region = models.CharField(max_length=20, choices=AWS_REGIONS)
    type = models.CharField(max_length=10, choices=TYPES)

    def __str__(self):
        return self.label


class configObject(models.Model):
    name = models.CharField(max_length=50)
    customer = models.ForeignKey(s3Info)
    headers = JSONField()
    fieldsFDV = JSONField()

    def __str__(self):
        return self.name + ' in ' + self.customer.label
