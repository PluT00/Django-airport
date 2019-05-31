from django.urls import path

from crm import views


urlpatterns = [
    path('', views.flights_list, name="flights_list_url"),
    path('flight/<str:slug>/', views.flight_details, name="flight_details_url"),
    path(
        'flight/<str:slug>/ticket/create/',
        views.FlightTicket.as_view(),
        name="flight_ticket_url"
    ),
    path(
        'flight/<str:slug>/ticket/delete/',
        views.FlightTicketDelete.as_view(),
        name="flight_ticket_delete_url"
    ),
    path('mytickets/', views.MyTickets.as_view(), name="my_tickets_url")
]
