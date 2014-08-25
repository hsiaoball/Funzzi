from django.db import models
from django import forms
from django.contrib.auth.models import User, UserManager
import os
from django.conf import settings
from django_facebook.models import FacebookCustomUser, FacebookUser, FacebookProfile
# from allauth.socialaccount.models import SocialAccount
# from allauth.account.models import EmailAddress
import hashlib

def get_profile_image_path(username, filename):
    if 'OPENSHIFT_DATA_DIR' in os.environ:
        return os.path.join('login/profile_pic', str(username)+os.path.splitext(filename)[1])
    else:	
	    return os.path.join('login/profile_pic', str(username)+os.path.splitext(filename)[1])
	# return os.path.join('profile_pic', str(username)+'_'+filename)
	

 
# class UserProfile(models.Model): 
    # user = models.OneToOneField(User, related_name='profile')
    # def __unicode__(self):
        # return "{}'s profile".format(self.user.username)
 
    # class Meta:
        # db_table = 'user_profile'
 
    # def account_verified(self):
        # if self.user.is_authenticated:
            # result = EmailAddress.objects.filter(email=self.user.email)
            # if len(result):
                # return result[0].verified
        # return False
    # def profile_image_url(self):
        # fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
        # if len(fb_uid):
            # return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
 
        # return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())		
 
# User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])	
#generate a string, which is not already existing in the earlier Promotion instances
def code_generate():
    while 1:
        # from django.conf import settings
        import random, string
        prom_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
        return prom_code		
        # try:
            # Promotion.objects.get(promotion_code=prom_code)
        # except:
            # return prom_code


class model_addfield(FacebookCustomUser):
    email_confirmed =	models.BooleanField(default=0)
    confirmation_code =  models.CharField(max_length=33,default=code_generate)	
    objects = UserManager()	
	
class notice(models.Model):
    model_addfield = models.ForeignKey(model_addfield)
    date=models.DateTimeField('date published')
    noticer=models.IntegerField()
    post_id=models.IntegerField()
    notice_type=models.IntegerField() # 1: ask question 2: deal request
    un_read_notice=	models.IntegerField()
    def print_date(self):
        return str(self.date.year)+'-'+str(self.date.month)+'-'+str(self.date.day)+'T'+str(self.date.hour)+':'+str(self.date.minute)+':'+str(self.date.second)+'Z'

			
class CustomUser(models.Model):
    reputation =models.DecimalField(max_digits=9, decimal_places=4,default=0)
    profile_pic = models.ImageField(upload_to=get_profile_image_path, blank=True, null=True, default = 'default_profile_pic.jpg') 
    email_confirmed =	models.DecimalField(max_digits=1, decimal_places=1,default=0)
    confirmation_code =  models.CharField(max_length=33,default=code_generate)
#    objects = UserManager()

class Comment(models.Model):
    CustomUser = models.ForeignKey(CustomUser)	 
    comment_text = models.CharField(max_length=200)
    commenter_pk =	models.IntegerField(max_length=100)
    pub_date = models.DateTimeField('date published') 

class like(models.Model):
    CustomUser = models.ForeignKey(CustomUser)	 
    like_level = models.DecimalField(max_digits=9, decimal_places=4,default=0)
    liker_pk =	models.IntegerField(max_length=100)
    pub_date = models.DateTimeField('date published') 	

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()	