from django.conf.urls import patterns, include, url
from listing import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
              
    # Examples:
     url(r'^$', views.index, name='index'),
     url(r'^poll/^$', views.poll_page, name='poll_page'),	 
     # url(r'^$', TemplateView.as_view(template_name='listing/index.html'), name="home"),	 
    # url(r'^listing/', include('listing.foo.urls')),
     url(r'^polls/', include('polls.urls', namespace="polls")),
     url(r'^login/', include('login.urls', namespace="login")),
     url(r'^facebook/', include('django_facebook.urls')),
     url(r'^accounts/', include('django_facebook.auth_urls')), #Don't add this line if you use django registration or userena for registration and auth.	 
     url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
     # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,}),         
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
