from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class VideoDetail(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	video_name = models.CharField(max_length = 50)
	accuracy = models.PositiveIntegerField(default = 0)
	duration_h = models.PositiveIntegerField(default = 0)
	duration_m = models.PositiveIntegerField(default = 0)
	duration_s = models.PositiveIntegerField(default = 0)
	pub_time = models.DateField(default = datetime.now)
	class Meta:
		ordering = ('-pub_time',)
	def __str__(self):
		return self.video_name

class RecordDays(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	last_day = models.DateField(default = datetime.now)
	attend_days = models.PositiveIntegerField(default = 0)
	absent_days = models.PositiveIntegerField(default = 0)
	max_continue_days = models.PositiveIntegerField(default = 0)
	def __str__(self):
		return self.user.username

class RecordAccuracy(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	total_game = models.PositiveIntegerField(default = 0)
	average_accuracy = models.PositiveIntegerField(default = 0)
	def __str__(self):
		return self.user.username