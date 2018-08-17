from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=32)
	password = models.CharField(max_length=32)
	types = (
		(0,'master'),
		(1,'visitor')
		)
	usertype = models.IntegerField(choices=types)
	content = models.CharField(max_length=1000,null=True)
	img = models.CharField(max_length=128,null=True)


class Category(models.Model):
	name = models.CharField(max_length=32)
	def __str__(self):
		return self.name

class Category2(models.Model):
	name = models.CharField(max_length=32)
	content = models.CharField(max_length=128,null=True)
	img = models.CharField(max_length=128,null=True)
	likes = models.IntegerField(default=0)

class Article(models.Model):
	title = models.CharField(max_length=52)
	content = models.TextField()
	createtime = models.DateField(auto_now_add=True)
	updatetime = models.DateField(auto_now=True)
	category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
	count = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)

class Image(models.Model):
	img = models.CharField(max_length=256)
	createtime = models.DateField(auto_now_add=True)
	category = models.ForeignKey(Category2,on_delete=models.SET_NULL,null=True)
	count = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)

class Comment(models.Model):
	article = models.ForeignKey(Article,on_delete=models.CASCADE)
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	time = models.DateField(auto_now_add=True)
	content = models.CharField(max_length=128)



class Comment2(models.Model):
	image = models.ForeignKey(Image,on_delete=models.CASCADE)
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	time = models.DateField(auto_now_add=True)
	content = models.CharField(max_length=128)


class Ly(models.Model):
	username = models.CharField(max_length=20)
	email = models.EmailField()
	content = models.CharField(max_length=256)
	time = models.DateField(auto_now_add=True)


