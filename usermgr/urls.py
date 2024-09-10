
from django.urls import path
from .views import *
app_name = 'users'
urlpatterns = [
#      path('register_seller', register_seller),
#      path('register_marketer', register_marketer),
#      path('marketer_activation', marketer_activation),
#      path('forget_password', forget_password),
#      path('reset_password', reset_password),
#      path('chk_tok', chk_tok),
#      path('chk_active', chk_active),
#      path('hey_app',hey_app),
#      path('user_check_mobile',user_check_mobile),
#      path('user_check',user_check),
     path('login', logino),
path('front-login/' , login_front , name='login_front'),
     path('logout', logouto),
path('logout', logoutadmin),
path('chkadmin', chkadmin),
     ################################

     path('view_all_users', view_all_users),#
     path('view_one_user', view_one_user),#
     path('activate_one_user', activate_one_user),#
     path('deactivate_one_user', deactivate_one_user),#
     path('user_change_role', user_change_role),#
     path('view_all_url', view_all_url),#
     # path('user_change_role', user_change_role),
     path('available_roles', available_roles),#
     path('assign_url_to_user', assign_url_to_user),#
     path('delete_url_from_user', delete_url_from_user), ## need data
     path('add_url', add_url),#
     path('update_url_type', update_url_type),#
     path('update_url_name', update_url_name),#
     path('delete_url', delete_url),#
     
     
     
     path('view_role_urls', view_role_urls),#
path('add_url_to_role', add_url_to_role),#
path('delete_url_from_role', delete_url_from_role),#
path('apply_role_to_user', apply_role_to_user),#
path('apply_role_to_all_user', apply_role_to_all_user),#
path('sendo_mailo', sendmailo ),

]
url_list = [f'{app_name}/{pattern.pattern}' for pattern in urlpatterns]

