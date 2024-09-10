"""alrowad_edu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from usermgr.views import *
from .views import *

urlpatterns = [
# Portal Dashboard Urls
# path('', indexo),
path('login', TemplateView.as_view(template_name='index.html')),
path('publicurls', TemplateView.as_view(template_name='index.html')),
path('privateurls', TemplateView.as_view(template_name='index.html')),
path('viewusers', TemplateView.as_view(template_name='index.html')),
path('viewoneuser/<str:id>', TemplateView.as_view(template_name='index.html')),
path('getoneuser', getoneuser),
path('register', TemplateView.as_view(template_name='index.html')),
path('home', TemplateView.as_view(template_name='index.html')),
path('dashboard', TemplateView.as_view(template_name='index.html')),
path('viewusers', TemplateView.as_view(template_name='index.html')),
path('roles', TemplateView.as_view(template_name='index.html')),

#Apps Urls
path('admin/', admin.site.urls),
path('general_settings/',include("general_settings.urls")),
path('academic/',include("academic.urls")),
path('users/',include("usermgr.urls")),
path('student/',include("student.urls")),
path('countries/',include("countries.urls")),

#Front Urls
re_path(r'^academics(?:/years|/academicyearSemester|/acadmicyears)?/?$',
        TemplateView.as_view(template_name='index.html')),

re_path(r'^Administration(?:/Activity|/AdmissionRegistration|/Agreement|/Archiving|/Behaviour|/BooksUniform|/Clinic|'
        r'/Finance|/HelpDesk|/Hostel|/HumanResource/Inventory|/Procurement|/RoomBooking|/User'
        r'/SMS/StaffTransport|/StudentAffairs|/Surveys|/Transport|/Settings)?/?$',
        TemplateView.as_view(template_name='index.html')),

re_path(r'^Administration/AdmissionRegistration(?:/ApplicantRegistration|/DirectAdmit|/ApplicantRegistrationReport|/ManageApplicantDetails'
    r'|/ApplicantRegistrationSetting|/ApplicantRegistrationSetting/ManageGrades|/ApplicantDocumentVerification|/UpgradeDowngrade|'
        r'/MergeGuardianAccounts|/AdmissionReportDetails|/ChangeApplicantStatus|/AdmissionLogDetails|/ChangeApplicant'
    r'|/AdmissionParentWiseReport|/ManageClassrooms|/StudentsDocumentsreport|/ApplicantForm|/StudentRenewalLetters'
    r'|/RegistrationList|/IfNoGuardian|/NewStudentReport)?/?$',
        TemplateView.as_view(template_name='index.html')),

# Setting Urls
re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
re_path(r'^(?P<path>.*)$', serve, {'document_root': 'build/'}),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

