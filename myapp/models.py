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
    sex = models.CharField(max_length=10, choices=[('Male', '男'), ('Female', '女')])
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    weather = models.CharField(max_length=100,default='晴')