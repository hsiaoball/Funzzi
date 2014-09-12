from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from login.models import CustomUser, ImageUploadForm,model_addfield,notice
import os
from django.conf import settings
from django.core.mail import send_mail
import urllib
from django.core import serializers
from django.contrib.auth import get_user_model
from polls.views import get_username,get_fb_pic
# User = get_user_model()
User= model_addfield

@csrf_exempt	
def index(request):
    if 'function_name' in request.POST: 
        function_name=request.POST['function_name']
        if function_name=='profile':		
            return profile_view(request,request.POST['user_name']);	
    if 'username' not in request.POST:
        return HttpResponse("\"no username\"", content_type="application/json")
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request,user)
            if request.is_ajax():
                return HttpResponse(user.id, content_type="application/json")		
            return redirect('/polls/')
            # return render(request, 'polls/index.html')
        else:
            return HttpResponse("\"Disable account\"", content_type="application/json")		
    else:
        return HttpResponseBadRequest("\"invalid login\"", content_type="application/json")		

      
        
@csrf_exempt
def create(request):
    if 'username' in request.POST:
        username=request.POST['username']  
        password=request.POST['pw']
        if request.POST['pw'] != request.POST['pw_2']:
            return render(request, 'login/create.html',{'error_message': "password is not match."})
        if not username:
            return render(request, 'login/create.html',{'error_message': "Pleas enter username."})
        if User.objects.filter(username=username).exists():    
            return render(request, 'login/create.html',{'error_message': "username existed."})
        else:
            user = User.objects.create_user(username=request.POST['username'],
                                                  password=request.POST['pw'])
            user.save()                                      
            form = ImageUploadForm(request.POST, request.FILES)
            user = authenticate(username=username, password=password)
            login(request,user)
            if request.is_ajax():		
                return HttpResponse(request.user.id, content_type="application/json")			
            else:				  
                return render(request,'login/profile.html')    
    else:
        return render(request, 'login/create.html')

def profile_view_json(request,p_name):
    if CustomUser.objects.filter(username=p_name).exists():
        poster=CustomUser.objects.get(username=p_name)
        serialized_obj = serializers.serialize('json', [ poster, ])		
        # response_data = {}
        # response_data['id'] = poster.username
        # response_data['live_area'] = poster.live_area		
        return HttpResponse(serialized_obj, content_type="application/json")		
    else:
        return render(request, 'login/profile.html', {'error_msg': "The username is not existed" ,'p_name':p_name}) 

@csrf_exempt		
def check_login(request):
    if request.user.is_authenticated():
        groups_and_items = {}
        groups_and_items['id']=request.user.id
        groups_and_items['username']=request.user.username
        groups_and_items['profile_pic']=get_fb_pic(request.user.id)
      
        user= User.objects.get(pk=request.user.id)	
        notice_group=[]
        for notice in user.notice_set.all().order_by('-date')[:20]:
            if notice.notice_type == 1:
                notice_type='asked you a question about post '
            elif notice.notice_type == 2:    
                notice_type='sent you a deal request about post '
            else:    
                notice_type='not define'                
            notice_group.append( {'notice_pk': str(notice.pk), 'giver_pic':get_fb_pic(notice.noticer), 'notice_type': str(notice_type), 'un_read_notice': str(notice.un_read_notice), 'post_id': str(notice.post_id), 'notice_giver_id': str(notice.noticer), 'notice_giver': get_username(notice.noticer), 'date':str(notice.date), 'time':str(notice.date.hour)+':'+str(notice.date.minute) })	
        groups_and_items['un_read_notice_num']=user.notice_set.filter(un_read_notice=1).count()  	
        groups_and_items['notice']=notice_group	
        serialized_obj = json.dumps(groups_and_items)
        return HttpResponse(serialized_obj, content_type="application/json")
    else:
        return HttpResponse(0, content_type="application/json")	


def set_read_notice(request):      
    if request.user.is_authenticated():
        user= User.objects.get(pk=request.user.id)
        if 'notice_id' not in request.POST:
            return HttpResponse("\"no notice id\"", content_type="application/json")         
        read_notice=user.notice_set.get(pk=request.POST['notice_id'])
        read_notice.un_read_notice=0
        read_notice.save();
        return HttpResponse("\"success\"", content_type="application/json") 
        
@csrf_exempt		
def profile_view(request,p_name):
    if CustomUser.objects.filter(username=p_name).exists():
        poster=CustomUser.objects.get(username=p_name)
        if 'comment' in request.POST:
            if not request.user.is_authenticated():
                return render(request, 'login/profile.html', {'error_msg': 'Please login before comment'})
            poster.comment_set.create(comment_text=request.POST['comment'], commenter=request.user.username, pub_date=timezone.now()) 		
        elif 'like' in request.POST:
            if not poster.like_set.filter(liker=request.user.username).exists():		    
                poster.reputation=poster.reputation+1    
                poster.like_set.create(liker=request.user.username, pub_date=timezone.now()) 
                poster.save()
        elif 'unlike' in request.POST:
            if poster.like_set.filter(liker=request.user.username).exists():		
                poster.reputation=poster.reputation-1    
                like=poster.like_set.get(liker=request.user.username) 
                like.delete()
                poster.save()   
        if request.is_ajax():
            serialized_obj = serializers.serialize('json', [ poster, ])	
            return HttpResponse(serialized_obj, content_type="application/json")
        else:			
            return render(request, 'login/profile.html', {'poster': poster,})		
    else: #user not exist
        if request.is_ajax():
            return HttpResponse([], content_type='application/json')		
        else:
            return render(request, 'login/profile.html', {'error_msg': "The username is not existed" ,'p_name':p_name})    

def profile_view2(request,p_name,p_name2):
    name=p_name+'.'+p_name2
    return profile_view(request,name)     

def profile_view3(request,p_name,p_name2,p_name3):
    name=p_name+'.'+p_name2+'.'+p_name3
    return profile_view(request,name)       		


@csrf_exempt		
def profile(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.profile_pic = form.cleaned_data['image']
            if len(request.user.profile_pic) > settings.MAX_PROFILE_PIC_SIZE:
                      return render(request, 'login/profile.html',{'error_message': "upload profile pic > 2MB, Please choose smaller file."})
            request.user.save()    
            return render(request,'login/profile.html', {'msg':'form is valid'})
        return render(request,'login/profile.html', {'msg':form.errors})            
    # return render(request,'login/profile.html', {'msg':'NO post', 'profile_url': os.path.dirname(settings.MEDIA_ROOT)})            
    # return render(request,'login/profile.html', {'msg':'NO post', 'profile_url': os.path.join(os.path.relpath(os.path.dirname('foo/bar/bar_file.txt'),os.path.dirname('foo/foo_file.txt')),os.path.basename('foo/bar/bar_file.txt'))})        
    # return render(request,'login/profile.html', {'msg':'NO post', 'profile_url': os.path.relpath(os.path.dirname(), os.path.dirname(settings.MEDIA_ROOT))})            
    return render(request,'login/profile.html', {'msg':''})        

@csrf_exempt    
def logout_view(request):
    logout(request)    
    if request.is_ajax():	
        return HttpResponse('true', content_type='application/json')	
    else:		
        return redirect('/polls/')
    
def update(request):
    if request.method == 'POST': #update user
        if CustomUser.objects.filter(username=request.user.username).exists():
            update_user=CustomUser.objects.get(username=request.user.username)
            if request.POST['type']== 'other':
                type=request.POST['other_type']
            else:
                type = request.POST['type']
            update_user.live_area = request.POST['live']
            update_user.type = type
            update_user.fav_level=request.POST['level']
            update_user.fav_resort=request.POST['resort']
            update_user.fav_hotel=request.POST['hotel']
            update_user.ticket_type=request.POST['ticket']
            update_user.save()                                      
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                update_user.profile_pic = form.cleaned_data['image']
                if len(update_user.profile_pic) > settings.MAX_PROFILE_PIC_SIZE:
                      return render(request, 'login/update.html',{'error_message': "upload profile pic > 2MB, Please choose smaller file."})
                update_user.save()
            return redirect('/login/profile/'+update_user.username)    
    else:#go to update page
        if CustomUser.objects.filter(username=request.user.username).exists():
            update_user=CustomUser.objects.get(username=request.user.username)		
            return render(request, 'login/update.html',{'update_user':update_user})
        else:	
            return render(request, 'login/update.html',{'update_user':request.user})		
        
def fb_login(request):
    # return render(request, 'polls/fb.html',{'STATIC_URL': settings.STATIC_ROOT})
    return render(request, 'login/fb.html',{'STATIC_LOCAL_URL': "/"})
	
def send_registration_confirmation(request):
    try: p = User.objects.get(id=request.user.id)
    except ObjectDoesNotExist:
       	return HttpResponse("\"User not exist\"", content_type="application/json")     
    title = "NestQ account confirmation"
    content = "Welcome to NestQ.\n You are one step closer to find the perfect rentals/tenants! To complete sign-up for NestQ, please verify your email address.\n \"Clic here to verify your account\" \n\n"+settings.SERVER_URL +"login/email_link/"+ str(p.confirmation_code) + "/" + str(p.id)
    send_mail(title, content, 'hsiaoball@gmail.com', [p.email], fail_silently=False)	
    return HttpResponse('Sent confirm', content_type='application/json')	    
	
def email_link(request, code, user_id):
   try: p = User.objects.get(id=request.user.id)
   except ObjectDoesNotExist:
      	return HttpResponse("\"User not exist\"", content_type="application/json")     			
   if p.confirmation_code == code:				 
       p.email_confirmed=True
       p.save()
       return HttpResponseRedirect('../../../index.html')
   else:	
       return HttpResponse("\"email code mismatched\"", content_type="application/json")     									
