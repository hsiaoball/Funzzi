from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    # ex: /polls/
    # ex: /polls/5/
    url(r'^search/$', views.search_post, name='search_post'),	
    url(r'^event_query/$', views.event_query, name='event_query'),	
    url(r'^post_event/$', views.post_event, name='post_event'),		
    url(r'^comment_event/$', views.comment_event, name='comment_event'),		
    url(r'^add_pic/$', views.add_pic, name='add_pic'),	
    url(r'^delete_event/$', views.delete_event, name='delete_event'),	
    url(r'^ask_poster_question/$', views.ask_poster_question, name='ask_poster_question'),	
    url(r'^get_question_conversation/$', views.get_question_conversation, name='get_question_conversation'),	    
    url(r'^get_feature_post/$', views.get_feature_post, name='get_feature_post'),	     
)