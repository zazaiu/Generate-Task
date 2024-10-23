from django.db import models

# Create your models here.
class Prepod(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name
	
class Discp(models.Model):
	title = models.CharField(max_length=100) 
	
	def __str__(self):
		return self.title	
class Task(models.Model):
	#title = models.CharField(max_length=100)
	#description = models.TextField() #описание
	name =  models.CharField(max_length=100) #models.ForeignKey(Prepod, on_delete=models.CASCADE)
	example=models.TextField() #пример задачи
	discp = models.ForeignKey(Discp, on_delete=models.CASCADE)
	
	
	def __str__(self):
		return self.example	
	
	
class Variant(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	text = models.TextField()