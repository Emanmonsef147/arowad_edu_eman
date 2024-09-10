
from django.urls import path
from . import views

app_name = 'general_settings'
urlpatterns = [
    # #urls Year
    # path('add-year/',views.add_year),
    # path('update-year/',views.update_year),
    # # path('delete-year/',views.delete_year),
    # path('view-one-year/', views.view_one_year),
    # path('view-all-years/', views.view_all_years),
    # #urls Academic_Year_Semesters
    # path('add-semster/',views.add_semster),
    # path('update-semster/',views.update_semster),
    # path('view-all-semsters/',views.view_all_semsters),
    # path('view-one-semster/',views.view_one_semster),
    # # urls Academic_Years
    # path('add-acadmic-year/', views.add_acadmic_year),
    # path('view_years_by_semster/',views.view_years_by_semsters),
    # path('update-acdmic-year/', views.update_acadmic_year),
    # path('view-acdmic-years/', views.view_acadmic_years),
    # path('view-acdmic-years-acceptedopen/', views.view_acadmic_years_is_acceptedopen),
    # path('view-one-acdmic-year/<int:id>/', views.view_one_acadmic_year),

    # urls Stages
    path('add-stage/', views.add_stage),
    path('update-stage/', views.update_stage),
    path('delete-stage/', views.delete_stage),
    path('view-one-stage/', views.view_one_stage),
    path('view-all-stages/', views.view_all_satges),
    # urls Grades
    path('add-grade/', views.add_grade),
    path('update-grade/', views.update_grade),
    path('delete-grade/', views.delete_grade),
    path('view-one-grade/', views.view_one_grade),
    path('view-all-grades/', views.view_all_grades),
    path('view-last-grades/',views.view_last_grades),
    # urls Student Intial Class
    path('update-intial-class/',views.update_intial_class),
    path('view-one-intial-class/',views.view_one_intial_class),
    path('view-all-intial-classes/',views.view_all_intial_classes),
    # urls RegisterationGrades
    path('add-reg-grade/', views.add_register_grade),
    path('update-reg-grade/', views.update_reg_grade),
    path('toggle/', views.toggle),
    path('view-one-reg-grade/', views.view_one_reg_grade),
    path('view-all-reggrades/', views.view_all_reg_grades),

    # Urls Programme

    path('add-programme/' ,views.add_programme),
    path('update-programme/',views.update_programme),
    path('view-all-programmes/', views.view_all_programmes),
    path('view-one-programme/',views.view_one_programme),
    # Urls Grade Programme
    path('add-grade-programme/',views.add_grade_programme),
    path('view-grades-by-programme/',views.view_all_grades_by_programme),
    path('view-programmes-by-grade/',views.view_programme_by_grades),


    # Urls National Setting

path('add-update-national-setting/', views.add_national_setting),
    # path('update-national-setting/', views.update_national_setting),
    # # path('delete-national-setting/', views.delete_national_setting),
    path('view-national-setting/', views.view_national_setting),
# Urls Grading Type System
    path('add-gradetype/', views.add_grade_type),
    path('update-gradetype/',views.update_grade_type),
    path('view-one-gradetype/',views.view_one_grade_type),
    path('view-all-grade-types/',views.view_all_grade_types)

    
]
general_url_list = [f'{app_name}/{pattern.pattern}' for pattern in urlpatterns]