# -*- coding: utf-8 -*-

from django.db import models

TASKTYPE_CHOICES = (
    ("m", 'Мониторинг цен'),
    ("site", 'Мониторинг сайтов'))

class MobileDevice(models.Model):
	name = models.CharField(max_length=250)
	password = models.CharField(max_length=50)
	uuid = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=50, blank=True)
	change_password = models.BooleanField()
	key = models.CharField(max_length=250, blank=True, null=True)


	def __str__(self):
		return '%s' % (self.name.encode('utf-8'))

	class Meta:
		verbose_name = "Мобильное устройство"
		verbose_name_plural = "Мобильные устройства"

	def __unicode__(self):
		return u"%s" % (self.name)

class Task(models.Model):
	mobileDevice = models.ForeignKey(MobileDevice, on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=250)
	begin_date = models.DateField()
	end_date = models.DateField()
	in_work = models.BooleanField()
	completedate = models.CharField(max_length=25, blank=True, null=True)
	tasktype = models.CharField(max_length=50, choices=TASKTYPE_CHOICES)
	status = models.IntegerField(max_length=10, blank=True, null=True)

	def __str__(self):
		return '%s' % (self.name.encode('utf-8'))

	class Meta:
		verbose_name = "Заданиe"
		verbose_name_plural = "Задания"

	def __unicode__(self):
		return u"%s" % (self.name)

class Competitor(models.Model):
	name = models.CharField(max_length=250)
	address = models.CharField(max_length=250, blank=True, null=True)

	def __str__(self):
		return '%s' % (self.name.encode('utf-8'))

	class Meta:
		verbose_name = "Конкурент"
		verbose_name_plural = "Конкуренты"

	def __unicode__(self):
		return u"%s" % (self.name)

class Group(models.Model):
	name = models.CharField(max_length=250)
	def __str__(self):
		return '%s' % (self.name.encode('utf-8'))

	class Meta:
		verbose_name = "Группа"
		verbose_name_plural = "Группы"

	def __unicode__(self):
		return u"%s" % (self.name)

class Article(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
	task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
	competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, blank=True, null=True)
	
	name = models.CharField(max_length=250)
	price = models.CharField(max_length=250, blank=True)
	pricefrom = models.CharField(max_length=250, blank=True, null=True)
	priceto = models.CharField(max_length=250, blank=True, null=True)
	quant = models.CharField(max_length=250, blank=True, null=True)
	unit = models.CharField(max_length=250, blank=True, null=True)
	takephoto = models.NullBooleanField()
	photo_path = models.CharField(max_length=250, blank=True)
	latitude = models.CharField(max_length=250, blank=True, null=True)
	longitude = models.CharField(max_length=250, blank=True, null=True)
	is_action = models.CharField(max_length=250, blank=True, null=True)


	def __str__(self):
		return '%s' % (self.name.encode('utf-8'))

	class Meta:
		verbose_name = "Товар"
		verbose_name_plural = "Товары"

	def __unicode__(self):
		return u"%s" % (self.name)