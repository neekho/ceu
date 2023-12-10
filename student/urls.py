from django.urls import path

from . views import (MyLoginView, MyLogoutView, HomeView)
from . import views

urlpatterns = [

    

    path('home/', HomeView.as_view(), name='home'),

    path('all_students/', views.all_students, name='all-students'),

    path('search_student/<str:pk>/', views.student, name='student'),

    path('login/', MyLoginView.as_view(), name='login'),

    path('logout/', MyLogoutView.as_view(next_page='/login/'), name='logout'),
]