from django.urls import path

from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from . views import MyTokenObtainPairView


urlpatterns = [

    path('overview/', views.overview),


    path('students/', views.student_list), # list view

    path('student/<str:pk>/', views.student), # detailed view

    path('add/', views.add_student), # create

    path('student/update/<str:pk>/', views.update_student), # update

    path('student/delete/<str:pk>/', views.delete_student),


    path('cbv/students/', views.StudentsView.as_view()),

    path('cbv/student/<str:pk>/', views.StudentDetailView.as_view()),

    path('users/', views.UsersView.as_view()),

    
    path('user/<int:pk>/', views.UserDetail.as_view())



]


urlpatterns += [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


print(f'count of routes {len(urlpatterns)}')