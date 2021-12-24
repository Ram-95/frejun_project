from django.urls import path
from . import views

urlpatterns = [
    path('inbound/sms', views.inbound, name="inbound"),
    path('outbound/sms', views.outbound, name="outbound"),
]
