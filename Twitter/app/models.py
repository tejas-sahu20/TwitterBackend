from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Tweets(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='tweets')
    tweet = models.TextField()
    # text = models.TextField()
    def __str__(self):
        return self.user.name

class Comments(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='comments')
    tweet = models.ForeignKey(Tweets, on_delete=models.CASCADE,related_name='comments')
    text = models.TextField()
    def __str__(self):
        return self.user.name