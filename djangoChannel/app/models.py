from distutils.text_file import TextFile
from email import message
from django.db import models

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Chat(models.Model):
    UserName = models.CharField(max_length=100)
    content = models.TextField()
    groupName = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.UserName + ': ' + self.content 
