from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from mainsite import models
from datetime import date
from moviepy.editor import VideoFileClip
from django.contrib import messages
import os
import time
from . import final, img_effect, highlight_video_effect, music_slow

from django.conf import settings
MediaFilePath = settings.MEDIA_ROOT
n = 0
filename = ""
TargetDir = ""

# Create your views here.
def index(request, no=0):
	no = no
	if no==0:
		messages.add_message(request, messages.WARNING, '請選擇影片類型') 
	elif request.method=="POST":
		# try:
			uploaded_file = request.FILES['file']
			fss = FileSystemStorage()
			file = fss.save(uploaded_file.name, uploaded_file)
			print("Uploading file ",uploaded_file.name)
			if no == 2:
				duration = VideoFileClip(MediaFilePath +"/"+ uploaded_file.name).duration
				duration = round(duration)
				duration_h = duration/3600
				duration = duration%3600
				duration_m = duration/60
				duration_s = duration%60
				models.VideoDetail.objects.create(user=request.user, video_name=uploaded_file.name, pub_time=date.today(), duration_h=duration_h, duration_m=duration_m, duration_s=duration_s)
				record_days = models.RecordDays.objects.get(user=request.user)
				last_day = record_days.last_day
				end = date.today()
				interval = (end - last_day).days
				absent_days = record_days.absent_days
				attend_days = record_days.attend_days
				max_continue_days = record_days.max_continue_days
				if absent_days == 0 and interval != 0:
					attend_days = attend_days + 1
					if max_continue_days < attend_days:
						max_continue_days = attend_days
				else:
					absent_days = 0
					attend_days = 1
				models.RecordDays.objects.filter(user=request.user).update(absent_days=absent_days, attend_days=attend_days, max_continue_days=max_continue_days, last_day=date.today())
				
			# messages.add_message(request, messages.SUCCESS, '上傳成功') 
			global n
			n = no
			return redirect("../../process/")
		# except:
			messages.add_message(request, messages.WARNING, '請上傳影片')
	mediafiles = os.listdir(MediaFilePath)
	return render(request, "skill_train/index.html", locals())

def process(request):
	return render(request, "skill_train/process.html", locals())

def result(request, edit=0):
	edit = edit
	mediafiles = os.listdir(MediaFilePath)
	mediafiles = sorted(mediafiles,key=lambda x: os.path.getmtime(os.path.join(MediaFilePath, x)))

	file =  mediafiles[len(mediafiles)-1]
	global filename
	filename = file

	global TargetDir
	if n == 1:
		TargetDir = "game_highlight"
	elif n == 2:
		TargetDir = "self_practice_highlight"

	(scores, misses) = final.main(file, TargetDir)
	scores = 1
	misses = 0

	if n == 2:
		accuracy = scores/(scores+misses)*100
		accuracy = int(accuracy+0.5)
		models.VideoDetail.objects.filter(user=request.user).filter(video_name=filename).update(accuracy=accuracy)
		record_accuracy = models.RecordAccuracy.objects.get(user=request.user)
		total_game = record_accuracy.total_game
		average_accuracy = record_accuracy.average_accuracy
		average_accuracy = (total_game*average_accuracy+accuracy)/(total_game+1)
		total_game = total_game+1
		models.RecordAccuracy.objects.filter(user=request.user).update(total_game=total_game, average_accuracy=average_accuracy)

	highlight_video_path = MediaFilePath + "/" + TargetDir

	highlightfiles = os.listdir(highlight_video_path)
	highlightfiles = sorted(highlightfiles,key=lambda x: os.path.getmtime(os.path.join(highlight_video_path, x)))
	
	empty = 0
	if len(highlightfiles)==0:
		empty = 1
	else:
		highlight_video = highlightfiles[len(highlightfiles)-1]
		if highlight_video == ".DS_Store":
			if len(highlightfiles) > 1:
				highlight_video = highlightfiles[len(highlightfiles)-2]
				relative_path = "/" + TargetDir + "/{{ highlight_video }}"
			else:
				empty = 1

	print("TargetDir:",TargetDir)

	targetdir = TargetDir

	return render(request, "skill_train/result.html", locals())

def filter(request, s=0, f=0, m=0):
	s = s
	f = f
	m = m
	img_effect.main(f, filename)

	return render(request, "skill_train/edit_filter.html", locals())

def filter_process(request, s=0, f=0, m=0):
	s = s
	f = f
	m = m
	return render(request, "skill_train/filter_process.html", locals())

def download(request, s=0, f=0, m=0):
	s = s
	f = f
	m = m

	highlight_video_effect.main(f, TargetDir, filename)

	musicdir = MediaFilePath + "/../static/music"
	music_slow.main(s, m, musicdir, filename)


	filtered_path = MediaFilePath + "/filtered_videos"

	highlightfiles = os.listdir(filtered_path)
	highlightfiles = sorted(highlightfiles,key=lambda x: os.path.getmtime(os.path.join(filtered_path, x)))

	file =  highlightfiles[len(highlightfiles)-1]

	targetdir = TargetDir

	return render(request, "skill_train/filtered_result.html", locals())

	

