from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.http import JsonResponse
import json
from common.models import ClassRoom

# def listclassroom(request):
#     # 获取参数 data是用户检索的数据
#     data = request.params['data']
#     # confirm 是 用来判断用户是否确认查询
#     confirm = request.params['confirm']
#     qs = ClassRoom.objects.values()
#     # 根据data数据 进行过滤
#     if 'id' in data:
#         qs = qs.filter(ClassRoom_Id=data['id'])
#     if 'name' in data:
#         qs = qs.filter(ClassRoom_Name=data['name'])
#     if 'capacity' in data:
#         qs = qs.filter(ClassRoom_Capacity=data['capacity'])
#     if 'building' in data:
#         qs = qs.filter(Teaching_Building=data['building'])
#     if 'district' in data:
#         qs = qs.filter(District=data['district'])
#     # 定义用来返回的数据集合
#     ClassRoom_Id_set = set({})
#     ClassRoom_Name_set = set({})
#     ClassRoom_Capacity_set = set({})
#     Teaching_Building_set = set({})
#     District_set = set({})
#     retlist = []
#     # 根据数据将返回的数据进行统计
#     for dict in qs:
#         for key, value in dict.items():
#             if key == 'ClassRoom_Id':
#                 ClassRoom_Id_set .add(value)
#             if key == 'ClassRoom_Name':
#                 ClassRoom_Name_set.add(value)
#             if key == 'ClassRoom_Capacity':
#                 ClassRoom_Capacity_set.add(value)
#             if key == 'Teaching_Building':
#                 Teaching_Building_set.add(value)
#             if key == 'District':
#                 District_set.add(value)
#     if confirm == 1:
#            retlist = list(qs)
#     # retlist 是用来返回的查询结果 其他都是 应该提示用户的参数
#     return JsonResponse({'ret': 0, 'retlist': retlist, 'classroom_id': list(ClassRoom_Id_set),
#                          'classroom_name': list(ClassRoom_Name_set), 'classroom_capacity': list( ClassRoom_Capacity_set),
#                          'teaching_building': list(Teaching_Building_set),'district':list(District_set)})

def initialaddclassroom(request):
    return render(request, '添加教室信息.html')

def initialmodifyclassroom(request):
    return render(request,'修改教室信息.html')

def initialmodifylesson(request):
    return render(request,'手动课程调整.html')

def initialautoarrange(request):
    return render(request,'自动排课.html')

def initialquerylesson(request):
    return render(request,'排课结果查询-条件查询.html')

def initialqueryclassroom(request):
    return render(request,'查询教室课表.html')

def listclassroom(request):
    # # 获取参数 data是用户检索的数据
    # data = request.POST['data']
    # confirm 是 用来判断用户是否确认查询
    qs = ClassRoom.objects.all()
    # 根据data数据 进行过滤
    if 'name' in request.GET and request.GET['name'] != "":
        qs = qs.filter(ClassRoom_Name=request.GET['name'])
    if 'building' in request.GET and request.GET['building'] != "":
        qs = qs.filter(Teaching_Building=request.GET['building'])
    if 'district' in request.GET and request.GET['district'] != "":
        qs = qs.filter(District=request.GET['district'])

    # retlist = list(qs)
    # print(retlist)
    # # 定义用来返回的数据集合
    # """
    # ClassRoom_Id_set = set({})
    # ClassRoom_Name_set = set({})
    # ClassRoom_Capacity_set = set({})
    # Teaching_Building_set = set({})
    # District_set = set({})
    # """
    # retlist = []
    # # 根据数据将返回的数据进行统计
    # retlist = list(qs)
    # retlist 是用来返回的查询结果 其他都是 应该提示用户的参数
    return render(request, '修改教室信息.html', {'retlist': qs})


def addclassroom(request):
    # info    = request.params['data']


    # 从请求消息中 获取要添加教室的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = ClassRoom.objects.create(ClassRoom_Name=request.POST['name'] ,
                            ClassRoom_id=request.POST['id'] ,
                            ClassRoom_Capacity=request.POST['capacity'],
                            Teaching_Building=request.POST['building'],
                            District=request.POST['district'])

    return render(request, '添加教室信息.html')
    # return JsonResponse({'ret': 0, 'id':record.ClassRoom_id})


def modifyclassroom(request):
    # 从请求消息中 获取修改教室的信息
    # 找到该教室，并且进行修改操作

    classroomid = request.params['classroom_id']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        classroom = ClassRoom.objects.get(ClassRoom_Id=classroomid)
    except ClassRoom.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{classroomid}`的教室不存在'
        }
    if 'id' in newdata:
        classroom.ClassRoom_Id = newdata['id']
    if 'name' in newdata:
        classroom.ClassRoom_Name = newdata['name']
    if 'capacity' in newdata:
        classroom.ClassRoom_Capacity = newdata['capacity']
    if 'building' in newdata:
        classroom.Teaching_Building = newdata['building']
    if 'district' in newdata:
        classroom.District = newdata['district']

    # 注意，一定要执行save才能将修改信息保存到数据库
    classroom.save()
    return JsonResponse({'ret': 0})


def deleteclassroom(request):

    classroomid = request.GET['courseid']

    try:
        # 根据 id 从数据库中找到相应的教室记录
        classroom = ClassRoom.objects.get(ClassRoom_id=classroomid)
    except ClassRoom.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{classroomid}`的教室不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    classroom.delete()

    # , {'retlist': qs}
    return render(request, '修改教室信息.html')