from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.urlresolvers import reverse
from polls.models import Poll
from decimal import Decimal
import os
import datetime
from django.conf import settings
from django.core import serializers
import json
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
@csrf_exempt
def index(request):  
        return HttpResponseRedirect('index.html')
      

def poll_page(request):  
        return HttpResponseRedirect('poll.html')		