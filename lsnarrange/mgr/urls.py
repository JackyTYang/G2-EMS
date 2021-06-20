from django.urls import path

from mgr import classroom,arrangeclass

urlpatterns = [

    path('classroom/', classroom.classroomdispatcher),

    path('arrangeclass/',arrangeclass.arrangeclassdispatcher)

]