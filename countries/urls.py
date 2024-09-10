from django.urls import path
from . import views
urlpatterns = [
    #urls Year
    path('view-all-countries/',views.view_countries),
path('view-all-states',views.view_states),
path('view-all-cities',views.view_cities),
path('view-all-langs/',views.view_langs),
path('view-all-religions/',views.view_religion)]