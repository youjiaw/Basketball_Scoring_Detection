from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import forms, models, future_game, weather
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth 
from django.contrib.auth.decorators import login_required
from datetime import date

# Create your views here.

def login(request):
	if request.method =='POST':
		login_form = forms.LoginForm(request.POST)
		if login_form.is_valid():
			login_name = request.POST['username'].strip()
			login_password = request.POST['password']
			user = authenticate(username = login_name, password = login_password)
			if user is not None:
				if user.is_active:
					auth.login(request, user)
					try:
						record_days = models.RecordDays.objects.get(user=user)
					except:
						record_days = models.RecordDays(user=user)
						record_days.save()
					try:
						record_accuracy = models.RecordAccuracy.objects.get(user=user)
					except:
						record_accuracy = models.RecordAccuracy(user=user)
						record_accuracy.save()
					return redirect('/')
				else:
					messages.add_message(request, messages.WARNING, '帳號尚未啟用')
			else:
				messages.add_message(request, messages.WARNING, '登入失敗')
		else:
			messages.add_message(request, messages.INFO, '請檢查輸入的欄位內容')
	else:
		login_form = forms.LoginForm()
	return render(request, 'login.html', locals())

def index(request):
	country = weather.target_country
	phenomenon, max_t, min_t, comfort_level, rainy_prob = weather.getWeather(weather.url)
	comfort_level = int(comfort_level)
	pm25_level, time = weather.getPM2dot5(weather.pm_url)
	pm25_len = len(pm25_level)
	games = future_game.get_NBA_schedule('2021')
	if request.user.is_authenticated:
		user = request.user
		return render(request, 'homepage_login.html', locals())
	else:
		return render(request, 'homepage_logout.html', locals())
	
def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
	return redirect('/')

def tracking(request):
	if request.user.is_authenticated:
		# try:
			# record_days = models.RecordDays.objects.get(user=request.user)
			# start = record_days.last_day
			# end = datetime.now()
			# interval = (end-start).days  
			# if interval != 0:
			# 	record_days.update(absent_days=interval, attend_days=0)
		# except:
		# 	return redirect('/except')
		username = request.user.username
		record_days = models.RecordDays.objects.get(user=request.user)
		start = record_days.last_day
		end = date.today()
		interval = (end-start).days  
		if interval != 0:
			models.RecordDays.objects.filter(user=request.user).update(absent_days=interval, attend_days=0, last_day=end)
		videos = models.VideoDetail.objects.filter(user=request.user)
		pub_time_list = []
		accuracy_list = []
		for video in videos:
			pub_time_list.append(str(video.pub_time))
			accuracy_list.append(video.accuracy)
		return render(request, 'tracking.html', locals())
	else:
		return redirect('/')

def compare(request, no=0):
	if request.user.is_authenticated:
		user = request.user
		if no == 1:
			my_accuracy = models.RecordAccuracy.objects.get(user=user).average_accuracy
			others_accuracys = models.RecordAccuracy.objects.all().order_by('-average_accuracy')
			accuracys = []
			for others_accuracy in others_accuracys:
				accuracys.append(others_accuracy.average_accuracy)
		if no == 2 : 
			my_days = models.RecordDays.objects.get(user=user).max_continue_days
			others_days = models.RecordDays.objects.all().order_by('-max_continue_days')
			days = []
			for others_day in others_days:
				days.append(others_day.max_continue_days)
		return render(request, 'compare.html', locals())
	else:
		return redirect('/')

def history(request):
	if request.user.is_authenticated:
		try:
			videos = models.VideoDetail.objects.filter(user=request.user).order_by('-pub_time')
			video_path_dir = "../media/"
		except:
			videos = None
		return render(request, 'history.html', locals())
	else:
		return redirect('/')