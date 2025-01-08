from django.db import models

# Create your models here.
# models.py
from django.db import models

class Cloth(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    image = models.ImageField(upload_to='myapp/', default='default_image.jpg')  # 设置默认值

    def __str__(self):
        return self.title

class PersonInfo(models.Model):
    name = models.CharField(max_length=100, default="Unknown")
    password = models.CharField(max_length=255, default="Unknown")
    sex = models.CharField(max_length=10, choices=[('Male', '男'), ('Female', '女')], blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)
    province = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    weather = models.CharField(max_length=100, blank=True, default='晴')

class Post(models.Model):
    pid = models.AutoField(primary_key=True)  # 自动递增字段，通常作为主键
    uid = models.IntegerField()
    feature = models.CharField(max_length=255)
    text = models.TextField()
    image = models.URLField()
    look = models.IntegerField(default=0)
    like = models.IntegerField(default=0)

    def __str__(self):
        return f"Post {self.pid}"
