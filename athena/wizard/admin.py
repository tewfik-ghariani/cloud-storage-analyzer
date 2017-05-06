from django.contrib import admin
from .models import s3Info
from .models import configObject


admin.site.register(s3Info)
admin.site.register(configObject)
