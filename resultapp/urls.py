from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('notice/<int:notice_id>/', views.notice_detail, name='notice_detail'),
]