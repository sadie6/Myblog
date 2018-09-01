from django.shortcuts import render
from blog import models
from django.db.models import Count
import random 
from django.utils.safestring import mark_safe
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.forms import widgets
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.cache import cache_page


# Create your views here.
class Page:
	def __init__(self,current_page,data_count,per_page_count=10,page_num=9):    #当前页，总数据条数，每页多少条，页码显示几页
		self.current_page = int(current_page)
		self.data_count = int(data_count)
		self.per_page_count = int(per_page_count)
		self.page_num = int(page_num)


	@property
	def start(self):
		return (int(self.current_page)-1)*int(self.per_page_count)

	@property
	def end(self):
		return int(self.current_page)*int(self.per_page_count)

	@property
	def all_count(self):
		"""获取总页数"""
		v,y = divmod(self.data_count,self.per_page_count)
		if y:
			v += 1 
		return v

	def page_str(self,base_url):
		page_list = []
		if self.all_count<self.page_num:
			start_index = 1
			end_index = self.all_count+1

		else:
			if self.current_page <= (self.page_num+1)/2:
				start_index = 1
				end_index = self.page_num+1
			else:
				start_index = self.current_page - (self.page_num-1)/2
				end_index = self.current_page + (self.page_num+1)/2
				if(self.current_page + (self.page_num-1)/2) > self.all_count:
					end_index = self.all_count +1
					start_index = self.all_count - self.page_num + 1

		allpage = '<a href="%s?p=%s" class="allpage"><b>%s</b></a>&nbsp;&nbsp;' %(base_url,self.all_count,self.all_count)

		page_list.append(allpage)

		if self.current_page != 1:
			prev = '<a href="%s?p=%s" onclick="page(%s)">上一页</a>&nbsp;&nbsp;' %(base_url,self.current_page-1,self.current_page-1)
			page_list.append(prev)

		for i in range(int(start_index),int(end_index)):
			if i == self.current_page:
				temp = '<a href="%s?p=%s" class="curPage">%s</a>&nbsp;&nbsp;' %(base_url,i,i)
			else:
				temp = '<a href="%s?p=%s" onclick="page(%s)">%s</a>' %(base_url,i,i,i)
			page_list.append(temp)

		if self.current_page != self.all_count:
			nex = '<a href="%s?p=%s" onclick="page(%s)">下一页</a>' %(base_url,self.current_page+1,self.current_page+1)
			page_list.append(nex)
		page_str = mark_safe("".join(page_list))
		return page_str



class Fm(forms.Form):
    username = forms.fields.CharField(min_length = 4,max_length = 10)
    pwd = forms.fields.CharField(min_length=6,max_length=16)
    content = forms.fields.CharField()


class Mf_ly(forms.ModelForm):
	class Meta:
		model = models.Ly
		exclude = ['time']
		widgets = {
		'content':widgets.Textarea(attrs={'name':'lytext','cols':'60','rows':'12','id':'lytext'})
		}


class MF_article(forms.ModelForm):
	

	class Meta:
		model = models.Article
		fields = ['title','content','category']
		widgets = {
		'content':widgets.Textarea(attrs={'name':"content", 'rows':"6", 'id':"saytext"})
		}
		labels = {
		'category':'文章分类','title':'文章标题','content':'文章内容'
		}

	def __init__(self, *args, **kwargs):
		super(MF_article, self).__init__(*args, **kwargs)
		self.fields['content'].required = False



@cache_page(20)
def index(request):
	about_obj = models.User.objects.get(id=1)
	image_obj = models.Image.objects.all().order_by('?')[:6]
	category_obj = models.Category.objects.annotate(num_pro=Count('article'))
	article_obj = models.Article.objects.all().order_by('?')[:6]
	article_obj2 = models.Article.objects.all().order_by('-updatetime')[:10]
	# print(obj)
	return render(request,'index.html',{'about':about_obj,'image':image_obj,'category':category_obj,'article':article_obj,'article2':article_obj2})

@cache_page(1000)
def share(request):
	current_page = request.GET.get('p',1)
	category2_obj = models.Category2.objects.all()

	page_obj = Page(current_page,len(category2_obj),8)
	data = category2_obj[int(page_obj.start):int(page_obj.end)] 
	# print(data)
	base_url = '/blog/share/'
	page_str = page_obj.page_str(base_url)


	data1 = data[::2]
	data2 = data[1::2]
	category2 = [[],[],[],[]]
	if(len(data)%2==0):
		for i in range(len(data1)):
			category2[i].append(data1[i])
			category2[i].append(data2[i]) 
	else:
		for i in range(len(data1)-1):
			category2[i].append(data1[i])
			category2[i].append(data2[i])
		category2[i+1].append(data1[i+1])

	return render(request,'share.html',{'category':category2,'page_str':page_str})

def list(request,nid):
	current_page = request.GET.get('p',1)
	category_obj = models.Category.objects.annotate(num_pro=Count('article'))
	article_obj = models.Article.objects.all().order_by('?')[:6]
	article_obj2 = models.Article.objects.all().order_by('-count')[:6]
	if nid == '0':
		article_obj3 = models.Article.objects.all().order_by('-updatetime')[:10]
	else:
		article_obj3 = models.Article.objects.filter(category_id=nid).order_by('-updatetime')[:10]


	#fenye
	page_obj = Page(current_page,len(article_obj3))
	
	# page_obj = Page(current_page,len(List))
	data = article_obj3[int(page_obj.start):int(page_obj.end)] 
	# print(data)
	base_url = '/blog/list/%s' %nid
	page_str = page_obj.page_str(base_url)

	return render(request,'list.html',{'category':category_obj,'article':article_obj,'article2':article_obj2,'article3':article_obj3,'page_str':page_str})

@cache_page(1000)
def about(request):
	about_obj = models.User.objects.get(id=1)
	image_obj = models.Image.objects.all().order_by('?')[:6]
	category_obj = models.Category.objects.annotate(num_pro=Count('article'))
	article_obj = models.Article.objects.all().order_by('?')[:6]
	return render(request,'about.html',{'about':about_obj,'image':image_obj,'category':category_obj,'article':article_obj})

def gbook(request):
	about_obj = models.User.objects.get(id=1)
	image_obj = models.Image.objects.all().order_by('?')[:6]
	category_obj = models.Category.objects.annotate(num_pro=Count('article'))
	article_obj = models.Article.objects.all().order_by('?')[:6]
	ly_obj = models.Ly.objects.all()
	if request.method == 'GET':
		mf = Mf_ly()
	else:
		mf = Mf_ly(request.POST)
		if mf.is_valid():
			mf.save()

	return render(request,'gbook.html',{'about':about_obj,'image':image_obj,'category':category_obj,'article':article_obj,'obj':mf,'ly':ly_obj})
@cache_page(60)
def info(request,nid):
	category_obj = models.Category.objects.annotate(num_pro=Count('article'))
	article_obj = models.Article.objects.all().order_by('?')[:6]
	article_obj2 = models.Article.objects.all().order_by('-count')[:6]
	article_obj3 = models.Article.objects.get(id=int(nid))
	comment_obj = models.Comment.objects.filter(article_id=int(nid))
	comment_count = len(comment_obj)

	return render(request,'info.html',{'category':category_obj,'article':article_obj,'article2':article_obj2,'article3':article_obj3,'comment':comment_obj,'comment_count':comment_count})

def infopic(request,nid):
	about_obj = models.User.objects.get(id=1)
	image_obj = models.Image.objects.all().order_by('?')[:6]
	image_obj2 = models.Image.objects.filter(category_id=nid)
	category_obj = models.Category.objects.annotate(num_pro=Count('article'))
	category2_obj = models.Category2.objects.filter(id=nid).first()
	article_obj = models.Article.objects.all().order_by('?')[:6]
	comment_obj = models.Comment2.objects.filter(image_id=int(nid))
	comment_count = len(comment_obj)
	return render(request,'infopic.html',{'about':about_obj,'image':image_obj,'category':category_obj,'article':article_obj,'image2':image_obj2,'len':len(image_obj2),'comment':comment_obj,'comment_count':comment_count,'category2':category2_obj})




def comment(request):
	if request.method == 'GET':
		return HttpResponseRedirect('index')

	else:
		username = request.POST.get('username')
		pwd = request.POST.get('pwd')
		user_obj = models.User.objects.filter(username=username).first()
		if user_obj and user_obj.password == pwd:
			content = request.POST.get('content')
			aid = request.POST.get('aid',0)
			pid = request.POST.get('pid',0)

			if int(aid):
				# print(content,aid,username,pwd)
				models.Comment.objects.create(article_id=aid,userId_id=user_obj.id,content=content)
				# return HttpResponse('ok')
				url = 'info/%s' %aid
				return HttpResponseRedirect(url)

			if int(pid):
				models.Comment2.objects.create(image_id=pid,userId_id=user_obj.id,content=content)
				url = 'infopic/%s' %pid
				return HttpResponseRedirect(url)




		else:
			return HttpResponse('username or password is error!')


def digit(request):
	aid = request.GET.get('aid',0)
	pid = request.GET.get('pid',0)
	

	
	if int(aid):
		url = 'info/%s' %aid
		article_obj = models.Article.objects.filter(id=int(aid)).first()
		article_obj.likes = article_obj.likes + 1
		article_obj.save()		
		# return HttpResponseRedirect(url)
		return HttpResponse('ok')
	elif int(pid):
		url = 'infopic/%s' %pid
		category2_obj = models.Category2.objects.filter(id=int(pid)).first()
		category2_obj.likes = category2_obj.likes + 1
		category2_obj.save()
		# return HttpResponseRedirect(url)
		return HttpResponse('ok')

	else:
		# return HttpResponseRedirect('index')
		return HttpResponse('errors')










def qx(request):
	about_obj = models.User.objects.get(id=1)
	image_obj = models.Image.objects.all().order_by('?')[:6]
	category_obj = models.Category.objects.annotate(num_pro=Count('article'))
	article_obj = models.Article.objects.all().order_by('?')[:6]
	return render(request,'meigui.html',{'about':about_obj,'image':image_obj,'category':category_obj,'article':article_obj})







@cache_page(1000)
def write(request):
	about_obj = models.User.objects.get(id=1)
	image_obj = models.Image.objects.all().order_by('?')[:6]
	category_obj = models.Category.objects.annotate(num_pro=Count('article'))
	article_obj = models.Article.objects.all().order_by('?')[:6]
	if request.method == 'GET':	
		obj = MF_article()
	else:
		obj = MF_article(request.POST)
		if obj.is_valid():
			obj.save()

	return render(request,'write.html',{'about':about_obj,'image':image_obj,'category':category_obj,'article':article_obj,'obj':obj})


def photo(request):
	if request.method == 'GET':
		about_obj = models.User.objects.get(id=1)
		image_obj = models.Image.objects.all().order_by('?')[:6]
		category_obj = models.Category.objects.annotate(num_pro=Count('article'))
		article_obj = models.Article.objects.all().order_by('?')[:6]
		category2_obj = models.Category2.objects.all()

		return render(request,'photo.html',{'about':about_obj,'image':image_obj,'category':category_obj,'article':article_obj,'category2':category2_obj})
	else:
		cid = request.POST.get('categorylist')
		img_obj = request.FILES.get('f')
		if cid:
			if img_obj:
				with open('static/images/'+img_obj.name,'wb') as f:
					for i in img_obj.chunks():
						f.write(i)
				models.Image.objects.create(img='/static/images/'+img_obj.name,category_id=int(cid))
				return HttpResponse("ok")
			else:
				return HttpResponse("error")

		else:
			if img_obj:
				with open('static/images/'+img_obj.name,'wb') as f:
					for i in img_obj.chunks():
						f.write(i)
				return HttpResponse('/static/images/'+img_obj.name)
			else:
				return HttpResponse("error")

@csrf_exempt
def upload_img(request):

	img_obj = request.FILES.get('imgFile')
	with open('static/images/'+img_obj.name,'wb') as f:
		for i in img_obj.chunks():
			f.write(i)
	dic = {
	"error":0,
	'url':'/static/images/' + img_obj.name,
	'message':'error',
	}
	return HttpResponse(json.dumps(dic))