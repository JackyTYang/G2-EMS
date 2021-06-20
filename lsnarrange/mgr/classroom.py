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
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = ClassRoom.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)


    return JsonResponse({'ret': 0, 'retlist': retlist})


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