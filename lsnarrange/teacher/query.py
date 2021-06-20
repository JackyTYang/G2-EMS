from django.http import JsonResponse
import json
from  common.models import ClassRoom #该引入的表需改为新的排课结果文件

def listlesson(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = ClassRoom.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})