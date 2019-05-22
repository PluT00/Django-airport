from django.urls import path

from crm import views


urlpatterns = [
    path('', views.flights_list, name="flights_list_url"),
    path('flight/<str:slug>/', views.flight_details, name="flight_details_url"),
]
