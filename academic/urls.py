from django.urls import path
from . import views
app_name = 'academic'
urlpatterns = [
    #urls Year
    path('add-year/',views.add_year),
    path('update-year/',views.update_year),
    # path('delete-year/',views.delete_year),
    path('view-one-year/', views.view_one_year),
    path('view-all-years/', views.view_all_years),
    path('view-all-last-years/',views.view_all_last_years),
    #urls Academic_Year_Semesters
    path('add-semster/',views.add_semster),
    path('update-semster/',views.update_semster),
    path('view-all-semsters/',views.view_all_semsters),
    path('view-one-semster/',views.view_one_semster),
    # urls Academic_Years
    path('add-acadmic-year/', views.add_acadmic_year),
    # path('view_years_by_semster/',views.view_years_by_semsters),
    path('update-acdmic-year/', views.update_acadmic_year),
    path('view-acdmic-years/', views.view_acadmic_years),
    # path('view-acdmic-years-acceptedopen/', views.view_acadmic_years_is_acceptedopen),
    path('view-one-acdmic-year/<int:id>/', views.view_one_acadmic_year)
    ]
academic_url_list = [f'{app_name}/{pattern.pattern}' for pattern in urlpatterns]