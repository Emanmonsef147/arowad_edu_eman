from rest_framework.authtoken.models import Token
from .urls import url_list
from general_settings.urls import general_url_list
from academic.urls import academic_url_list
from django.http import JsonResponse, HttpResponseNotFound
from .models import Public_Url, Private_Url, User, User_Type  # Adjust the import path as needed

class DefenseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        encrypted_data2 = (request.path)
        # if ('login' in str(encrypted_data2)):
        #     return HttpResponseNotFound('Authentication')
        print("path", encrypted_data2)
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        print("auth_header", auth_header)

        pub_url = set(Public_Url.objects.all().values_list('url', flat=True))
        # print(list(pub_url))
        encrypted_data2 = str(encrypted_data2)
        if encrypted_data2 != "/" and encrypted_data2.startswith("/"):

            encrypted_data2 = encrypted_data2[1:]
            print("encrypted_data2", encrypted_data2)
        else:
            print("encrypted_data2", encrypted_data2)

        urls = [url_list, general_url_list, academic_url_list]
        all_urls = [url for url_group in urls for url in url_group]

        if encrypted_data2 in all_urls:
            print("back_url", encrypted_data2)
        else:
            if encrypted_data2 not in list(pub_url) and not any(var in encrypted_data2 for var in ['.svg', '.ico', '.jpg','.png' ,'.js','.css','.jsx','.woff2','.woff']):
                # print("encrypted_data")
                if Token.objects.filter(key=auth_header).count() < 1:
                    return HttpResponseNotFound(auth_header)
                user_id = Token.objects.get(key=auth_header).user_id
                if not User.objects.get(id=user_id).is_superuser or User_Type.objects.get(id=user_id).user_type != "superadmin":

                    if Token.objects.filter(key=auth_header).count() < 1:

                        return HttpResponseNotFound()

                    if Private_Url.objects.filter(user=user_id, url=auth_header).count() < 1:
                        return JsonResponse({"error" : "ليس لديك صلاحية " })

            # else:
            #     pass
        response = self.get_response(request)
        return response


# class DefenseMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         try:
#             # ... (existing code)
#             response = self.get_response(request)
#         except Exception as e:
#             print("Exception in DefenseMiddleware:", str(e))
#             raise
#
#         return response


