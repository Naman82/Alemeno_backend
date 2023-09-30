from django.urls import path
from . import views

urlpatterns = [
    path('upload/',views.PhotoProcessView.as_view()),   
]