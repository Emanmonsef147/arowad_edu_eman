
from django.urls import path
from . import views
app_name = 'student'
urlpatterns = [
# urls Applicant
    path('view-status-by-category/',views.view_status_by_category),
    path('view-reggrades-bylimitage/', views.view_reggrades_bylimitages),
    path('view-academic-years-by-agelimit/',views.view_academic_year_bylimitages),

    #Urls Applicant Document Type
    path('add-applicant-document-type/',views.applicant_document_type_create),
    path('view-all-applicant-document-type/',views.applicant_document_type_view_all),
    path('view-one-applicant-document-type/',views.applicant_document_type_view_one),
    path('update-applicant-document-type/',views.applicant_document_type_update),
    path('delete-applicant-document-type/',views.applicant_document_type_delete),
    #Urls Applicant
    path('add-applicant/', views.create_applicant),
    path('view-all-applicant-by-years/',views.view_applicant_by_year),
    path('view-all-applicant-by-grade/',views.view_applicant_by_grade),
    path('view-applicants-by-status/',views.view_applicants_by_status),
    path('view-applicants-by-filter/',views.view_applicants_by_filter),
    path('view-status-applicant/',views.view_status_applicants),
    path('view-one-applicant/',views.view_one_applicant),
    path('update-applicant/',views.update_applicant),
    path('applicant-login/',views.login_applicant),
    path('applicant-logout/',views.logout_applicant),
]
student_url_list = [f'{app_name}/{pattern.pattern}' for pattern in urlpatterns]