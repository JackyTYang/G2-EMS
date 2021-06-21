from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.http import JsonResponse
import json
from  common.models import ClassRoom

def classroomdispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST','PUT','DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)


    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_classroom':
        return listclassroom(request)
    elif action == 'add_classroom':
        return addclassroom(request)
    elif action == 'modify_classroom':
        return modifyclassroom(request)
    elif action == 'del_classroom':
        return deleteclassroom(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def listclassroom(request):
    # 获取参数 data是用户检索的数据
    data = request.params['data']
    # confirm 是 用来判断用户是否确认查询
    confirm = request.params['confirm']
    qs = ClassRoom.objects.values()
    # 根据data数据 进行过滤
    if 'id' in data:
        qs = qs.filter(ClassRoom_Id=data['id'])
    if 'name' in data:
        qs = qs.filter(ClassRoom_Name=data['name'])
    if 'capacity' in data:
        qs = qs.filter(ClassRoom_Capacity=data['capacity'])
    if 'building' in data:
        qs = qs.filter(Teaching_Building=data['building'])
    if 'district' in data:
        qs = qs.filter(District=data['district'])
    # 定义用来返回的数据集合
    ClassRoom_Id_set = set({})
    ClassRoom_Name_set = set({})
    ClassRoom_Capacity_set = set({})
    Teaching_Building_set = set({})
    District_set = set({})
    retlist = []
    # 根据数据将返回的数据进行统计
    for dict in qs:
        for key, value in dict.items():
            if key == 'ClassRoom_Id':
                ClassRoom_Id_set.add(value)
            if key == 'ClassRoom_Name':
                ClassRoom_Name_set.add(value)
            if key == 'ClassRoom_Capacity':
                ClassRoom_Capacity_set.add(value)
            if key == 'Teaching_Building':
                Teaching_Building_set.add(value)
            if key == 'District':
                District_set.add(value)
    if confirm == 1:
        retlist = list(qs)
    # retlist 是用来返回的查询结果 其他都是 应该提示用户的参数
    return JsonResponse({'ret': 0, 'retlist': retlist, 'classroom_id': list(ClassRoom_Id_set),
                         'classroom_name': list(ClassRoom_Name_set), 'classroom_capacity': list(ClassRoom_Capacity_set),
                         'teaching_building': list(Teaching_Building_set), 'district': list(District_set)})


def addclassroom(request):

    info    = request.params['data']

    # 从请求消息中 获取要添加教室的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = ClassRoom.objects.create(ClassRoom_Name=info['name'] ,
                            ClassRoom_Id=info['id'] ,
                            ClassRoom_Capacity=info['capacity'],
                            Teaching_Building=info['building'],
                            District=info['district'])


    return JsonResponse({'ret': 0, 'id':record.id})


def modifyclassroom(request):
    # 从请求消息中 获取修改教室的信息
    # 找到该教室，并且进行修改操作

    classroomid = request.params['id']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        classroom = ClassRoom.objects.get(id=classroomid)
    except ClassRoom.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{classroomid}`的教室不存在'
        }

    if 'name' in newdata:
        classroom.ClassRoom_Name = newdata['name']
    if 'capacity' in newdata:
        classroom.ClassRoom_Capacity = newdata['capacity']
    if 'building' in newdata:
        classroom.Teaching_Building = newdata['building']
    if 'district' in newdata:
        classroom.District = newdata['district']

    # 注意，一定要执行save才能将修改信息保存到数据库
    ClassRoom.save()

    return JsonResponse({'ret': 0})


def deleteclassroom(request):

    classroomid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        classroom = ClassRoom.objects.get(id=classroomid)
    except ClassRoom.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{classroomid}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    classroom.delete()

    return JsonResponse({'ret': 0})