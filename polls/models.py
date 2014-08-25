import datetime
from django.utils import timezone
from django.db import models
from django import forms
import os

# Create your models here.
def wrapper(poll, filename, order):
    if 'OPENSHIFT_DATA_DIR' in os.environ:
        return os.path.join('polls/post_pic', str(poll.pk)+str(order)+os.path.splitext(filename)[1])
    else:	
        return os.path.join('polls/post_pic', str(poll.pk)+str(order)+os.path.splitext(filename)[1])
		
def get_room_image_path1(poll, filename):
    order=1
    if 'OPENSHIFT_DATA_DIR' in os.environ:
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])
    else:	
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])
 


def get_room_image_path2(poll, filename):
    order=2
    if 'OPENSHIFT_DATA_DIR' in os.environ:
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])
    else:	
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])   

def get_room_image_path3(poll, filename):
    order=3
    if 'OPENSHIFT_DATA_DIR' in os.environ:
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])
    else:	
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1]) 

def get_room_image_path4(poll, filename):
    order=4
    if 'OPENSHIFT_DATA_DIR' in os.environ:
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])
    else:	
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])  
def get_room_image_path5(poll, filename):
    order=5
    if 'OPENSHIFT_DATA_DIR' in os.environ:
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])
    else:	
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])   
def get_room_image_path6(poll, filename):
    order=6
    if 'OPENSHIFT_DATA_DIR' in os.environ:
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])
    else:	
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])    
def get_room_image_path7(poll, filename):
    order=7
    if 'OPENSHIFT_DATA_DIR' in os.environ:
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])
    else:	
        return os.path.join('polls/post_pic', str(poll.pk)+'_'+str(order)+os.path.splitext(filename)[1])   		
			
class Poll(models.Model):
    user_pk = models.IntegerField()
    user_field =models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    state =models.CharField(max_length=30)
    # zip=models.DecimalField(max_digits=5, decimal_places=5,default=0)
    city=models.CharField(max_length=30)
    zip = models.IntegerField()
	
    pub_date = models.DateTimeField('date published')
    rent= models.IntegerField()
    start_date = models.DateTimeField(auto_now=False)
    end_date = models.DateTimeField(auto_now=False)
    num_bed=models.IntegerField()
    num_bath=models.IntegerField()
    
    room_pic1 = models.ImageField(upload_to=get_room_image_path1, blank=True, null=True, default = '')     
    room_pic2 = models.ImageField(upload_to=get_room_image_path2, blank=True, null=True, default = '')
    room_pic3 = models.ImageField(upload_to=get_room_image_path3, blank=True, null=True, default = '')
    room_pic4 = models.ImageField(upload_to=get_room_image_path4, blank=True, null=True, default = '')
    room_pic5 = models.ImageField(upload_to=get_room_image_path5, blank=True, null=True, default = '')
    room_pic6 = models.ImageField(upload_to=get_room_image_path6, blank=True, null=True, default = '')
    room_pic7 = models.ImageField(upload_to=get_room_image_path7, blank=True, null=True, default = '')	
    content = models.CharField(max_length=5000,default=0)
	#property
    size= models.IntegerField()
    property_type=models.DecimalField(max_digits=2, decimal_places=1, null=True)# 0:townhouse 1:SFH 2:condo 3:apt
    floor_level=models.DecimalField(max_digits=2, decimal_places=1, null=True)	
    parking=models.DecimalField(max_digits=2, decimal_places=1, null=True)	#0: no 1:garage 2: coverd top	3:street
    pet = models.DecimalField(max_digits=2, decimal_places=1, null=True)	#0: no 1: both 2: dog 3:cat	
    smoke = models.NullBooleanField(null=True)
    private_bath = models.NullBooleanField( null=True)
    washer_dryer=models.DecimalField(max_digits=2, decimal_places=1, null=True)	#0: no 1: in unit 2: public		
    kitchen_access=	models.NullBooleanField( null=True)
    internet=	models.NullBooleanField( null=True)    	
    cable_tv=	models.NullBooleanField( null=True)	
	#Community Features
    park=	models.NullBooleanField( null=True)	
    play_ground=	models.NullBooleanField( null=True)	
    tennis=	models.NullBooleanField( null=True)	
    basketball=	models.NullBooleanField( null=True)	
    swim_pool=	models.NullBooleanField( null=True)	
    jacuzzi=	models.NullBooleanField( null=True)	
    gym=	models.NullBooleanField( null=True)	
    bbq_area=	models.NullBooleanField( null=True)	
	#Rent include
    rent_internet=	models.NullBooleanField( null=True)	
    rent_cable_tv=	models.NullBooleanField( null=True)		
    rent_water=	models.NullBooleanField( null=True)		
    rent_gas=	models.NullBooleanField( null=True)		
    rent_electricity=	models.NullBooleanField( null=True)		
    rent_garbage=	models.NullBooleanField( null=True)		
    rent_parking=	models.NullBooleanField( null=True)			
	
    def passed_event(self):
        now = timezone.now()	 
        if	self.start_date.date() >= datetime.date.today():
		    return False
        else:
            return True		
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <  now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Guest_list(models.Model):
    poll = models.ForeignKey(Poll)
    guest_name = models.CharField(max_length=200)
    guest_pk = models.IntegerField()		
    status = models.CharField(max_length=200)
    def __unicode__(self):  # Python 3: def __str__(self):
      return self.guest_name
	  

	  
class Comment(models.Model):
    poll = models.ForeignKey(Poll)	
    commenter_pk = models.IntegerField()	
    comment_text = models.CharField(max_length=200)
    commenter =	models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')

class Questions(models.Model):
    poll = models.ForeignKey(Poll)	
    commenter_pk = models.IntegerField()	
    host=models.BooleanField()	
    comment_text = models.CharField(max_length=400)
    pub_date = models.DateTimeField('date published')    
    
class ImageUploadForm(forms.Form):
    """Image upload form."""
    image1 = forms.ImageField()
    image2 = forms.ImageField()    
    image3 = forms.ImageField()    	
    image4 = forms.ImageField()    
    image5 = forms.ImageField()    	
    image6 = forms.ImageField()    
    image7 = forms.ImageField()    	