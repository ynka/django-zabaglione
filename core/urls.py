# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from core.models import *
from core.views import *
from django.conf import settings


urlpatterns = patterns('',
        (r'^$', index),
        (r'^project/(?P<project_id>\d+)/ticket/new/$', add_or_update_ticket,{},'add_ticket_url'),
        (r'^project/(?P<project_id>\d+)/ticket/(?P<ticket_id>\d+)/update/$', add_or_update_ticket,{},'update_ticket_url'),
        (r'^project/(?P<project_id>\d+)/ticket/(?P<object_id>\d+)/add_related_ticket/$',add_related_ticket,{},'add_related_ticket_url'),
        (r'^project/(?P<project_id>\d+)/news/(?P<object_id>\d+)/$',news_detail,{}, 'news_detail_url'),
        (r'^project/(?P<project_id>\d+)/ticket/(?P<object_id>\d+)/$',ticket_detail,{},"ticket_detail_url"),
        (r'^project/(?P<object_id>\d+)/news/new/$',add_news,{},'add_news_url'),
        (r'^project/(?P<object_id>\d+)/news/$',news, {}, "news_url"),
        (r'^project/(?P<object_id>\d+)/$', project_detail,{},"project_detail_url"),
        (r'^project/(?P<object_id>\d+)/repository$',project_repository,{},"project_repository_url"),
        (r'^projects/$', projects,{},"project_list_url"),
)
