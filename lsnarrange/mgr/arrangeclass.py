from django.http import JsonResponse
import json
from common.models import ClassRoom
from common.models import ArrangeResult
from common.models import Course
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
    # data是用户 检索的数据参数
    data = request.params['data']
    # confirm 是用来判断用户是否进行查询
    confirm = request.params['confirm']
    qs = ArrangeResult.objects.values()
    # 根据参数进行过滤
    if 'course_id' in data:
        qs = qs.filter(Course_Id=data['course_id'])
    if 'classroom_id' in data:
        qs = qs.filter(ClassRoom_Id=data['classroom_id'])
    if 'course_beg' in data:
        qs = qs.filter(Course_beg=data['course_beg'])
    if 'course_end' in data:
        qs = qs.filter(Course_end=data['course_end'])

    # 定义参数集合
    Course_Id_set = set({})
    Classroom_Id_set = set({})
    Course_beg_set = set({})
    Course_end_set = set({})
    retlist = []
    # 找到对应的参数
    for dict in qs:
        for key, value in dict.items():
            if key == 'Course_Id':
                Course_Id_set.add(value)
            if key == 'ClassRoom_Id':
                Classroom_Id_set.add(value)
            if key == 'Course_beg':
                Course_beg_set.add(value)
            if key == 'Course_end':
                Course_end_set.add(value)
    # 由于排课结果表中数据较少 所以我们根据ID
    # 将所有结果返回
    if confirm == 1:
        for dict in qs:
            Course_instance = Course.objects.filter(Course_Id=dict['Course_Id'])
            Classroom_instance = ClassRoom.objects.filter(ClassRoom_Id=dict['ClassRoom_Id'])
            middle = list(Classroom_instance.values())[0]
            middle2 = list(Course_instance.values())[0]
            middle.update(middle2)
            # print(middle)
            retlist.append(middle)

    return JsonResponse({'ret': 0, 'retlist': retlist, 'Course_id': list(Course_Id_set),
                         'Classroom_id': list(Classroom_Id_set), 'Course_beg': list(Course_beg_set),
                         'Course_end': list(Course_end_set)})


def autoarrangeresult(request):

    arFirst = AutoArrange(True)
    arLast = AutoArrange(False)

    if arFirst.process() == False and arLast.process() == False :
        return JsonResponse({'ret': 1, 'msg': '自动排课失败'})

    record = ArrangeResult.objects.all().delete()
    for i in arFirst.listResult:
        record = ArrangeResult.objects.create(
            Course_id=i[0],
            ClassRoom_id=i[1],
            Course_beg=i[2],
            Course_end=i[3]
        )
    for i in arLast.listResult:
        record = ArrangeResult.objects.create(
            Course_id=i[0],
            ClassRoom_id=i[1],
            Course_beg=i[2],
            Course_end=i[3]
        )

    record.save()

    return JsonResponse({'ret': 0, 'msg': '自动排课成功'})


def modifyarrangeresult(request):
    # 从请求消息中 获取修改排课结果的信息
    # 找到该排课结果，并且进行修改操作

    course_id = request.params['course_id']
    newdata = request.params['newdata']

    try:
        # 根据课程id 从数据库中找到相应的排课结果
        result = ArrangeResult.objects.get(Course_Id=course_id)
    except ClassRoom.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{course_id}`的课程安排不存在'
        }
    # 如果有该Id的记录
    if 'classroom_id' in newdata:
        result.ClassRoom_Id = newdata['classroom_id']
    if 'course_beg' in newdata:
        result.Course_beg = newdata['course_beg']
    if 'course_end' in newdata:
        result.Course_end = newdata['course_end']

    # 注意，一定要执行save才能将修改信息保存到数据库
    result.save()

    return JsonResponse({'ret': 0})


def deletearrangeresult(request):
    data = request.params['data']
    course_id = data['course_id']

    try:
        # 根据 id 从数据库中找到相应的排课结果记录
        classroom = ArrangeResult.objects.get(Course_Id=course_id)
    except ClassRoom.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{course_id}`的课程安排不存在'
        }
    # delete 方法就将该记录从数据库中删除了
    classroom.delete()

    return JsonResponse({'ret': 0})