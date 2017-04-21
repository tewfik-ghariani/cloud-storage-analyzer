from django.db import models
from django.contrib.auth.models import User
# Create your models here.


'''

class Account(models.Model):
    user = models.OneToOneField(User)  #to extend the User built-in module
    site_web = models.URLField(blank=True)
    #avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    signature = models.TextField(blank=True)
    

    def __str__(self):
        return "Profil of {0}".format(self.user.username)
'''