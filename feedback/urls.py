from django.urls import path

from .views import Feedback
urlpatterns = [
    path('', Feedback.as_view()),

]
