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
def Time_String_to_int(s):
    s=s.strip()
    day_dict = {"周一":0,"周二":1,"周三":2,"周四":3,"周五":4,"周六":5,"周日":6}
    beg = int(s[2])
    end = int(s[s.find("节")-1])
    number = day_dict[s[0:2]]
    beg += number*13
    end += number*13
    print(beg,end)
    return [beg,end]
def Time_int_to_String( beg, end):
    day_number = beg/13
    return_result=""
    day_dict={0:"周一",1:"周二",2:"周三",3:"周四",4:"周五",5:"周六",6:"周日"}
    return_result=day_dict[day_number]
    while(end-beg!=0):
        return_result+=str(beg)+','
        beg+=1
    return_result+=str(end)+"节"
    return return_result
# 以下为对排课的操作，本子系统核心部分
def listarrangeresult(request):
    # data是用户 检索的数据参数
    data = request.params['data']
    # confirm 是用来判断用户是否进行查询
    qs = ArrangeResult.objects.values()
    # 根据参数进行过滤
    retlist = []
    if 'id' in data:
        qs = qs.filter(Course_beg=data['id'])
    if 'begin' in data:
        qs = qs.filter(Course_beg=data['begin'])
    if 'end' in data:
        qs = qs.filter(Course_end=data['end'])
    for dict in qs:
            Course_instance = Course.objects.filter(Course_id=dict['Course_id'])
            Classroom_instance = ClassRoom.objects.filter(ClassRoom_id=dict['ClassRoom_id'])
            print(Classroom_instance.values())
            middle = list(Classroom_instance.values())[0]
            middle2 = list(Course_instance.values())[0]
            if 'building' in data and middle['Teaching_Building'] == data['building']:
                if 'classroom' in data and middle['ClassRoom_Name'] == data['classroom']:
                    if 'year' in data and middle['year'] == data['year']:
                        if 'term' in data and middle['term'] == data['term']:
                            if 'course_id' in data and middle2['Course_id'] == data['classroom_id']:
                                 if 'district' in data and middle2['District'] == data['district']:
                                    if 'teacher' in data and middle2['teacher_name'] == data['teacher']:
                                        if'name' in data and middle2['name']  ==  data['name']:
                                          middle.update(middle2)
                                          print(middle2)
                                          middle["New_time"] = Time_int_to_String(data['begin'],data['end'])
                                          retlist.append(middle)
    return JsonResponse({'ret': 0, 'retlist': retlist })
"""
    # 定义参数集合
    Course_Id_set = set({})
    Classroom_Id_set = set({})
    Course_beg_set = set({})
    Course_end_set = set({})
    retlist = []

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
"""
# 由于排课结果表中数据较少 所以我们根据ID
# 将所有结果返回


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
   # course_id = request.params['course_id']
    newdata = request.params['newdata']
    course_id = newdata['course_id']
    result = ArrangeResult.objects.filter(Course_id= course_id)
    result = list(result.values())
    print(type(result))
    print(result)
    Classroom_id = result[0]["ClassRoom_id"]
    Course_begin = result[0]["Course_beg"]
    Course_end   = result[0]["Course_end"]
    print(Classroom_id)
 # 如果有该Id的记录
    """
    if 'classroom_id' in newdata:
        result.ClassRoom_Id = newdata['classroom_id']
    """
    # 注意，一定要执行save才能将修改信息保存到数据库
    result = ArrangeResult.objects.get(Course_id=course_id)
    qs = ArrangeResult.objects.values()
    qs =qs.filter(ClassRoom_id= Classroom_id)
    judge = 1;
    Course_begin = newdata['begin']
    Course_end   = newdata['end']
    for dict in qs:
        #print(dict)
        if dict['Course_beg'] > Course_end or dict['Course_end'] < Course_begin or dict['Course_id'] == course_id :
            continue
        else :
            judge =0;
    if judge == 1:
        result.Course_beg = Course_begin;
        result.Course_end = Course_end;
        result.ClassRoom_id = Classroom_id;
        #print(Course_begin,Course_end)
        result.save()
    else :
        return JsonResponse({'ret': 1})
    return JsonResponse({'ret': 0})

def deletearrangeresult(request):
    data = request.params['data']
    course_id = data['course_id']

    try:
        # 根据 id 从数据库中找到相应的排课结果记录
        classroom = ArrangeResult.objects.get(Course_id=course_id)
    except ClassRoom.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{course_id}`的课程安排不存在'
        }
    # delete 方法就将该记录从数据库中删除了
    classroom.delete()

    return JsonResponse({'ret': 0})
