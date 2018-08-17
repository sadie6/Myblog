from django.conf.urls import url
from . import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    url('index/',views.index),
    url('share/',views.share),
    url('list/(?P<nid>\d+)',views.list),
    url('about/',views.about),
    url('gbook/',views.gbook),
    url('info/(?P<nid>\d+)$',views.info),
    url('infopic/(?P<nid>\d+)',views.infopic),
    url('comment',views.comment),
    url('digit',views.digit),
    url('write',views.write),
    url('photo',views.photo),
    url('upload_img',views.upload_img),


    url('qx',views.qx),
    


]