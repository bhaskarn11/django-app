from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html',), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('password/reset', PasswordResetView.as_view(template_name='account/password-reset.html'), name ='password_reset'),   
    path('password/reset/init',PasswordResetDoneView.as_view(template_name='account/password-reset-done.html'), name ='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='account/password-reset-confirm.html'), name ='password_reset_confirm'),
    path('password/reset/success', PasswordResetCompleteView.as_view(template_name = 'account/password-reset-complete.html'), name='password_reset_complete'),
]