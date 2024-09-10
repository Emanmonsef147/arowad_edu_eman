from django.shortcuts import render ,redirect,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect, requires_csrf_token,csrf_exempt
from django.http import HttpResponse
from usermgr.models import *
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django_ratelimit.core import is_ratelimited,get_usage
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view , permission_classes# Create your views here.
from django.http import  JsonResponse
from .serializers import *
import os
from django.conf import settings
import base64

@csrf_exempt
def indexo(request):
    try:
        request.GET.get('token', '')
    except Exception:
        return redirect("https://manfa3a.infinitybridge.org")

    token = request.GET.get('token', '')
    print("tototo",token)
    if 'token' in request.session:
        if request.session['token'] != token:
            del request.session['token']

    if 'token' in request.session:
        token = request.session['token']
        print("toto from session",token )
        if Token.objects.filter(key=token).count() > 0:
            print("token")
            idd = Token.objects.get(key=token).user_id
            if User_Type.objects.get(user_id_id=idd).user_type != "superadmin":
                #####seee the latest chatgpt  response to https
                # request.session['token'] = token
                # return HttpResponseRedirect(reverse('publicurls'))
                return redirect('https://manf3a.infinitybridge.org/')
            else:

                return redirect('/home')

                # return render(request, 'home.html', {'token': token})
            # else:
            ### save to session and redirect to /
            ####   in / check the session and keep or redirect to main page
        else:
            # return redirect('/publicurls')
            return redirect('https://manf3a.infinitybridge.org/')

    else:
        if token is not None or token != "":

            if Token.objects.filter(key=token).count() > 0:
                idd=Token.objects.get(key=token).user_id
                if User_Type.objects.get(user_id_id=idd).user_type == "superadmin":
                    #####seee the latest chatgpt  response to https
                    request.session['token'] = token
                    # return HttpResponseRedirect(reverse('publicurls'))
                    return redirect('/home')

                # return render(request, 'home.html', {'token': token})
            else:
                # del request.session['token']
                return redirect('https://manf3a.infinitybridge.org/')
                  ### save to session and redirect to /
                 ####   in / check the session and keep or redirect to main page
        else:
            return redirect('https://manf3a.infinitybridge.org/')

    # request.set_cookie['stg']='stg'
    return render(request, 'index.html')


@csrf_exempt
def setoneuser(request,id=None):
    print(id)
    if 'user_one_id' in request.session:
        del request.session['user_one_id']
    if id is None or id == '':
        return redirect('/viewusers')
    else:
        if not id.isdigit():
            return redirect('/viewusers')
        if User.objects.filter(id=id).count() > 0:

            request.session['user_one_id']=id
        else:
            return redirect('/viewusers')




    return render(request, 'index.html')

@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def getoneuser(request):
    if \
    get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)[
        'count'] > 120:
        return JsonResponse({"error": "too_many_requests"})
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    toto = oneuserSerializer(data=request.data)
    if toto.is_valid():
        idd=toto.data['idd']
        if not str(idd).isdigit():
            return JsonResponse({"error":"invalid user id"})
        if User.objects.filter(id=idd).count() < 1:
            return JsonResponse({"error":"invalid user id"})
        user=User.objects.get(id=idd)
        profile=User_Profile.objects.get(user_id_id=user.id)
        profile_img=""

        mediaroot = os.path.abspath(settings.MEDIA_ROOT)
        with open(mediaroot + '/' + str(profile.userimg), "rb") as image_file:
            # with open("media/" + str(uouo.userimg), "rb") as image_file:

            profile_img = base64.b64encode(image_file.read()).decode("utf-8")
        return JsonResponse({"success":{
            'email':user.email,
            'username':user.username,
            'user_id':user.id,
            'is_active':user.is_active,
            'date_joined':user.date_joined,
            'fullname':profile.fullname,
            'phone':profile.phone,
            'address':profile.address,
            'birth':profile.birth,
            'admin_msg':profile.admin_msg,
            'nat_id':profile.nat_id,
            'profile_img':profile_img,
            'user_type':User_Type.objects.get(user_id=user.id).user_type,
            'user_urls':list(Private_Url.objects.filter(id__in=User_urls.objects.filter(user_id_id=user.id).values_list('url_id', flat=True)).values('url','id'))


        }})
    else:
        return JsonResponse({"error",toto.errors})






