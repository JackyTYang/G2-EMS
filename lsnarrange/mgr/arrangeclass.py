from django.http import JsonResponse
import json
from common.models import ClassRoom
from common.models import ArrangeResult
from mgr.autoarrange import AutoArrange


def arrangeclassdispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_arrangeresult':
        return listarrangeresult(request)
    elif action == 'modify_arrangeresult':
        return modifyarrangeresult(request)
    elif action == 'auto_arrangeresult':
        return autoarrangeresult(request)
    elif action == 'del_arrangeresult':
        return deletearrangeresult(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


# 以下为对排课的操作，本子系统核心部分
def listarrangeresult(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = ClassRoom.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})


def autoarrangeresult(request):
    ar = AutoArrange()
    if ar.process() == False:
        return JsonResponse({'ret': 1, 'msg': '自动排课失败'})

    record = ArrangeResult.objects.all().delete()
    for i in ar.listResult:
        record = ArrangeResult.objects.create(
            Course_Id=i[0],
            ClassRoom_Id=i[1],
            Course_beg=i[2],
            Course_end=i[3]
        )

    record.save()

    return JsonResponse({'ret': 0, 'retlist': ar.listResult})


def modifyarrangeresult(request):
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


def deletearrangeresult(request):
    classroomid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        classroom = ClassRoom.objects.get(id=classroomid)
    except ClassRoom.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{classroomid}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    classroom.delete()

    return JsonResponse({'ret': 0})
