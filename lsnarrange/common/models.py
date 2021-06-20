from django.db import models

# Create your models here.
from django.db import models

class ClassRoom(models.Model):
    # 教室唯一id
    ClassRoom_Id = models.IntegerField(primary_key = True)

    # 教室名字,如:208
    ClassRoom_Name = models.CharField(max_length=10)

    # 教室容量
    ClassRoom_Capacity = models.IntegerField()

    # 教学楼
    Teaching_Building = models.CharField(max_length=20)

    # 校区
    District = models.CharField(max_length=10)
