from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name



class Room(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)  
    host  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    decription = models.TextField()
    participant = models.ManyToManyField(User, related_name='participants' )
    created = models.DateTimeField(auto_now= True)
    updated = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.name


class message(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    body = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now= True)
    updated = models.DateTimeField(auto_now_add= True)


    class Meta:
        ordering=['-created', '-updated']


    def __str__(self):
        return self.body











