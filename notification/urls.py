from django.urls import path
from .views import Device, NotifyUsers, ReportPositiveUser
urlpatterns = [
    path('device/', Device.as_view()),
    path('notify-users/', NotifyUsers.as_view()),
]
