from django.shortcuts import redirect
from usermgr.models import *
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from django.http import HttpResponseNotFound

class DefenseSuperAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        encrypted_data2 = (request.path)
        # if ('login' in str(encrypted_data2)):
        #     return HttpResponseNotFound('Authentication')
        print("path",encrypted_data2)
        # auth_header = request.META.get('HTTP_AUTHORIZATION')
        # print("auth_header",auth_header)

        # pub_url = Public_Url.objects.all().values_list('url', flat=True)
        # print(list(pub_url))
        encrypted_data2=str(encrypted_data2)
        if encrypted_data2!="/":

            if 'token' in request.session:
                token = request.session['token']

                if Token.objects.filter(key=token).count() > 0:
                    print("token")
                    idd = Token.objects.get(key=token).user_id
                    if User_Type.objects.get(user_id_id=idd).user_type != "superadmin":
                        #####seee the latest chatgpt  response to https
                        # request.session['token'] = token
                        # return HttpResponseRedirect(reverse('publicurls'))
                        return redirect('http://localhost:5177')
                    else:
                        if encrypted_data2=="/home":
                            pass

                        # return redirect('/home')

                        # return render(request, 'home.html', {'token': token})
                    # else:
                    ### save to session and redirect to /
                    ####   in / check the session and keep or redirect to main page
                else:
                    # return redirect('/publicurls')
                    return redirect('http://localhost:5177')
        else:
            pass
        response = self.get_response(request)
        return response




## org manfa3a
# class DefenseMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         encrypted_data2 = (request.path)
#         # if ('login' in str(encrypted_data2)):
#         #     return HttpResponseNotFound('Authentication')
#         # print("path",encrypted_data2)
#         auth_header = request.META.get('HTTP_AUTHORIZATION')
#         # print("auth_header",auth_header)
#
#         pub_url = Public_Url.objects.all().values_list('url', flat=True)
#         # print(list(pub_url))
#         encrypted_data2=str(encrypted_data2)
#         if encrypted_data2!="/" and encrypted_data2.startswith("/"):
#
#             encrypted_data2 = encrypted_data2[1:]
#         else:
#             pass
#         print("encrypted_data2",encrypted_data2)
#         if encrypted_data2 not in list(pub_url) and not any(var in encrypted_data2 for var in ['.ico','.jpg' ,'.png','.js','.css','.jsx']):
#             # print("encrypted_data")
#             if Token.objects.filter(key=auth_header).count()<1:
#                 return HttpResponseNotFound()
#             user_id = Token.objects.get(key=auth_header).user_id
#             if not User.objects.get(id=user_id).is_superuser or  User_Type.objects.get(id=user_id).user_type !="superadmin":
#
#                 if Token.objects.filter(key=auth_header).count() < 1 :
#                     return HttpResponseNotFound()
#                 if Private_Url.objects.filter(user=user_id,url=auth_header).count()<1:
#                     return  JsonResponse({"error":"ليس لديك صلاحية "})
#
#         else:
#             pass
#         response = self.get_response(request)
#         return response
#
#




    # def __call__(self, request):
    #     encrypted_data2 = request.path
    #     print(encrypted_data2)
    #     auth_header = request.META.get('HTTP_AUTHORIZATION')
    #
    #     try:
    #         token = Token.objects.get(key=auth_header)
    #         user_id = token.user_id
    #         pub_urls = Public_Url.objects.values_list('url', flat=True)
    #     except Token.DoesNotExist:
    #         return HttpResponseNotFound()
    #
    #     if encrypted_data2 not in pub_urls or \
    #             not User.objects.filter(id=user_id, is_superuser=True).exists() or \
    #             User_Type.objects.filter(id=user_id, user_type="superadmin").exists():
    #         if not Private_Url.objects.filter(user=user_id, url=auth_header).exists():
    #             return JsonResponse({"error": "ليس لديك صلاحية "})
    #
    #     response = self.get_response(request)
    #     return response