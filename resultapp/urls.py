from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # or home if you use that name
]