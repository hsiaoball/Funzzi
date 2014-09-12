from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from login import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^create/$', views.create, name='create'),
    url(r'^update/$', views.update, name='update'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<p_name>\w+)$', views.profile_view, name='profile_view'),
    url(r'^profile/json/(?P<p_name>\w+)$', views.profile_view_json, name='profile_view_json'),
    # url(r'^profile/(?P<p_name>\w+)/like$', views.	like, name='like'),	
    # url(r'^profile/(?P<p_name>\w+)/comment$', views.profile_comment, name='profile_comment'),	
    url(r'^profile/(?P<p_name>\w+).(?P<p_name2>\w+)$', views.profile_view2, name='profile_view2'),	
    url(r'^profile/(?P<p_name>\w+).(?P<p_name2>\w+).(?P<p_name3>\w+)$', views.profile_view3, name='profile_view3'),		
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^profile_view/$', views.profile_view, name='profile_view'),	
    url(r'^check_login/$', views.check_login, name='check_login'),	
    url(r'^fb_login/$', views.fb_login, name='fb_login'),	 	
    url(r'^confirm_email/$', views.send_registration_confirmation, name='confirm_email'),	 		
    url(r'^email_link/(?P<code>\w+)/(?P<user_id>\d+)$', views.email_link, name='email_link'),	 			
    url(r'^set_read_notice/$', views.set_read_notice, name='set_read_notice'),	     
    # ex: /polls/5/results/
    # url(r'^profile/$', views.results, name='profile'),

)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)