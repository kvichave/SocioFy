from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserSocial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # social_auth = models.ForeignKey(UserSocialAuth, on_delete=models.CASCADE)
    social_app=models.CharField(max_length=100)  
    data=models.CharField(max_length=99999,default="None")
    page_id=models.IntegerField(max_length=999,default=000)

    

