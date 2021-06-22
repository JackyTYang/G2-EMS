from django.db import models

# Create your models here.
from django.db import models

class ClassRoom(models.Model):
    # 教室唯一id
    ClassRoom_id = models.IntegerField(primary_key = True, unique=True)

    # 教室名字,如:208
    ClassRoom_Name = models.CharField(max_length=10)

    # 教室容量
    ClassRoom_Capacity = models.IntegerField()

    # 教学楼
    Teaching_Building = models.CharField(max_length=20)

    # 校区
    District = models.CharField(max_length=10)


class Course(models.Model):
    # 课程唯一id
    Course_id = models.IntegerField(primary_key = True, unique=True)

    # 课程名字
    Course_Name = models.CharField(max_length=20)

    # 学分
    Course_Credit = models.FloatField()

    # 教师
    Teacher_Id = models.CharField(max_length=20)

    # 学期
    Course_Term = models.IntegerField()

    # 学年
    Course_Year = models.IntegerField()

    # 课程容量
    Course_Capacity = models.IntegerField()

    # 课程总课时
    Course_Range = models.IntegerField()

    # 介绍
    Introduction = models.CharField(max_length=200)

    # 预修要求
    Requirement = models.CharField(max_length=30)


class ArrangeResult(models.Model):
    # 课程唯一id
    # Course_Id = models.IntegerField(primary_key=True)

    # 外键程唯一id
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # 教室唯一id
    ClassRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    # 课程开始
    Course_beg = models.IntegerField()

    # 课程结束
    Course_end = models.IntegerField()