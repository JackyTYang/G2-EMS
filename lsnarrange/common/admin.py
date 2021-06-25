from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import ClassRoom
from .models import Course
from .models import ArrangeResult

admin.site.register(ClassRoom)
admin.site.register(Course)
admin.site.register(ArrangeResult)