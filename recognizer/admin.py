from django.contrib import admin

# Register your models here.
from .models import *




class DataAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'time_upload', 'class_by_recognizer', 'class_by_user')
    list_editable = ('class_by_user',)
    list_filter = ('class_by_user', 'class_by_recognizer', 'time_upload', 'id' )

admin.site.register(Data, DataAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_upload', 'feedback')
    list_filter = ('name', 'time_upload', 'id' )

admin.site.register(Feedback, FeedbackAdmin)