from django.urls import path, reverse_lazy, include
from django.contrib.auth import views as auth_views
import users.views as views
from users.forms import LoginForm
app_name = 'users'

#https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html

urlpatterns = [
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('identifier_validation/', views.ValidateIdentififer.as_view(), name='validate_identifier'),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html', authentication_form = LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/',views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
