from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(SubjectCombination)
admin.site.register(Result)
admin.site.register(Notice)