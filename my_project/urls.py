from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    re_path(r'^jet/', include(('jet.urls', 'jet'))),
    re_path(r'^jet/dashboard/', include('jet.dashboard.urls', namespace='jet-dashboard')),
    path('admin/', admin.site.urls),
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'), 
    path('accounts/', include('django.contrib.auth.urls')),  # new
    path('', TemplateView.as_view(template_name='base.html'), name='base'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
        r'(?P<post>[-\w]+)/$',
        views.post_detail, 
        name='post_detail'),
    url(r'^about/$', views.about, name='about'),
    url(r'^search/$', views.search, name='search'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post')
    ]