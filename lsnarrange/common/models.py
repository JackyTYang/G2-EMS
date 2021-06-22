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
    Course_id = models.IntegerField(primary_key= True)  #课程号
    name = models.CharField(max_length=20)  #课程名
    credit = models.DecimalField(max_digits = 2, decimal_places = 1)  #课程学分
    capacity = models.IntegerField()  #课程容量
    teacher_id = models.IntegerField()  #教师号
    teacher_name = models.CharField(max_length=10)  #教师名
    term = models.CharField(max_length = 10) #春 夏 秋 秋冬 春夏 短 冬
    year = models.IntegerField() #年份
    range = models.IntegerField() #课时
    #arrangeresult 不能修改


class ArrangeResult(models.Model):
    # 课程唯一id
    # 外键 会自动在后面加上一个id
    Course = models.ForeignKey(Course,on_delete=models.CASCADE)

    # 教室唯一id
    ClassRoom = models.ForeignKey(ClassRoom,on_delete=models.CASCADE)

    # 课程开始
    Course_beg = models.IntegerField()

    # 课程结束
    Course_end = models.IntegerField()