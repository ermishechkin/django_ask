from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.static import serve
from ask import views

urlpatterns = [
    url(r'^test/', views.test),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<page>[0-9]+)/$', views.index, name='index'),
    url(r'^hot/$', views.hot, name='hot'),
    url(r'^hot/(?P<page>[0-9]+)/$', views.hot, name='hot'),
    url(r'^tag/(?P<name>[^/]+)/$', views.tag, name='tag'),
    url(r'^tag/(?P<name>[^/]+)/(?P<page>[0-9]+)/$', views.tag, name='tag'),
    url(r'^ask/', views.ask, name='ask'),
    url(r'^login/', views.login2, name='login'),
    url(r'^logout/', views.logout2, name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^question/(?P<id>[0-9]+)/$', views.question, name='question'),
    url(r'^question/(?P<id>[0-9]+)/(?P<page>[0-9]+)/$', views.question, name='question'),
    url(r'^mark_q$', views.setMarkQuestion, name='setMarkQuestion'),
    url(r'^mark_a$', views.setMarkAnswer, name='setMarkAnswer'),
    url(r'^answer$', views.add_answer, name='add_answer'),
    url(r'^(?P<path>css/[^/]+)$', serve, name='css', kwargs={'document_root' : settings.STATIC_ROOT}),
    url(r'^(?P<path>js/[^/]+)$', serve, name='js', kwargs={'document_root' : settings.STATIC_ROOT}),
    url(r'^(?P<path>fonts/[^/]+)$', serve, name='fonts', kwargs={'document_root' : settings.STATIC_ROOT}),
] + static('/uploads/', document_root=settings.STATIC_ROOT+'../uploads/')


