from django.contrib import admin
from .models import VideoDetail, RecordDays, RecordAccuracy
# Register your models here.
class VideoDetailAdmin(admin.ModelAdmin):
	list_display = ('video_name', 'pub_time')
		
admin.site.register(VideoDetail, VideoDetailAdmin)
admin.site.register(RecordDays)
admin.site.register(RecordAccuracy)
