from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/post/', views.job_post, name='job_post'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('messages/', views.inbox, name='inbox'),
    path('messages/new/<int:user_id>/', views.compose_message, name='compose_message'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/alumni/', views.register_alumni, name='register_alumni'),
    path('alumni/', views.alumni_list, name='alumni_list'),
    path('alumni/profile/<int:pk>/', views.alumni_profile, name='alumni_profile'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
]
