from django.db import models

# Create your models here.
HTML_TYPES = (
    ('text', 'text'),
    ('number', 'number'),
    ('date', 'date'),
)

ATHENA_TYPES = (
    ('string', 'string'),
    ('tinyint', 'tinyint'),
    ('smallint', 'smallint'),
    ('int', 'int'),
    ('bigint', 'bigint'),
    ('boolean', 'boolean'),
    ('float', 'float'),
    ('double', 'double'),
    ('array', 'array'),
    ('map', 'map'),
    ('timestamp', 'timestamp'),
)


class genericSchema(models.Model):
    attribute = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices = ATHENA_TYPES)
    html_type = models.CharField(max_length=20, choices = HTML_TYPES)


    def __str__(self):
        return self.attribute
    class Meta:
       abstract = True


class testSchema(genericSchema):
    pass


