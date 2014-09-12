from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect,render_to_response
from django.utils import timezone
from django.core.urlresolvers import reverse
from polls.models import Poll,Questions
from decimal import Decimal
import os
import datetime
from django.conf import settings
from django.core import serializers
import json
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from polls.models import ImageUploadForm
from django.conf import settings
from django_facebook.models import FacebookCustomUser, FacebookUser, FacebookProfile
from login.models import CustomUser, model_addfield,notice
import logging
User= model_addfield
logger = logging.getLogger(__name__)
POST_PIC_MAX_SIZE=1*1024*1024
@csrf_exempt


class Obj(object):
  _ids = 0
  def __init__(self):
    self.id = self._ids.next()	
    if self.id > 1:
	    raise NameError('More than one instance')

def post_event(request):
    if request.user.is_authenticated():
        if 'event_id' in request.POST:
            try: p = Poll.objects.get(pk=request.POST['event_id'])
            except ObjectDoesNotExist:
               	return HttpResponse("\"event not exist\"", content_type="application/json")     
            p.start_date=request.POST['departure_time'],
            p.end_date=request.POST['return_time'],
            p.content=request.POST['content'],
            p.address=request.POST['address'],
            p.state=request.POST['state'],
            p.zip=request.POST['zip'],
            p.city=request.POST['city'],
            p.rent=request.POST['rent'],		
            p.num_bed=request.POST['num_bed'],	
            p.num_bath=request.POST['num_bath'],
            p.size=request.POST['size'],
            p.property_type=1,
            #p.property_type=request.POST['property_type'],
            p.floor_level=request.POST['floor_level'],
            p.parking=request.POST['parking'],
            p.pet=request.POST['pet'],
            p.smoke=request.POST['smoke'],
            p.private_bath=request.POST['private_bath'],
            p.washer_dryer=request.POST['washer_dryer'],
            p.kitchen_access=request.POST['kitchen_access'],
            p.internet=request.POST['internet'],
            p.cable_tv=request.POST['cable_tv'],
            p.park=request.POST['park'],
            p.play_ground=request.POST['play_ground'],
            p.tennis=request.POST['tennis'],
            p.basketball=request.POST['basketball'],
            p.swim_pool=request.POST['swim_pool'],
            p.jacuzzi=request.POST['jacuzzi'],
            p.gym=request.POST['gym'],
            p.bbq_area=request.POST['bbq_area'],
            p.rent_internet=request.POST['rent_internet'],
            p.rent_cable_tv=request.POST['rent_cable_tv'],
            p.rent_water=request.POST['rent_water'],
            p.rent_gas=request.POST['rent_gas'],
            p.rent_electricity=request.POST['rent_electricity'],
            p.rent_garbage=request.POST['rent_garbage'],
            p.rent_parking=request.POST['rent_parking'],			
            p.save()            				
        else:    				
            p = Poll(
                     pub_date=timezone.now(),  
                     start_date=request.POST['departure_time'],
                     end_date=request.POST['return_time'],
                     content=request.POST['content'],
                     address=request.POST['address'],
                     state=request.POST['state'],
                     zip=request.POST['zip'],
                     city=request.POST['city'],
                     rent=request.POST['rent'],		
                     num_bed=request.POST['num_bed'],	
                     num_bath=request.POST['num_bath'],	
                     user_pk=request.user.pk,
                     size=request.POST['size'] if request.POST['size'] else None,
                     #property_type=request.POST['property_type'] if request.POST['property_type'] else None,
                     floor_level=request.POST['floor_level'] if request.POST['floor_level'] else None,
                     #parking=request.POST['parking'] if request.POST['parking'] else None,
                     #pet=request.POST['pet'] if request.POST['pet'] else None,
                     smoke=request.POST['smoke'] if request.POST['smoke'] else None,
                     private_bath=request.POST['private_bath'] if request.POST['private_bath'] else None,
                     #washer_dryer=request.POST['washer_dryer'] if request.POST['washer_dryer'] else None,
                     kitchen_access=request.POST['kitchen_access'] if request.POST['kitchen_access'] else None,
                     internet=request.POST['internet'] if request.POST['internet'] else None,
                     cable_tv=request.POST['cable_tv'] if request.POST['cable_tv'] else None,
                     park=request.POST['park'] if request.POST['park'] else None,
                     play_ground=request.POST['play_ground'] if request.POST['play_ground'] else None,
                     tennis=request.POST['tennis'] if request.POST['tennis'] else None,
                     basketball=request.POST['basketball'] if request.POST['basketball'] else None,
                     swim_pool=request.POST['swim_pool'] if request.POST['swim_pool'] else None,
                     jacuzzi=request.POST['jacuzzi'] if request.POST['jacuzzi'] else None,
                     gym=request.POST['gym'] if request.POST['gym'] else None,
                     bbq_area=request.POST['bbq_area'] if request.POST['bbq_area'] else None,
                     rent_internet=request.POST['rent_internet'] if request.POST['rent_internet'] else None,
                     rent_cable_tv=request.POST['rent_cable_tv'] if request.POST['rent_cable_tv'] else None,
                     rent_water=request.POST['rent_water'] if request.POST['rent_water'] else None,
                     rent_gas=request.POST['rent_gas'] if request.POST['rent_gas'] else None,
                     rent_electricity=request.POST['rent_electricity'] if request.POST['rent_electricity'] else None,
                     rent_garbage=request.POST['rent_garbage'] if request.POST['rent_garbage'] else None,
                     rent_parking=request.POST['rent_parking'] if request.POST['rent_parking'] else None,
                     ) 
            p.save() 
        return HttpResponse(p.id, content_type="application/json")  
    else:            
        return HttpResponse("\"not authorized\"", content_type="application/json") 

def ask_poster_question(request):    
    if request.user.is_authenticated():
        if 'event_id' in request.POST:
            try: p = Poll.objects.get(pk=request.POST['event_id'])
            except ObjectDoesNotExist:
               	return HttpResponse("\"event not exist\"", content_type="application/json")     
            poster=User.objects.get(pk=request.POST['receiver_pk'])
            poster.notice_set.create( noticer=request.POST['giver_pk'],
                             post_id=p.pk,
                             date=timezone.now(),
                             notice_type=1,
                             un_read_notice=1)		
            if str(p.user_pk) == request.POST['giver_pk']:
                is_host=1
                commenter_pk=request.POST['receiver_pk']
            else:
                is_host=0       
                commenter_pk=request.POST['giver_pk']                
            p.questions_set.create( commenter_pk=commenter_pk,
                             comment_text=request.POST['question'],
                             host=is_host,
                             pub_date=timezone.now())			                              
            return HttpResponse("\"success\"", content_type="application/json")                               
            				
def get_question_conversation(request):    
    if request.user.is_authenticated():
        if 'event_id' in request.POST:
            try: p = Poll.objects.get(pk=request.POST['event_id'])
            except ObjectDoesNotExist:
               	return HttpResponse("\"event not exist\"", content_type="application/json")   
            if request.POST['questioner_id']== str(p.user_pk):
                questioner_id=request.user.id
            else:
                questioner_id=request.POST['questioner_id']
            questions=p.questions_set.filter( commenter_pk=questioner_id)			                              
            q_group=[]
            for question in questions:  
                if question.host==1:
                    commenter_id=p.user_pk
                else:
                    commenter_id=question.commenter_pk
                q_group.append({'host': str(question.host), 'commenter_id': get_username(commenter_id), 'comment_text': question.comment_text, 'pub_date': str(question.pub_date)})
            serialized_obj = json.dumps(q_group)
            # serialized_obj = serializers.serialize('json', questions)	            
            return HttpResponse(serialized_obj, content_type='application/json')
        return HttpResponse("\"no event_id\"", content_type="application/json")                
                             
def get_feature_post(request):
    return search_post(request)
    
def add_pic(request):    
    if request.user.is_authenticated():
        if 'event_id' in request.POST:
            # if request.FILES['image1'].size > POST_PIC_MAX_SIZE or request.FILES['image2'].size > POST_PIC_MAX_SIZE or request.FILES['image3'].size > POST_PIC_MAX_SIZE or request.FILES['image4'].size > POST_PIC_MAX_SIZE or request.FILES['image5'].size > POST_PIC_MAX_SIZE or request.FILES['image6'].size > POST_PIC_MAX_SIZE or request.FILES['image7'].size > POST_PIC_MAX_SIZE :	
               	# return HttpResponse("\"image to big maximum is 1MB\"", content_type="application/json")  			
            try: p = Poll.objects.get(pk=request.POST['event_id'])
            except ObjectDoesNotExist:
               	return HttpResponse("\"event not exist\"", content_type="application/json")     
            if p.user_pk!= request.user.id:
               	return HttpResponse("\"not poster\"", content_type="application/json")     			
            form = ImageUploadForm(request.POST, request.FILES)
            # logger.info('1Something went wrong!')			
            form.is_valid()
                # return HttpResponse(form.errors, content_type="application/json") 
                # logger.error('Something went wrong!')			
            if 'image1' in form.cleaned_data: p.room_pic1 = form.cleaned_data['image1']
                # return HttpResponse("\"test\"", content_type="application/json") 
            if 'image2' in form.cleaned_data: p.room_pic2 = form.cleaned_data['image2']
            if 'image3' in form.cleaned_data: p.room_pic3 = form.cleaned_data['image3']
            if 'image4' in form.cleaned_data: p.room_pic4 = form.cleaned_data['image4']
            if 'image5' in form.cleaned_data: p.room_pic5 = form.cleaned_data['image5']
            if 'image6' in form.cleaned_data: p.room_pic6 = form.cleaned_data['image6']
            if 'image7' in form.cleaned_data: p.room_pic7 = form.cleaned_data['image7']				
                # if len(p.room_pic1 ) > settings.MAX_PROFILE_PIC_SIZE:
                      # return HttpResponse("\"Pic too big\"", content_type="application/json") 
            # else:
               	# return HttpResponse(form.errors, content_type="application/json") 							  
            p.save()           
            return redirect('/../../index.html#event/'+str(p.pk))
	
        else:
            return render(request, 'polls/error_msg.html', {'error_msg':'No event_id'})
    else:
        return HttpResponse("\"not login\"", content_type="application/json")  
		
def event_query(request,poll_id):
    try: poll = Poll.objects.get(pk=poll_id)
    except ObjectDoesNotExist:
       	return HttpResponse("\"event not exist\"", content_type="application/json")
    # logger.debug('1Something went wrong!')			
    connection=[]
    if request.user.is_authenticated():
        connection=check_fb_mutual_frd(request.user.id,poll.user_pk)
    groups_and_items = {}
    comment=poll.comment_set.all()
    passanger=poll.guest_list_set.all()
    comment_group = []
    passanger_group= []
    pending_group= []
    poll_ser={}	


    for comment in poll.comment_set.all():
        comment_group.append( {'comment_text': comment.comment_text, 'commenter': get_username(comment.commenter_pk), 'commenter_pic': get_fb_pic(comment.commenter_pk), 'pub_date':str(comment.pub_date) })	

    img_group=[]
    if poll.room_pic1 !="" and poll.room_pic1 !=None: img_group.append(str(poll.room_pic1))
    if poll.room_pic2 !="" and poll.room_pic2 !=None: img_group.append(str(poll.room_pic2))
    if poll.room_pic3 !="" and poll.room_pic3 !=None: img_group.append(str(poll.room_pic3))	
    if poll.room_pic4 !="" and poll.room_pic4 !=None: img_group.append(str(poll.room_pic4))
    if poll.room_pic5 !="" and poll.room_pic5 !=None: img_group.append(str(poll.room_pic5))
    if poll.room_pic6 !="" and poll.room_pic6 !=None: img_group.append(str(poll.room_pic6))
    if poll.room_pic7 !="" and poll.room_pic7 !=None: img_group.append(str(poll.room_pic7))	
	
    	
    poll_ser.update({'size':str(poll.size),
                     'property_type':str(poll.property_type),
                     'floor_level':str(poll.floor_level),
                     'parking':str(poll.parking),
                     'pet':str(poll.pet),
                     'smoking':str(poll.smoke),
                     'private_bath':str(poll.private_bath),
                     'washer_dryer':str(poll.washer_dryer),
                     'kitchen_access':str(poll.kitchen_access),
                     'internet':str(poll.internet),
                     'cable_tv':str(poll.cable_tv),
                     'park':str(poll.park),
                     'play_ground':str(poll.play_ground),
                     'tennis':str(poll.tennis),
                     'basketball':str(poll.basketball),
                     'swim_pool':str(poll.swim_pool),
                     'jacuzzi':str(poll.jacuzzi),
                     'gym':str(poll.gym),
                     'bbq_area':str(poll.bbq_area),
                     'rent_internet':str(poll.rent_internet),
                     'rent_cable_tv':str(poll.rent_cable_tv),
                     'rent_water':str(poll.rent_water),
                     'rent_gas':str(poll.rent_gas),
                     'rent_electricity':str(poll.rent_electricity),
                     'rent_garbage':str(poll.rent_garbage),
                     'rent_parking':str(poll.rent_parking),	
                     'free_way': 'I880',   
                     'utilities':'include',
                     'term': 'Long term',
                     'over_night_guest': 'Yes',
                     'funiture':'Not provide',
                     'about_you': 'Female',
                     'about_us': 'Nice people',
                     'connection': connection,
                     'content':str(poll.content)})	
    res ={}
    # poll_ser = dict((k,v) for k,v in poll_ser.iteritems()  if v != 'None' )
    poll_ser.update({'user_field':get_username(poll.user_pk),
                     'pk':str(poll.pk),	
	                 'user_pk':str(poll.user_pk),
                     'pub_date':str(poll.pub_date),
                     'start_date':str(poll.start_date),
                     'end_date':str(poll.end_date),
                     'fb_url':get_fb_url(poll.user_pk),	
                     'poster_fb_pic':get_fb_pic(poll.user_pk),						 
                     'address':str(poll.address),
                     'state':str(poll.state),
                     'zip':str(poll.zip),
                     'city':str(poll.city),					 
                     'rent':str(poll.rent),				 
                     'room_pic1':str(poll.room_pic1),					 
                     'room_pic2':str(poll.room_pic2),
                     'room_pic3':str(poll.room_pic3),
                     'room_pic4':str(poll.room_pic4),
                     'room_pic5':str(poll.room_pic5),
                     'room_pic6':str(poll.room_pic6),
                     'room_pic7':str(poll.room_pic7),	
                     'imgs': img_group,					 
                     'num_bed':str(poll.num_bed),					 
                     'num_bath':str(poll.num_bath)})	
    # poll_ser = filter( lambda x,y: y!='None', poll_ser)					 
    # poll_ser = dict((k,'Yes') for k,v in poll_ser.iteritems()  if v == 'True' )
    for k,v in poll_ser.items():
        if v=='True':
            poll_ser[k]='Yes'
        elif k=='pet':
            if v=='0':   poll_ser[k]='No'
            elif v=='1': poll_ser[k]='Yes'
            elif v=='2': poll_ser[k]='Dog'
            elif v=='3': poll_ser[k]='Cat'				
        elif k=='washer_dryer':
            if v=='0':   poll_ser[k]='No'
            elif v=='1.0': poll_ser[k]='In Unit'
            elif v=='2': poll_ser[k]='In Community'	


			
    groups_and_items['poll']=poll_ser
    groups_and_items['comment']=comment_group	
    # groups_and_items['imgs']=img_group	
    # all=list(Poll.objects.all().filter(pk=poll_id))+list(list(poll.comment_set.all())+list(poll.guest_list_set.all()))
    # serialized_obj = serializers.serialize('json', groups_and_items)	
    serialized_obj = json.dumps(groups_and_items)	
    return HttpResponse(serialized_obj, content_type='application/json')			

def delete_event(request):
    if request.user.is_authenticated():
        try: p = Poll.objects.get(pk=request.POST['event_id'])
        except ObjectDoesNotExist:
           	return HttpResponse("\"event not exist\"", content_type="application/json")  
        if p.user_pk== request.user.id:			
           p.delete()
           return HttpResponse("\"success\"", content_type="application/json")  
        else:
           return HttpResponse("\"not poster\"", content_type="application/json")  		
    
def check_fb_mutual_frd(your_id, poster_id):
    if your_id==poster_id:
        return {'code':-1}
    poster_fb_id=get_fb_id(poster_id)
    if poster_fb_id ==0:
        return {'code':0, 'msg':'poster doesnt login with FB'}
    your_friends = FacebookUser.objects.filter(user_id=your_id).values_list('facebook_id', flat=True)	
    try: your_friends
    except NameError:
        return {'code':0, 'msg':'find no your fb friend-NameError'}
    else:
        if poster_fb_id in your_friends:
            return {'code':1}
        if len(your_friends) == 0:
            return {'code':0, 'msg':'find no your fb friend-len is 0'}
    poster_friends=FacebookUser.objects.filter(user_id=poster_id).values_list('facebook_id', flat=True)
    try: poster_friends
    except NameError:
        return {'code':0, 'msg':'poster has no FB friend-NameError'}
    else:
        if len(poster_friends) == 0:
            return {'code':0, 'msg':'poster has no FB friend-len is 0'}
    mutual_friend= [val for val in your_friends if val in poster_friends]
    if len(mutual_friend)>0:
        return {'code':2, 'mutual_friend': mutual_friend}
    return {'code':0, 'msg':'no mutual_friend', 'your friends':your_friends, 'poster_fb_id': poster_fb_id}
            
    
def search_post(request):	
    if request.user.is_authenticated():
        user_friends = FacebookUser.objects.filter(user_id=request.user.id)		
    latest_poll_list= Poll.objects.all()
    base_queryset = FacebookUser.objects.filter(user_id=request.user.id)	
    if 'search_zip' in request.POST:
        if request.POST['search_zip']!='' and request.POST['search_zip']!='undefined':
            latest_poll_list = latest_poll_list.filter(zip=request.POST['search_zip'])	
    if 'meetup_place' in request.POST:
        if request.POST['meetup_place']!='':
               latest_poll_list=latest_poll_list.filter(meetup_place=request.POST['meetup'])
    if 'start_date' in request.POST:
        if request.POST['start_date']!='':
               latest_poll_list=latest_poll_list.filter(start_date=request.POST['start_date'])			   
    # if request.POST['user_id']!='':
        # latest_poll_list=latest_poll_list.filter(user_field=request.POST['user_id'])  			
    # latest_poll_list = Poll.objects.all().filter(resort=resort,meetup_place=meetup,user_field=user_id).order_by('-pub_date')[:20]
    try:  latest_poll_list
    except NameError:
        latest_poll_list = Poll.objects.all().order_by('-pub_date')[:20]
    else:
        latest_poll_list=latest_poll_list.order_by('-pub_date')[:20]
    try: user_friends
    except NameError:
        got_friends=0	
    else:
        got_friends=1	
        if len(user_friends) == 0:
            got_friends=0	
    poll_ser=[]	      	
    for poll in latest_poll_list:
        poster_fb_id=get_fb_id(poll.user_pk)
        if poster_fb_id != 0 and got_friends == 1 and poster_fb_id !=None:
            mutual_result=user_friends.filter(facebook_id=poster_fb_id)
            your_friend=1
            if len(	mutual_result) == 0:
                your_friend=0	           		
        else:
            your_friend=0	
        img_addr=''	
        if poll.room_pic1 !="" and poll.room_pic1 !=None: img_addr=	str(poll.room_pic1)
        elif poll.room_pic2 !="" and poll.room_pic2 !=None: img_addr=	str(poll.room_pic2)
        elif poll.room_pic3 !="" and poll.room_pic3 !=None: img_addr=	str(poll.room_pic3)	
        elif poll.room_pic4 !="" and poll.room_pic4 !=None: img_addr=	str(poll.room_pic4)
        elif poll.room_pic5 !="" and poll.room_pic5 !=None: img_addr=	str(poll.room_pic5)
        elif poll.room_pic6 !="" and poll.room_pic6 !=None: img_addr=	str(poll.room_pic6)
        elif poll.room_pic7 !="" and poll.room_pic7 !=None: img_addr=	str(poll.room_pic7)
        else: img_addr='polls/nopic.jpg'
        poll_ser.append({'user_field':get_username(poll.user_pk),
                         'pk':str(poll.pk),	
                         'poster_fb_id':poster_fb_id,						 
                         'poster_fb_pic':get_fb_pic(poll.user_pk),							 
                         'got_friends': got_friends,
                         'user_pk':str(poll.user_pk),
                         'your_friend': your_friend,
                         'pub_date':str(poll.pub_date),
                         'start_date':str(poll.start_date),
                         'end_date':str(poll.end_date),
                         'address':str(poll.address),
                         'state':str(poll.state),
                         'zip':str(poll.zip),
                         'city':str(poll.city),					 
                         'rent':poll.rent,				 
                         'room_pic1': img_addr,						 
                         'num_bed':str(poll.num_bed),						 
                         'num_bath':str(poll.num_bath)})	

    serialized_obj = json.dumps(poll_ser)	
    # serialized_obj = serializers.serialize('json', latest_poll_list)	
    return HttpResponse(serialized_obj, content_type='application/json')	
	
def comment_event(request):
    if request.user.is_authenticated():
        try: p = Poll.objects.get(pk=request.POST['event_id'])
        except ObjectDoesNotExist:
           	return HttpResponse("\"event not exist\"", content_type="application/json")				
        p.comment_set.create( commenter_pk=request.user.id,
                             comment_text=request.POST['comment'],
                             pub_date=timezone.now())			
        return HttpResponse("\"success\"", content_type="application/json")  
    else:            
        return HttpResponse("\"not authorized\"", content_type="application/json") 	
	
def get_username(pk):
    try: person=FacebookCustomUser.objects.get(pk=pk)	
    except ObjectDoesNotExist:
        return 'Mr.x'
    return person.username
	
def get_fb_id(pk):
    try: person=FacebookProfile.objects.get(user_id=pk)	
    except ObjectDoesNotExist:
        return 0
    return person.facebook_id	

def get_fb_pic(pk):
    try: person=FacebookProfile.objects.get(user_id=pk)	
    except ObjectDoesNotExist:
        return 'default_profile_pic.jpg'
    return str(person.image)		

def get_fb_url(pk):
    try: person=FacebookProfile.objects.get(user_id=pk)	
    except ObjectDoesNotExist:
        return ''
    return str(person.facebook_profile_url)		