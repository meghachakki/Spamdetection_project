from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),  # Landing page
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout view
    path('profile/', views.profile, name='profile'),  # Profile page
    path('sender/<int:sender_id>/', views.user_detail, name='user_detail'),
    path('profile/mark_message_read/', views.mark_message_read, name='mark_message_read'),  # New URL for marking message as read
   
]

