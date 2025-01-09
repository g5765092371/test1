from django.db import models

# Create your models here.
# models.py
from django.db import models

class Cloth(models.Model):
    title = models.CharField(max_length=255,null=True)
    category = models.CharField(max_length=255,null=True)
    color = models.CharField(max_length=255,null=True)
    image = models.ImageField(upload_to='myapp/', default='default_image.jpg')  # 设置默认值

    def __str__(self):
        return self.title

class PersonInfo(models.Model):
    # 将 uid 设置为主键
    uid = models.IntegerField(unique=True, primary_key=True)  # 将 uid 作为主键
    name = models.CharField(max_length=100, default="Unknown")
    password = models.CharField(max_length=255, default="Unknown")
    sex = models.CharField(max_length=10, choices=[('Male', '男'), ('Female', '女')], blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)
    province = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    preferences = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    pid = models.IntegerField(primary_key=True)
    postid = models.IntegerField(null=True)
    feature = models.CharField(max_length=255,null=True)
    text = models.TextField(null=True)
    image = models.URLField(null=True)
    look = models.IntegerField(default=0)
    like = models.IntegerField(default=0)

    def __str__(self):
        return f"Post {self.pid}"

class Like(models.Model):
    pid = models.IntegerField(primary_key=True)
    uid = models.IntegerField(null=True)
    postid = models.IntegerField(null=True)

class Look(models.Model):
    uid = models.IntegerField(null=True)
    pid = models.IntegerField(null=True)
