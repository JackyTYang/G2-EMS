from django.urls import path

from teacher import query

urlpatterns = [

    path('query/', query.listlesson()),#教师查询排课结果

]