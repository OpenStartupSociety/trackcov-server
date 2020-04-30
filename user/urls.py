from django.urls import path
from .views import UserProfile, DailySymptomsTracker, HealthProfile

urlpatterns = [
    path('profile/', UserProfile.as_view()),
    path('daily-symptoms/', DailySymptomsTracker.as_view()),
    path('health-profile/', HealthProfile.as_view())
]
