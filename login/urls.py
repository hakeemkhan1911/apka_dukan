from django.urls import path
from . import views

app_name='login'

urlpatterns = [
    path('register_user',views.register_user,name='register_user'),
    path('register',views.register,name='register'),
    path('login_user',views.login_user,name='login_user'),
    path('logout_user',views.logout_user,name='logout_user'),
    path('me',views.me,name='me'),
    path('update_user',views.update_user,name='update_user'),
    path('delete_user',views.delete_user,name='delete_user'),
    path('which_user',views.which_user, name='which_user'),
    #For password reset 
    path('password_reset/', views.password_reset, name='password_reset'),
    path('new_password/', views.new_password, name='new_password'),
    path('profile_photo_update/',views.profile_photo_update,name='profile_photo_update'),
    path('user_profile/<int:user_id>',views.user_profile,name='user_profile')
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]
