from django.shortcuts import render
from .models import *
from django.shortcuts import  redirect
from django.http import  JsonResponse
from  validate_email  import validate_email
import re
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import base64
from django.core.mail import EmailMessage,send_mail,EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from cryptography.fernet import  Fernet
from datetime import timedelta
from rest_framework.permissions import AllowAny

from rest_framework.decorators import api_view , permission_classes# Create your views here.
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view,action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_ratelimit.core import is_ratelimited,get_usage
import os
from .serializers import *
from django.utils.safestring import mark_safe
from django.conf import settings

# Create your views here.
def get_ipp(request):
    ip = ""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]

    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def reg_validation(request):

    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    re_password = request.POST.get('re_password')
    full_name = request.POST.get('full_name')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    user_type = request.POST.get('user_type')
    if username is None:
        return JsonResponse({ 'error': 'اسم المستخدم مطلوب'})
    if email is None:
        return JsonResponse({'error':  'البريد الالكتروني مطلوب'})
    if password is None:
        return JsonResponse({'error':  'كلمة المرور مطلوبة'})
    if re_password is None:
        return JsonResponse({'error': 'كلمة المرور مطلوبة'})
    if full_name is None:
        return JsonResponse({'error':  'الاسم بالكامل مطلوب'})
    if phone is None:
        return JsonResponse({'error':  'رقم الهاتف مطلوب'})
    if address is None:
        return JsonResponse({'error': 'العنوان مطلوب'})
    if user_type is None:
        return JsonResponse({'error':  'نوع المستخدم مطلوب'})
    if password != re_password:
        return JsonResponse({'status': 'error', 'message': 'كلمتا المرور غير متطابقتان'})
    if len(username) < 8:
        return JsonResponse({'error':  'اسم المستخدم يجب ان يكون 8 حروف على الأقل'})
    if len(password) < 8:
        return JsonResponse({'error':  'كلمة المرور يجب ان يكون 8 حروف على الأقل'})
    if len(full_name) < 8:
        return JsonResponse({'error':  'الاسم بالكامل يجب ان يكون 8 حروف على الأقل'})
    if len(phone) < 11:
        return JsonResponse({'error':  'رقم الهاتف يجب ان يكون 11 حروف على الأقل'})
    if len(address) < 10:
        return JsonResponse({'error':  'العنوان يجب ان يكون 10 حروف على الأقل'})
    if any(var.isdigit() for var in username):
        return JsonResponse({'error':  'اسم المستخدم يجب ان يكون حروف فقط'})
    special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    # if any(c in special_characters for c in password):

    #         return Response({'error':'password_no_special'})
    if (special_char.search(username) != None):
        return JsonResponse({'error': 'اسم المستخدم يجب ان لا يحتوي على علامات خاصه'})
    res = any(ele.isupper() for ele in password)
    if res == False:
        return JsonResponse({'error': 'كلمة المرور يجب ان تحتوي على حرف كبير على الاقل'})
    resl = any(ele.islower() for ele in password)

    if resl == False:
        return JsonResponse({'error': 'كلمة المرور يجب ان تحتوي على حرف صغير على الاقل'})
    resd = any(ele.isdigit() for ele in password)

    if resd == False:
        return JsonResponse({'error': 'كلمة المرور يجب ان تحتوي على رقم على الاقل'})
    special_characters = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    # if any(c in special_characters for c in password):

    #         return Response({'error':'password_no_special'})
    if (special_char.search(password) == None):
        return JsonResponse({'error': 'كلمة المرور يجب ان تحتوي على علامة خاصة على الاقل'})
    if email is not None:
        if len(email) < 8:
            return JsonResponse({'error': 'البريد الاكتروني يجب ان يكون اكبر من 8 احرف'})
        if not validate_email(email):
            return JsonResponse({'error': 'بريد الكتروني خاطئ'})
    else:
        return JsonResponse({'error': 'بريد الكتروني خاطئ'})
    if not any(var.isdigit() for var in phone):
        return JsonResponse({'status': 'error', 'message': 'رقم الهاتف يجب ان يكون ارقام فقط'})
    if User.objects.filter(username=username).count() > 0:
        return JsonResponse({'error':  'اسم المستخدم مسجل من قبل'})
    if User.objects.filter(email=email).count() > 0:
        return JsonResponse({'error': 'البريد الالكتروني مسجل من قبل'})
    if User.objects.filter(phone=phone).count() > 0:
        return JsonResponse({'error':  'رقم الهاتف مسجل من قبل'})

    if not user_type in ['seller','marketer']:

      return JsonResponse({'error':  'نوع المستخدم غير صحيح'})


    return [ username , email, password,phone,full_name,address,user_type]

@api_view(['POST'])
@permission_classes([AllowAny, ])
def register_seller(request):
    if get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)['count'] > 120:
        return JsonResponse({"error": "too_many_requests"})
    permission_classes = [AllowAny]
    reg_info = RegSerializer(data=request.data)
    if reg_info.is_valid():
        username = reg_info.data['username']
        email = reg_info.data['email']
        password = reg_info.data['password']
        re_password = reg_info.data['re_password']
        full_name = reg_info.data['full_name']
        phone = reg_info.data['phone']
        address = reg_info.data['address']
        user_type = reg_info.data['user_type']
        if password != re_password:
            return JsonResponse({ 'error':'كلمتا المرور غير متطابقتان'})
        if len(username) < 8:
            return JsonResponse({'error': 'اسم المستخدم يجب ان يكون 8 حروف على الأقل'})
        if len(password) < 8:
            return JsonResponse({'error': 'كلمة المرور يجب ان يكون 8 حروف على الأقل'})
        if len(full_name) < 8:
            return JsonResponse({'error': 'الاسم بالكامل يجب ان يكون 8 حروف على الأقل'})
        if len(phone) < 11:
            return JsonResponse({'error': 'رقم الهاتف يجب ان يكون 11 حروف على الأقل'})
        if len(address) < 10:
            return JsonResponse({'error': 'العنوان يجب ان يكون 10 حروف على الأقل'})
        for vars in username:
            if vars.isdigit():
                return JsonResponse({'error': 'اسم المستخدم يجب ان يكون حروف فقط'})
            
        special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        # if any(c in special_characters for c in password):

        #         return Response({'error':'password_no_special'})
        if (special_char.search(username) != None):
            return JsonResponse({'error': 'اسم المستخدم يجب ان لا يحتوي على علامات خاصه'})
        res = any(ele.isupper() for ele in password)
        if res == False:
            return JsonResponse({'error': 'كلمة المرور يجب ان تحتوي على حرف كبير على الاقل'})
        resl = any(ele.islower() for ele in password)

        if resl == False:
            return JsonResponse({'error': 'كلمة المرور يجب ان تحتوي على حرف صغير على الاقل'})
        resd = any(ele.isdigit() for ele in password)

        if resd == False:
            return JsonResponse({'error': 'كلمة المرور يجب ان تحتوي على رقم على الاقل'})
        special_characters = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        # if any(c in special_characters for c in password):

        #         return Response({'error':'password_no_special'})
        if (special_char.search(password) == None):
            return JsonResponse({'error': 'كلمة المرور يجب ان تحتوي على علامة خاصة على الاقل'})
        if email is not None:
            if len(email) < 8:
                return JsonResponse({'error': 'البريد الاكتروني يجب ان يكون اكبر من 8 احرف'})
            if not validate_email(email):
                return JsonResponse({'error': 'بريد الكتروني خاطئ'})
        else:
            return JsonResponse({'error': 'بريد الكتروني خاطئ'})
        if not any(var.isdigit() for var in phone):
            return JsonResponse({'error': 'رقم الهاتف يجب ان يكون ارقام فقط'})
        if User.objects.filter(username=username).count() > 0:
            return JsonResponse({'error': 'اسم المستخدم مسجل من قبل'})
        if User.objects.filter(email=email).count() > 0:
            return JsonResponse({'error': 'البريد الالكتروني مسجل من قبل'})
        if User_Profile.objects.filter(phone=phone).count() > 0:
            return JsonResponse({'error': 'رقم الهاتف مسجل من قبل'})

        if not user_type in ['seller', 'marketer']:
            return JsonResponse({'error': 'نوع المستخدم غير صحيح'})

        if not user_type == 'seller':
            return JsonResponse({ 'error': 'نوع المستخدم غير صحيح'})
        User.objects.create_user(username=username, email=email, password=password, is_active=False)
        user_id=User.objects.get(username=username, email=email)
        User_Profile.objects.create(user_id=user_id,fullname=full_name,phone=phone,address=address,)
        User_Type.objects.create(user_id=user_id,user_type=user_type,ip_address=get_ipp(request))
        html_content = render_to_string("seller_account_created.html", {"title": "منفعة"
            , "content": " تم التسجيل بنجاح "})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            "منصة منفعة",
            text_content,
            'nanomanfaa@outlook.com',
            [email],
        )
        email.attach_alternative(html_content, 'text/html')
        email.send()
        return JsonResponse({'success': 'تم التسجيل بنجاح\n سيتم التواصل معكم لتنشيط الحساب'})
    else:
        return JsonResponse({'error':reg_info.errors})


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register_marketer(request):
    if  get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)[
        'count'] > 120:
        return JsonResponse({"error": "too_many_requests"})
    permission_classes = [AllowAny]
    reg_info = RegSerializer(data=request.data)
    if reg_info.is_valid():
        username = reg_info.data['username']
        email = reg_info.data['email']
        password = reg_info.data['password']
        re_password = reg_info.data['re_password']
        full_name = reg_info.data['full_name']
        phone = reg_info.data['phone']
        address = reg_info.data['address']
        user_type = reg_info.data['user_type']
        if password != re_password:
            return JsonResponse({'status': 'error', 'message': 'كلمتا المرور غير متطابقتان'})
        if len(username) < 8:
            return JsonResponse({'error': 'اسم المستخدم يجب ان يكون 8 حروف على الأقل'})
        if len(password) < 8:
            return JsonResponse({'error': 'كلمة المرور يجب ان يكون 8 حروف على الأقل'})
        if len(full_name) < 8:
            return JsonResponse({'error': 'الاسم بالكامل يجب ان يكون 8 حروف على الأقل'})
        if len(phone) < 11:
            return JsonResponse({'error': 'رقم الهاتف يجب ان يكون 11 حروف على الأقل'})
        if len(address) < 10:
            return JsonResponse({'error': 'العنوان يجب ان يكون 10 حروف على الأقل'})
        if any(var.isdigit() for var in username):
            return JsonResponse({'error': 'اسم المستخدم يجب ان يكون حروف فقط'})
        special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        # if any(c in special_characters for c in password):

        #         return Response({'error':'password_no_special'})
        if (special_char.search(username) != None):
            return JsonResponse({'error': 'اسم المستخدم يجب ان لا يحتوي على علامات خاصه'})
        res = any(ele.isupper() for ele in password)
        if res == False:
            return JsonResponse({'error': 'كلمة المرور يجب ان تحتوي على حرف كبير على الاقل'})
        resl = any(ele.islower() for ele in password)

        if resl == False:
            return JsonResponse({'error': 'كلمة المرور يجب ان تحتوي على حرف صغير على الاقل'})
        resd = any(ele.isdigit() for ele in password)

        if resd == False:
            return JsonResponse({'error': 'كلمة المرور يجب ان تحتوي على رقم على الاقل'})
        special_characters = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        # if any(c in special_characters for c in password):

        #         return Response({'error':'password_no_special'})
        if (special_char.search(password) == None):
            return JsonResponse({'error': 'كلمة المرور يجب ان تحتوي على علامة خاصة على الاقل'})
        if email is not None:
            if len(email) < 8:
                return JsonResponse({'error': 'البريد الاكتروني يجب ان يكون اكبر من 8 احرف'})
            if not validate_email(email):
                return JsonResponse({'error': 'بريد الكتروني خاطئ'})
        else:
            return JsonResponse({'error': 'بريد الكتروني خاطئ'})
        if not any(var.isdigit() for var in phone):
            return JsonResponse({'status': 'error', 'message': 'رقم الهاتف يجب ان يكون ارقام فقط'})
        if User.objects.filter(username=username).count() > 0:
            return JsonResponse({'error': 'اسم المستخدم مسجل من قبل'})
        if User.objects.filter(email=email).count() > 0:
            return JsonResponse({'error': 'البريد الالكتروني مسجل من قبل'})
        if User_Profile.objects.filter(phone=phone).count() > 0:
            return JsonResponse({'error': 'رقم الهاتف مسجل من قبل'})

        if not user_type in ['seller', 'marketer']:
            return JsonResponse({'error': 'نوع المستخدم غير صحيح'})


        if not user_type == 'marketer':
                return JsonResponse({'error': 'نوع المستخدم غير صحيح'})

        User.objects.create_user(username=username, email=email, password=password,is_active=False)
        user_id = User.objects.get(username=username, email=email)
        User_Profile.objects.create(user_id=user_id, fullname=full_name, phone=phone, address=address, )
        User_Type.objects.create(user_id=user_id, user_type=user_type, ip_address=get_ipp(request))
        key = b'HgwhGsa9t-k9Eat8nMM1X4w-DUBxhNzvKIU7kqWrRjo='

        cipher_suite = Fernet(key)
        encoded_text = cipher_suite.encrypt(bytes(email, 'utf-8'))
        rp = Activateaccount.objects.create(link=str(encoded_text)[2:-1])
        rp.save()

        html_content = render_to_string("marketer_account_created.html", {"title": "منفعة"
           , "content": "http://localhost:5173/activate/"+str(encoded_text)[2:-1]})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            "منصة منفعة",
            text_content,
            'nanomanfaa@outlook.com',
            [email],
        )
        email.attach_alternative(html_content, 'text/html')

        email.send()
        return JsonResponse({'success': "تم التسجيل بنجاح \n  قم بتنشيط الحساب من رساله البريد الالكتروني "})
    else:
        return JsonResponse({'error':reg_info.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
def marketer_activation(request):
    if  get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)[
        'count'] > 120:
        return JsonResponse({"error": "too_many_requests"})
    # authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (AllowAny,)
    tok = activationSerializer(data=request.data)
    date1 = datetime.now()
    is_done = False
    if tok.is_valid():
        token = tok.data['token']
        date1 = datetime.now()
        key = b'HgwhGsa9t-k9Eat8nMM1X4w-DUBxhNzvKIU7kqWrRjo='
        cipher_suite = Fernet(key)
        decoded_text = cipher_suite.decrypt(bytes(token, 'utf-8'))
        print(str(decoded_text)[2:-1])
        user3 = User.objects.get(email=str(decoded_text)[2:-1])
        date1 = datetime.now()
        date2 = user3.date_joined
        date3 = str(date2)
        date4 = date3[0:18]
        date5 = datetime.strptime(date4, '%Y-%m-%d %H:%M:%S')
        diff = date1 - date5
        if diff > timedelta(minutes=59):
            # return redirect('login.html' + '?message=' + 'Link expired')
            return JsonResponse({"error": "انتهت صلاحية الرابط"})

            # return redirect('login')
        if user3.is_active:
            return JsonResponse({"error": "الحساب منشط بالفعل"})
            # print(User.username + ' is already activated')
            # return redirect('/login')

            # else:
        user3.is_active = True
        # userprof = Patients.objects.get(patient_id=user3.id)
        user3.save()
        rr = Activateaccount.objects.filter(link=token)
        rr.delete()
        # patients.active=True
        # patients.save()
        is_done = True
        return JsonResponse({"success": "تم تنتشيط الحساب بنجاح"})
    if is_done:
        return JsonResponse({"success": "تم تنشيط الحساب بنجاح"})
    else:
        return JsonResponse({"error": "error"})

@api_view(['POST'])
@permission_classes([AllowAny])
def forget_password(request):
    if  get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)[
        'count'] > 120:
        return JsonResponse({"error": "too_many_requests"})
    permission_classes = [AllowAny]

    mailo = forgetpassSerializer(data=request.data)
    id = 0
    date1 = datetime.now()
    statuss = ""
    message = ""
    if mailo.is_valid():

        mail = mailo.data['email']
        if User.objects.filter(email=mail).count() < 1:
            return JsonResponse({"error": "هذا الحساب غير موجود"})
        else:
            if Forget_time.objects.filter(email=mail).count() < 1:
                ff = Forget_time.objects.create(email=mail)
                ff.save()
                fff = Forget_time.objects.get(email=mail)
                fff.last_demand = datetime.now()
                fff.save()
                iddd = User.objects.get(email=mail).id
                user = User.objects.get(id=iddd)
                # domain=get_current_site(request).domain
                # key=Fernet.generate_key()
                key = b'HgwhGsa9t-k9Eat8nMM1X4w-DUBxhNzvKIU7kqWrRjo='
                cipher_suite = Fernet(key)
                encoded_text = cipher_suite.encrypt(bytes(mail, 'utf-8'))
                print(str(encoded_text)[2:-3])
                print(encoded_text.decode('utf-8'))
                # decoded_text = cipher_suite.decrypt(encoded_text)
                activate_url = 'http://' + 'localhost:5173' + "/reset/" + str(encoded_text)[2:-1]  # +   #link
                statuss = "success"
                message = activate_url
                rp = Reset_password.objects.create(link=str(encoded_text)[2:-1])
                rp.save()
                html_content = render_to_string("forgetEmail.html", {"title": "منصة منفعة "
                    , "content": message})
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(
                    "اعادة تعيين كلمة مرور منصة منفعة",
                    text_content,
                    'nanomanfaa@outlook.com',
                    [mail],


                )
                email.attach_alternative(html_content, 'text/html')
                email.send( fail_silently=False)
                return JsonResponse("success","تم ارسال رساله اعادة تعيين كلمة المرور ")
            else:
                date2 = Forget_time.objects.get(email=mail).last_demand
                date3 = str(date2)
                date4 = date3[0:18]
                date5 = datetime.strptime(date4, '%Y-%m-%d %H:%M:%S')
                diff = date1 - date5
                if diff < timedelta(minutes=10):
                    # statuss = "error"
                    # message = "too_many_request_in_10_minuits"
                    return JsonResponse({'error':'too_many_request_in_10_minuits'})
                else:
                    fff = Forget_time.objects.get(email=mail)
                    fff.last_demand = datetime.now()
                    fff.save()
                    iddd = User.objects.get(email=mail).id
                    user = User.objects.get(id=iddd)
                    # domain=get_current_site(request).domain
                    # key=Fernet.generate_key()
                    key = b'HgwhGsa9t-k9Eat8nMM1X4w-DUBxhNzvKIU7kqWrRjo='
                    cipher_suite = Fernet(key)
                    encoded_text = cipher_suite.encrypt(bytes(mail, 'utf-8'))
                    print(str(encoded_text)[2:-3])
                    print(encoded_text.decode('utf-8'))
                    # decoded_text = cipher_suite.decrypt(encoded_text)
                    activate_url = 'https://' + 'localhost:5173' + "/reset/" + str(encoded_text)[2:-1]  # +   #link
                    statuss = "success"
                    message = activate_url
                    rp = Reset_password.objects.create(link=str(encoded_text)[2:-1])
                    rp.save()
                    html_content = render_to_string("forgetEmail.html", {"title": "منصة منفعة"
                        , "content": message})
                    text_content = strip_tags(html_content)
                    email = EmailMultiAlternatives(
                        "اعادة تعيين كلمة مرور منصة منفعة",
                        text_content,
                        'no-reply@manfa3a.com',
                        [mail],
                    )
                    email.attach_alternative(html_content, 'text/html')
                    email.send(fail_silently=True)
                    return JsonResponse("success", "تم ارسال رساله اعادة تعيين كلمة المرور ")

        # return JsonResponse({statuss: message})



@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    if  get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)[
        'count'] > 120:
        return JsonResponse({"error": "too_many_requests"})
    permission_classes = [AllowAny]
    date1 =datetime.now()
    tok = resetpassSerializer(data=request.data)
    date1 = datetime.now()
    if tok.is_valid():
        token = tok.data['token']
        print(token)
        password = tok.data['password']
        re_password = tok.data['re_password']
        print(token)
        token_ex = Reset_password.objects.filter(link=token)

        if token_ex.count() == 0:
            return JsonResponse({'error': 'انتهت صلاحية الرابط'})

        if token_ex.count() > 0:
            date2 = token_ex[0].last_forget
            date3 = str(date2)
            date4 = date3[0:18]
            date5 = datetime.strptime(date4, '%Y-%m-%d %H:%M:%S')
            diff = date1 - date5
            if diff > timedelta(minutes=59):
                return JsonResponse({'error': 'انتهت صلاحية الرابط'})
            else:
                if password is not None:
                    if len(password) < 8:
                        return JsonResponse({'error': 'كلمة السر يجب ان تكون اكبر من 8 احرف'})
                    res = any(ele.isupper() for ele in password)
                    if res == False:
                        return JsonResponse({'error': 'كلمة السر يجب ان تحتوي على احرف كبيرة'})
                    resl = any(ele.islower() for ele in password)

                    if resl == False:
                        return JsonResponse({'error': 'كلمة السر يجب ان تحتوي على احرف صغيرة'})
                    resd = any(ele.isdigit() for ele in password)

                    if resd == False:
                        return JsonResponse({'error': 'كلمة الير يجب ان تحتوي على ارقام'})
                    special_characters = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
                    special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
                    # if any(c in special_characters for c in password):

                    #         return Response({'error':'password_no_special'})
                    if (special_char.search(password) == None):
                        return JsonResponse({'error': 'كلمة السر يجب ان تحتوي على علامات خاصة'})
                    if password != re_password:
                        return JsonResponse({'error': 'كلمتا السر غير متطابقتان'})
                    key = b'HgwhGsa9t-k9Eat8nMM1X4w-DUBxhNzvKIU7kqWrRjo='
                    cipher_suite = Fernet(key)
                    decoded_text = cipher_suite.decrypt(bytes(token, 'utf-8'))
                    print(str(decoded_text)[2:-1])
                    user_is = User.objects.filter(email=str(decoded_text)[2:-1])
                    if user_is.count() > 0:
                        uu = User.objects.get(email=str(decoded_text)[2:-1])
                        uu.set_password(password)
                        uu.save()
                        rr = Reset_password.objects.filter(link=token)
                        rr.delete()
                        return JsonResponse({'success': "تم اعادة تعيين كلمة المرور بنجاح"})
                    else:
                        return JsonResponse({'error': 'المستخدم غير موجود'})

                else:
                    return JsonResponse({'error': 'لا يوجد  كلمة سر'})
        else:
            return JsonResponse({'error': 'هذا الحساب غير موجود'})
    else:
        return JsonResponse({'error': tok.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
def chk_tok(request):
    permission_classes = [AllowAny]
    if  get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)[
        'count'] > 120:
        return JsonResponse({"error": "too_many_requests"})
    tok = checkTokenserializer(data=request.data)
    if tok.is_valid():
        token = tok.data['token']
        if Reset_password.objects.filter(link=token).count() < 1:
            return Response({'error': 'انتهت صلاحية الرابط'})

        else:
            # if Reset_password.objects.filter(link=tok).count()>0:

            return Response({'success': 'success'})
    else:
        return JsonResponse({'error':tok.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
def chk_active(request):
    permission_classes = [AllowAny]
    if get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)[
        'count'] > 120:
        return JsonResponse({"error": "too_many_requests"})
    tok = checkTokenserializer(data=request.data)
    if tok.is_valid():
        token = tok.data['token']
        if Activateaccount.objects.filter(link=token).count() < 1:
            return Response({'error': 'link_expired'})

        else:
            # if Reset_password.objects.filter(link=tok).count()>0:

            return Response({'success': 'success'})
    else:
        return JsonResponse({'success': tok.errors})

@permission_classes([IsAuthenticated])
# @action(detail=False, methods=['post'])
@api_view(['POST'])
def logouto(request):
        if  get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)[
            'count'] > 120:
            return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication)
        permission_classes = (IsAuthenticated,)
        # Delete the token associated with the user
        toto=activationSerializer(data=request.data)
        tokena=""
        if toto.is_valid():
            tokena=toto.data['token']

        # print(request.user)
            Token.objects.filter(key=tokena).delete()
            # logout(request)
            return JsonResponse({"success": "Successfully_logged_out."})
        else:
            return JsonResponse({"error":toto.errors})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def view_all_users(request):
        if   get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)[
            'count'] > 120:
            return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication, SessionAuthentication)
        permission_classes = (IsAuthenticated,)
        toto=usersSerializer(data=request.data)
        if toto.is_valid():
            tokena=toto.data['token']
            typo=toto.data['type']
            user_id=Token.objects.get(key=tokena).user_id
            # print(typo)
            if User.objects.get(id=user_id).is_superuser or User_Type.objects.get(user_id_id=user_id).user_type=='superadmin':
                if typo=='all':

                    users = User.objects.all().exclude(user_type__user_type='superadmin',is_superuser=True)
                    user_info = []
                    for user in users:
                        # profile = user.user_profile
                        print(user.id)
                        user_info.append({
                            'fullname': User_Profile.objects.get(user_id=user.id).fullname,
                            'date_joined': user.date_joined,
                            'is_active': user.is_active,
                            'user_type': User_Type.objects.get(user_id_id=user.id).user_type,
                            'user_id': user.id
                        })
                    return JsonResponse({'success':user_info})
                else:
                    if typo in ['superadmin','admin','hr','employee', 'teacher','guardian', 'student']:
                        users = User.objects.filter(user_type__user_type=typo).exclude(user_type__user_type='superadmin',is_superuser=True)
                        user_info = []
                        for user in users:
                            # profile = user.user_profile
                            user_info.append({
                                'fullname': User_Profile.objects.get(user_id=user.id).fullname,
                                'date_joined': user.date_joined,
                                'is_active': user.is_active
                            })
                        return JsonResponse({'success':user_info})
                    else:
                        return JsonResponse({"error": "نوع المستخدم غير موجود"})
            else:
                return JsonResponse({'error':'ليس لديك صلاحيه'})
        else:
            return JsonResponse({'error':toto.errors})

@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def activate_one_user(request):
        if   get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)['count'] > 120:
             return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication, SessionAuthentication)
        permission_classes = (IsAuthenticated,)
        toto=activateuserSerializer(data=request.data)
        if toto.is_valid():
            tokena=toto.data['token']
            user_id_normal=toto.data['user_id']
            user_id = Token.objects.get(key=tokena).user_id
            if User.objects.get(id=user_id).is_superuser or User_Type.objects.get(user_id_id=user_id).user_type == 'superadmin':
                if User.objects.filter(id=user_id_normal).count() > 0:
                    if User.objects.get(id=user_id_normal).is_active:
                        return JsonResponse({"success":"هذا المستخدم تم تفعيله من قبل"})
                    else:
                        uu=User.objects.get(id=user_id_normal)
                        uu.is_active=True
                        uu.save()
                        return JsonResponse({"success":"تم التفعيل بنجاح"})
                else:
                    return JsonResponse({"error":"مستخدم غير موجود"})
            else:
                return JsonResponse({'error': 'ليس لديك صلاحيه'})
        else:
            return JsonResponse({'error': toto.errors})
@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def deactivate_one_user(request):
        if   get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)['count'] > 120:
             return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication, SessionAuthentication)
        permission_classes = (IsAuthenticated,)
        toto=activateuserSerializer(data=request.data)
        if toto.is_valid():
            tokena=toto.data['token']
            user_id_normal=toto.data['user_id']
            user_id = Token.objects.get(key=tokena).user_id
            if User.objects.get(id=user_id).is_superuser or User_Type.objects.get(user_id=user_id).user_type == 'superadmin':
                if User.objects.filter(id=user_id_normal).count() > 0:
                    if not User.objects.get(id=user_id_normal).is_active:
                        return JsonResponse({"success":"هذا المستخدم غير مفعل"})
                    else:
                        uu=User.objects.get(id=user_id_normal)
                        uu.is_active=False
                        uu.save()
                        return JsonResponse({"success":"تم الغاء التفعيل بنجاح"})
                else:
                    return JsonResponse({"error":"مستخدم غير موجود"})
            else:
                return JsonResponse({'error': 'ليس لديك صلاحيه'})
        else:
            return JsonResponse({'error': toto.errors})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_change_role(request):
        if   get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)['count'] > 120:
             return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication, SessionAuthentication)
        permission_classes = (IsAuthenticated,)
        toto=chRoleeuserSerializer(data=request.data)
        if toto.is_valid():
            tokena=toto.data['token']
            user_id_normal=toto.data['user_id']
            role=toto.data['role']
            user_id = Token.objects.get(key=tokena).user_id
            if User.objects.get(id=user_id).is_superuser or User_Type.objects.get(user_id=user_id).user_type == 'superadmin':
                if User.objects.filter(id=user_id_normal).count() > 0:
                    if role not  in ['superadmin','admin','hr','employee', 'guardian','student', 'teacher']:
                        return JsonResponse({"error": "نوع المستخدم غير موجود"})
                    if User_Type.objects.get(user_id=user_id_normal).user_type == 'superadmin':
                        return JsonResponse({"success":"لا يمكن تغيير نوع هذا المستخدم "})
                    else:
                        uu=User_Type.objects.get(user_id=user_id_normal)
                        uu.user_type=role
                        uu.save()
                        return JsonResponse({"success":"تم تغيير النوع  بنجاح"})
                else:
                    return JsonResponse({"error":"مستخدم غير موجود"})
            else:
                return JsonResponse({'error': 'ليس لديك صلاحيه'})
        else:
            return JsonResponse({'error': toto.errors})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def view_one_user(request):
        if   get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)['count'] > 120:
            return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication, SessionAuthentication)
        permission_classes = (IsAuthenticated,)
        toto=activateuserSerializer(data=request.data)
        if toto.is_valid():
            tokena=toto.data['token']
            user_id_normal=toto.data['user_id']
            user_id = Token.objects.get(key=tokena).user_id
            user_info=[]
            if User.objects.get(id=user_id).is_superuser or User_Type.objects.get(user_id_id=user_id).user_type == 'superadmin':
                if User.objects.filter(id=user_id_normal).count() > 0:
                    useri=User.objects.get(id=user_id_normal)
                    user_info.append({
                        "username":useri.username,
                        "email":useri.email,
                        "isactive":useri.is_active,
                        "phone" : User_Profile.objects.get(user_id=user_id_normal).phone,
                        "fullname": User_Profile.objects.get(user_id=user_id_normal).fullname,
                        "datejoined":User_Profile.objects.get(user_id=user_id_normal).date_joined,
                        "type":User_Type.objects.get(user_id=user_id_normal).user_type
                    })
                    return JsonResponse({"success": user_info})
                else:
                    return JsonResponse({"error": "مستخدم غير موجود"})
            else:
                    return JsonResponse({'error': 'ليس لديك صلاحيه'})
        else:
                return JsonResponse({'error': toto.errors})



@permission_classes([IsAuthenticated])
@api_view(['POST'])
def view_all_url(request):
        if   get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)['count'] > 120:
            return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication, SessionAuthentication)
        permission_classes = (IsAuthenticated,)
        toto=checkTokenserializer(data=request.data)
        if toto.is_valid():
            tokena=toto.data['token']
            user_id= Token.objects.get(key=tokena).user_id
            if User.objects.get(id=user_id).is_superuser or User_Type.objects.get(user_id=user_id).user_type == 'superadmin':
                return JsonResponse({"success": {"private":list(Private_Url.objects.all().values('id','url')),
                                                 "public":list(Public_Url.objects.all().values('id','url'))}})

            else:
                return JsonResponse({'error': 'ليس لديك صلاحيه'})
        else:
            return JsonResponse({'error':toto.errors})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def assign_url_to_user(request):
        if   get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)['count'] > 120:
            return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication, SessionAuthentication)
        permission_classes = (IsAuthenticated,)
        toto=chRoleeuserSerializer(data=request.data)
        if toto.is_valid():
            tokena=toto.data['token']
            user_id_normal=toto.data['user_id']
            url=toto.data['url']
            user_id= Token.objects.get(key=tokena).user_id


            if User.objects.get(id=user_id).is_superuser or User_Type.objects.get(user_id=user_id).user_type == 'superadmin':
                if User.objects.filter(id=user_id_normal).count() < 1:
                    return JsonResponse({"error": "مستخدم غير موجود"})
                if not url in Private_Url.objects.all().values_list('url', flat=True):
                    return JsonResponse({'error': "الصلاحية غير موجودة "})
                url_id = Private_Url.objects.get(url=url).id
                if User_urls.objects.filter(user_id_id=user_id_normal,url_id=url_id).count()>0:
                    return  JsonResponse({'error': "تمت اضافيه الصلاحيه لهذا المستخدم من قبل"})
                User_urls.objects.create(user_id_id=user_id_normal, url_id=url_id)
                return JsonResponse({"success": "تم اضافة الصلاحية بنجاح"})

            else:
                return JsonResponse({'error': 'ليس لديك صلاحيه'})
        else:
            return JsonResponse({'error':toto.errors})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def delete_url_from_user(request):
        if   get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)['count'] > 120:
            return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication, SessionAuthentication)
        permission_classes = (IsAuthenticated,)
        toto=chRoleeuserSerializer(data=request.data)
        if toto.is_valid():
            tokena=toto.data['token']
            user_id_normal=toto.data['user_id']
            url=toto.data['url']
            user_id= Token.objects.get(key=tokena).user_id
            if User.objects.get(id=user_id).is_superuser or User_Type.objects.get(user_id=user_id).user_type == 'superadmin':
                if User.objects.filter(id=user_id_normal).count() < 1:
                    return JsonResponse({"error": "مستخدم غير موجود"})
                print(list(Private_Url.objects.all().values_list('url', flat=True)))
                if url not  in list(Private_Url.objects.all().values_list('url', flat=True)):
                    return JsonResponse({'error': "الصلاحية غير موجودة "})
                url_id = Private_Url.objects.get(url=url).id
                if User_urls.objects.filter(user_id=user_id_normal, url_id=url_id).count() <1:
                    return JsonResponse({'error': "الصلاحية المحددة للمستخدم غير صحيحة "})
                else:
                    userati=User_urls.objects.get(user_id=user_id_normal, url_id=url_id)
                    userati.delete()

                    return JsonResponse({"success": "تم حذف الصلاحية من المستخدم بنجاح"})

            else:
                return JsonResponse({'error': 'ليس لديك صلاحيه'})
        else:
            return JsonResponse({'error':toto.errors})

@api_view(['POST'])
@permission_classes((AllowAny,))
def logino(request):
    if  get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='5/m', method='POST', increment=True)['count']>5:
        return JsonResponse({"error":"too_many_requests"})
    permission_classes = [AllowAny]

    typooo = ''
    userin = loginSerializer(data=request.data)
    if userin.is_valid():
        # print(request.session['username'])
        # if 'username' in request.session and 'usertype'in request.session:

        #     return Response({"success": "already_logged_in"})

        # if request.session.get('username') and request.session.get('usertype'):

        #     return Response({"success": "already_logged_in"})

        if not User.objects.filter(username=userin.data['username']):
            return Response({'error': 'المستخدم غير موجود'})
        userauth = authenticate(request, username=userin.data['username'], password=userin.data['password'],
                                is_active=True)
        if authenticate(request, username=userin.data['username'], password=userin.data['password'], is_active=True):
            login(request, userauth)
            request.session['username'] = userin.data['username']
            request.session['password'] = userin.data['password']

            # request.session['usertype']='normal_user'
            request.session.modified = True
            new_token = ""
            # userati=User.objects.all()
            idd = 0
            idd = User.objects.get(username=userin.data['username']).id
            uouo = User_Profile.objects.get(user_id=idd)
            image_base64 = ''
            # if userprofile.objects.filter(userp=idd).count() > 0:
            #     if uouo.perm_one:
            #         typooo = "Super_user"
            #     elif uouo.perm_two:
            #         typooo = ""
            #     elif uouo.perm_tri:
            #         typooo = ""
            #     elif uouo.perm_quad:
            #         typooo = ""
            #     elif uouo.perm_pent:
            #         typooo = ""
            #     elif uouo.perm_hex:
            #         typooo = "normal_user"
            #     else:
            #         return JsonResponse({"error": "user_have_no_permmision"})
            if Token.objects.filter(user_id=idd).count() > 0:
                mediaroot=os.path.abspath(settings.MEDIA_ROOT)
                print(uouo.userimg)
                with open(mediaroot +'/' + str(uouo.userimg), "rb") as image_file:
                # with open("media/" + str(uouo.userimg), "rb") as image_file:

                    image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
                    print(image_base64)

                token = ""
                tokena = Token.objects.all()
                new_token = tokena.get(user_id=idd).key
                print("old token", new_token)
            else:
                new_token = Token.objects.create(user=User.objects.get(username=request.session['username']))
                print("new token", new_token)
                media_root=os.path.abspath(settings.MEDIA_ROOT)
                with open(media_root +'/'+ str(uouo.userimg), "rb") as image_file:
                # with open("media/" + str(uouo.userimg), "rb") as image_file:

                    image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

            return Response({"success":"تم تسجيل الدخول بنجاح","user_data": {"username": request.session['username'],
                                                                                     "permission": typooo,
                             "token": str(new_token),
                             "user_img": image_base64,
                             "user_type": User_Type.objects.get(user_id=idd).user_type,
                             "user_id": idd, }
                             # "user_permission":userprofile.objects.get(userp=idd).perm_m
                             })
            # HttpResponseRedirect('/dashboard')
            # return redirect('/')

        elif User.objects.filter(username=userin.data['username'], is_active=False):
            return Response({"error": "المستخدم غير نشط"})
        else:

            return Response({'error': 'خطأفى كلمة المرور او اسم المستخدم'})
            # return JsonResponse({'success':'true'})
    else:
        return Response({'error': 'خطأفى كلمة المرور او اسم المستخدم'})
@api_view(['GET'])
@permission_classes([AllowAny])
def login_front(request):
    return redirect('/login')
@api_view(['POST'])
@permission_classes((AllowAny,))
def available_roles(request):
    if  get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='5/m', method='POST', increment=True)['count']>5:
        return JsonResponse({"error":"too_many_requests"})
    permission_classes = [AllowAny]
    return JsonResponse({'success':['superadmin','admin','hr','employee', 'guardian','student', 'teacher']})


@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def add_url(request):
        if   get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)['count'] > 120:
            return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication, SessionAuthentication)
        permission_classes = (IsAuthenticated,)
        toto=addurlSerializer(data=request.data)
        if toto.is_valid():
            tokena=toto.data['token']
            print(tokena,'fff')
            url=toto.data['url']
            url_type=toto.data['url_type']
            user_id= Token.objects.get(key=tokena).user_id
            if User.objects.get(id=user_id).is_superuser or User_Type.objects.get(user_id=user_id).user_type == 'superadmin':
               if Private_Url.objects.filter(url=url).count()>0 or Public_Url.objects.filter(url=url).count()>0:
                   return  JsonResponse({"error":'رابط الصلاحية مضاف من قبل'})
               if url_type not in ['public','private']:
                   return JsonResponse({"error":"نوع رابط الصلاحية غير صحيح"})
               if url_type == 'private':
                    Private_Url.objects.create(url=url)
                    return JsonResponse({"success": 'تمت الاضافة بنجاح'})
               if url_type == 'public':
                    Public_Url.objects.create(url=url)
                    return JsonResponse({"success": 'تمت الاضافة بنجاح'})
            else:
                return JsonResponse({'error': 'ليس لديك صلاحيه'})
        else:
            return JsonResponse({'error':toto.errors})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def update_url_type(request):
        if   get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)['count'] > 120:
            return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication, SessionAuthentication)
        permission_classes = (IsAuthenticated,)
        toto=addurlSerializer(data=request.data)
        if toto.is_valid():
            tokena=toto.data['token']
            url_type=toto.data['url_type']
            url=toto.data['url']
            user_id= Token.objects.get(key=tokena).user_id
            if User.objects.get(id=user_id).is_superuser or User_Type.objects.get(user_id=user_id).user_type == 'superadmin':
               # if url is None:
               #     return JsonResponse({"error": "اضف رابط صحيح"})
               if Private_Url.objects.filter(url=url).count() < 1 and Public_Url.objects.filter(url=url).count() < 1 :
                   return  JsonResponse({"error":'رابط الصلاحية غير موجود من قبل'})
               if url_type not in ['public','private']:
                   return JsonResponse({"error":"نوع رابط الصلاحية غير صحيح"})
               if url_type == 'private':
                    if Public_Url.objects.filter(url=url).count()>0:
                        Private_Url.objects.create(url=url)
                        uouo=Public_Url.objects.get(url=url)
                        uouo.delete()
                        return JsonResponse({"success": "تم تعديل نوع الصلاحية بنجاح"})

                    else:
                        return JsonResponse({"success" :"لا بيانات جديدة للتعديل"})


               if url_type == 'public':
                   if Private_Url.objects.filter(url=url).count() > 0:

                       Public_Url.objects.create(url=url)
                       uouo = Private_Url.objects.get(url=url)
                       uouo.delete()
                       return JsonResponse({"success": "تم تعديل نوع الصلاحية بنجاح"})
                   else:
                       return JsonResponse({"success": "لا بيانات جديدة للتعديل"})
            else:
                return JsonResponse({'error': 'ليس لديك صلاحيه'})
        else:
            return JsonResponse({'error':toto.errors})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def update_url_name(request):
        if   get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)['count'] > 120:
            return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication, SessionAuthentication)
        permission_classes = (IsAuthenticated,)
        toto=addurlSerializer(data=request.data)
        if toto.is_valid():
            tokena=toto.data['token']
            url_type=toto.data['url_type']
            url=toto.data['url']
            url_id=toto.data['url_id']
            user_id= Token.objects.get(key=tokena).user_id
            if User.objects.get(id=user_id).is_superuser or User_Type.objects.get(user_id=user_id).user_type == 'superadmin':
               # if url is None:
               #     return JsonResponse({"error": "اضف رابط صحيح"})

               if url_type not in ['public','private']:
                   return JsonResponse({"error":"نوع رابط الصلاحية غير صحيح"})
               if url_type=='private':
                   if Private_Url.objects.filter(id=url_id).count() < 1 :

                    return  JsonResponse({"error":'رابط الصلاحية غير موجود من قبل'})
               if url_type == 'public':
                   if Public_Url.objects.filter(id=url_id).count() < 1:
                        return JsonResponse({"error": 'رابط الصلاحية غير موجود من قبل'})
               if Public_Url.objects.filter(id=url_id).count()>0:
                   old_name_pl = Public_Url.objects.get(id=url_id).url

                   if old_name_pl == url:
                       return JsonResponse({"success":"لا يوجد  شيء للتعديل"})
                   if Public_Url.objects.filter(url=url).exclude(url=old_name_pl).count()>0:
                       return JsonResponse({"error":"اسم الصلاحية موجود من قبل"})

                   uouo=Public_Url.objects.get(id=url_id)
                   uouo.url=url
                   uouo.save()
                   return JsonResponse({"success": 'تم التعديل بنجاح'})


               if Private_Url.objects.filter(id=url_id).count() > 0:
                    old_name_pv = Private_Url.objects.get(id=url_id).url
                    if old_name_pv == url:
                        return JsonResponse({"success": "لا يوجد  شيء للتعديل"})
                    if Private_Url.objects.filter(url=url).exclude(url=old_name_pv).count() > 0:
                        return JsonResponse({"error": "اسم الصلاحية موجود من قبل"})
                    uouo = Private_Url.objects.get(id=url_id)
                    uouo.url = url
                    uouo.save()
                    return JsonResponse({"success": 'تم التعديل بنجاح'})
            else:
                return JsonResponse({"success": 'ليس لديك صلاحية'})

        else:
            return JsonResponse({'error':toto.errors})



@permission_classes([IsAuthenticated])
@api_view(['POST'])
def delete_url(request):
        if   get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)['count'] > 120:
            return JsonResponse({"error": "too_many_requests"})
        authentication_classes = (TokenAuthentication, SessionAuthentication)
        permission_classes = (IsAuthenticated,)
        toto=addurlSerializer(data=request.data)
        if toto.is_valid():
            tokena=toto.data['token']
            url_type=toto.data['url_type']
            url=toto.data['url']
            url_id=0
            user_id= Token.objects.get(key=tokena).user_id
            if User.objects.get(id=user_id).is_superuser or User_Type.objects.get(user_id=user_id).user_type == 'superadmin':
               # if url is None:
               #     return JsonResponse({"error": "اضف رابط صحيح"})
               if Private_Url.objects.filter(url=url).count() < 1 and Public_Url.objects.filter(url=url).count() < 1 :
                   return  JsonResponse({"error":'رابط الصلاحية غير موجود من قبل'})
               if url_type not in ['public','private']:
                   return JsonResponse({"error":"نوع رابط الصلاحية غير صحيح"})
               if Private_Url.objects.filter(url=url).count() >0:
                   url_id=Private_Url.objects.get(url=url).id
               if Public_Url.objects.filter(url=url).count() >0:
                   url_id = Public_Url.objects.get(url=url).id

               if User_urls.objects.filter(url_id=url_id).count()>0:
                   return JsonResponse({"error":'لايمكن حذف رابط الصلاحية لارتباطه بمستخدم او اكثر'})
               else:
                   if Private_Url.objects.filter(url=url).count() >0:
                       p_u=Private_Url.objects.get(url=url)
                       p_u.delete()
                       return JsonResponse({"success": 'تم الحذف بنجاح'})
                   if Public_Url.objects.filter(url=url).count() >0:
                       p_u = Public_Url.objects.get(url=url)
                       p_u.delete()
                       return JsonResponse({"success": 'تم الحذف بنجاح'})
            else:
                return JsonResponse({'error': 'ليس لديك صلاحيه'})
        else:
            return JsonResponse({'error':toto.errors})


@api_view(['POST'])
@permission_classes((AllowAny,))
def hey_app(request):
    if  get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='5/m', method='POST', increment=True)['count']>5:
        return JsonResponse({"error":"too_many_requests"})
    permission_classes = [AllowAny]
    return JsonResponse({"success": "OK"})


@api_view(['POST'])
@permission_classes([AllowAny, ])
def user_check(request):
    permission_classes = ([AllowAny])
    if \
    get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)[
        'count'] > 120:
        return JsonResponse({"error": "too_many_requests"})
    tok = usercheckSerializer(data=request.data)
    if tok.is_valid():
        userinfo = User.objects.all()
        userprof = userprofile.objects.all()
        tok1 = tok.data['token']
        userid = 0
        if Token.objects.filter(key=tok1).count() > 0:
            userid = Token.objects.get(key=tok1).user_id
            if 'username' in request.session or 'typeoo' in request.session:
                # if not request.path.startswith(settings.MEDIA_URL):
                if not userinfo.get(id=userid).username == request.session.get('username'):
                    return JsonResponse({"error": "user_is_not_logged_in"})

            if userinfo.filter(id=userid).count() > 0:
                if userinfo.get(id=userid).is_active == True:
                    p_one = userprof.get(userp=userid).perm_one
                    p_two = userprof.get(userp=userid).perm_two
                    p_three = userprof.get(userp=userid).perm_tri
                    p_four = userprof.get(userp=userid).perm_quad
                    p_five = userprof.get(userp=userid).perm_pent
                    p_six = userprof.get(userp=userid).perm_hex
                    if p_one == False and p_two == False and p_three == False and p_four == False and p_five == False and p_six == False:
                        return JsonResponse({"error": "user_have_no_permission"})
                    else:
                        if p_one == True:
                            return JsonResponse({"type": "super_admin",
                                                 "name": userprof.get(userp=userid).fullname})
                        if p_two == True:
                            return JsonResponse({"type": "admin",
                                                 "name": userprof.get(userp=userid).fullname})
                        if p_three == True:
                            return JsonResponse({"success": "",
                                                 "name": userprof.get(userp=userid).fullname})
                        if p_four == True:
                            return JsonResponse({"success": "",
                                                 "name": userprof.get(userp=userid).fullname})
                        if p_five == True:
                            return JsonResponse({"success": "",
                                                 "name": userprof.get(userp=userid).fullname})
                        if p_six == True:
                            return JsonResponse({"type": "normal_user", "name": userprof.get(userp=userid).fullname})
                else:
                    return JsonResponse({"error": "user_is_not_active"})


            else:
                return JsonResponse({"error": "user_is_not_exists"})

        else:
            return JsonResponse({"error": "user_is_not_logged_in"})

        # if 'username' in request.session or 'typeoo' in request.session:
        # # if not request.path.startswith(settings.MEDIA_URL):
        #     userati=request.session.get('username')
        #     usertype=request.session.get('typeoo')
        #     userid=request.session.get('userid')
        #     print(userid)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def user_check_mobile(request):
    permission_classes = ([AllowAny])
    if get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST', increment=True)[
        'count'] > 120:
        return JsonResponse({"error": "too_many_requests"})
    tok = checkTokenserializer(data=request.data)
    if tok.is_valid():
        # userinfo = User.objects.all()
        tok1 = tok.data['token']
        print(tok1)
        userid = 0
        if Token.objects.filter(key=tok1).count() > 0:
            userid = Token.objects.get(key=tok1).user_id
            userprof = User_Profile.objects.get(user_id=userid)
            if 'token' not in request.session:
                request.session['token'] =tok1
            return JsonResponse({"success":{"fullname":userprof.fullname,"usertype":User_Type.objects.get(user_id=userid).user_type}})
        else:
            print("user_is_not_logged_in")
            return JsonResponse({"error": "user_is_not_logged_in"})
    else:
        print(tok.errors)
        return  JsonResponse({"error":tok.errors})


        # if 'username' in request.session or 'typeoo' in request.session:
        # # if not request.path.startswith(settings.MEDIA_URL):
        #     userati=request.session.get('username')
        #     usertype=request.session.get('typeoo')
        #     userid=request.session.get('userid')
        #     print(userid)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def hey_app(request):
    permission_classes = ([AllowAny])
    if get_usage(request, group='ratelimit_view', fn=None, key='user_or_ip', rate='120/m', method='POST',
                      increment=True)[
                'count'] > 120:
        return JsonResponse({"error": "too_many_requests"})
    return JsonResponse({'success':'OK'})

def sendmailo(request):
    try:

        send_mail('Fund Time Account Activation', 'activate_url', 'manfaa@infinitybridge.org', ['manfaa@infinitybridge.org'],
              fail_silently=False)

        return JsonResponse({'success':"ok"})

    except Exception as e:
        return JsonResponse({'error':str(e)})

@csrf_exempt
def chkadmin(request):
    if 'token' in request.session:
        token = request.session['token']
        print('chkadmin token',token)
        if Token.objects.filter(key=token).count() > 0:
            idd = Token.objects.get(key=token).user_id
            if User_Type.objects.get(user_id_id=idd).user_type != "superadmin":
                return redirect('https://manf3a.infinitybridge.org/')
            else:
                return JsonResponse({'success':{'token':token}})
        else:
            print("You are not allowed to")
            return JsonResponse({'error':"Invalid"})
            # return redirect('https://manf3a.infinitybridge.org/')
        pass
    else:
        return JsonResponse({'error': "Invalid"})

        # return redirect('https://manf3a.infinitybridge.org/')


@csrf_exempt
def logoutadmin(request):

    if 'token' in request.session:
        token = request.session['token']
        del request.session['token']
        request.session.modified=True
        return JsonResponse({'success': "logged out"})
        # return redirect('https://manf3a.infinitybridge.org/')
    else:
        return JsonResponse({'success': "logged out"})
        # return redirect('https://manf3a.infinitybridge.org/')
        
        
        
        


@permission_classes([IsAuthenticated])
@api_view(['POST'])
@csrf_exempt
def view_role_urls(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    toto = RoleUrlSerializer(data=request.data)
    if toto.is_valid():
        token = toto.data['token']
        # url_id=toto.data['url_id']
        role=toto.data['role']
        if role not in ['superadmin','admin','hr','employee', 'guardian','student', 'teacher']:
            return JsonResponse({"error":"role is not exists"})
        if not User_Type.objects.get(user_id=Token.objects.get(key=token).user_id).user_type=="superadmin":
            return  JsonResponse({"error":"you don't have permissions '"})
        url_ids=list(Types_Urls.objects.filter(type=role).values_list("url_id",flat=True))
        return JsonResponse({"success":list(Private_Url.objects.filter(id__in=url_ids).values_list("url",flat=True))})
    else:
        return JsonResponse({"error": toto.errors})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
@csrf_exempt
def add_url_to_role(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    toto = RoleUrlSerializer(data=request.data)
    if toto.is_valid():
        token = toto.data['token']
        url=toto.data['url']
        role=toto.data['role']
        print("Role",role)
        if role not in [ 'superadmin','admin','hr','employee', 'guardian','student', 'teacher']:
            return JsonResponse({"error":"role is not exists"})
        if not User_Type.objects.get(user_id=Token.objects.get(key=token).user_id).user_type=="superadmin":
            return  JsonResponse({"error":"you don't have permissions '"})
        if Private_Url.objects.filter(url=url).count()<1:
            return JsonResponse({"error":"url is not valid"})
        url_id=Private_Url.objects.get(url=url).id
        if Types_Urls.objects.filter(url_id=url_id,type=role).count()>0:
            return JsonResponse({"error":"url is exist before"})
        else:
            Types_Urls.objects.create(url_id=url_id,type=role)
            return JsonResponse({"success":"url added successfully"})
    else:
        return JsonResponse({"error":toto.errors})

@permission_classes([IsAuthenticated])
@api_view(['POST'])
@csrf_exempt
def delete_url_from_role(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    toto = RoleUrlSerializer(data=request.data)
    if toto.is_valid():
        token = toto.data['token']
        url=toto.data['url']
        role=toto.data['role']
        if role not in ['superadmin','admin','hr','employee', 'guardian','student', 'teacher']:
            return JsonResponse({"error":"role is not exists"})
        if not User_Type.objects.get(user_id=Token.objects.get(key=token).user_id).user_type=="superadmin":
            return  JsonResponse({"error":"you don't have permissions '"})
        if Private_Url.objects.filter(url=url).count()<1:
            return JsonResponse({"error":"url is not valid"})
        url_id=Private_Url.objects.get(url=url).id
        if Types_Urls.objects.filter(url_id=url_id,type=role).count()<1:
            return JsonResponse({"error":"url is not exist for selected role "})
        else:
           dodo=Types_Urls.objects.filter(url_id=url_id,type=role)
           dodo.delete()
        return JsonResponse({"success":"url deleted successfully"})
    else:
        return JsonResponse({"error":toto.errors})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
@csrf_exempt
def apply_role_to_user(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    toto = RoleUrlSerializer(data=request.data)
    if toto.is_valid():
        token = toto.data['token']
        # url=toto.data['url']
        role=toto.data['role']
        user_id = toto.data['user_id']
        if role not in [ 'superadmin','admin','hr','employee', 'guardian','student', 'teacher']:
            return JsonResponse({"error":"role is not exists"})
        if not User_Type.objects.get(user_id=Token.objects.get(key=token).user_id).user_type=="superadmin":
            return  JsonResponse({"error":"you don't have permissions '"})
        if User.objects.filter(id=user_id).count()<1:
            return JsonResponse({"error":"user does not exist"})
        if User_Type.objects.filter(user_id=user_id,user_type=role).count()<1:
            return  JsonResponse({"error":"the role for this user is not valid"})
        url_ids=list(Types_Urls.objects.filter(type=role).values_list('url_id',flat=True))
        if User_urls.objects.filter(user_id_id=user_id).count()>0:
            user_url=User_urls.objects.filter(user_id_id=user_id)
            user_url.delete()
        for url in url_ids:
            User_urls.objects.create(user_id_id=user_id,url_id=url)
        return JsonResponse({"success":"Role Urls Applied successfully"})
    else:
        return JsonResponse({"error":toto.errors})

@permission_classes([IsAuthenticated])
@api_view(['POST'])
@csrf_exempt
def apply_role_to_all_user(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    toto = RoleUrlSerializer(data=request.data)
    if toto.is_valid():
        token = toto.data['token']
        # url=toto.data['url']
        role=toto.data['role']
        # user_id = toto.data['user_id']
        if role not in [ 'superadmin','admin','hr','employee', 'guardian','student', 'teacher']:
            return JsonResponse({"error":"role is not exists"})
        if not User_Type.objects.get(user_id=Token.objects.get(key=token).user_id).user_type=="superadmin":
            return  JsonResponse({"error":"you don't have permissions '"})
        user_ids=list(User_Type.objects.filter(user_type=role).values_list("user_id_id", flat=True))
        url_ids=list(Types_Urls.objects.filter(type=role).values_list('url_id',flat=True))

        for useridd in user_ids:

            if User_urls.objects.filter(user_id_id=useridd).count()>0:
                user_url=User_urls.objects.filter(user_id_id=useridd)
                user_url.delete()
        for useridd in user_ids:
            for url in url_ids:
                User_urls.objects.create(user_id_id=useridd,url_id=url)
        return JsonResponse({"success":"Role Urls Applied successfully"})

    else:
        return JsonResponse({"error":toto.errors})

