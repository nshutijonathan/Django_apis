from django.db import models

# Create your models here.
from django.db import models


class MyFriendList(models.Model):
    friend_name = models.CharField(max_length=200)
    mobile_no = models.IntegerField()
