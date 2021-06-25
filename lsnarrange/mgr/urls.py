from django.urls import path

from mgr import classroom,arrangeclass

urlpatterns = [

    # path('classroom/', classroom.classroomdispatcher),

    path('arrangeclass/',arrangeclass.arrangeclassdispatcher),

    path('add_classroom/',classroom.addclassroom),
    #
    path('list_classroom',classroom.listclassroom),

    path('modify_classroom',classroom.modifyclassroom),

    path('delete_classroom',classroom.deleteclassroom)


]