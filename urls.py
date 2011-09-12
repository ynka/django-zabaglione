from django.conf.urls.defaults import *
from core import urls
from core import views
from django.contrib import admin
from django.conf import settings


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^',include('core.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^search/', "core.views.custom_search_view", {}, 'search_url'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^accounts/logout/$',"django.contrib.auth.views.logout",{'next_page' : '/'}),
    (r'^accounts/', include('registration.urls')),
    (r'^attachments/', include('attachments.urls')),
)

if settings.LOCAL_DEV:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
    )
