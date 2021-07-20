from django.urls import path
import app.views as views
app_name = 'app'

urlpatterns = [
    path('<identifier>/', views.ProfileView.as_view(), name='profile'),
    path('p/<uuid>/', views.PostDetailView.as_view(), name='post'),
    path("follow/<identifier>/", views.Follow.as_view(), name="follow"),
    path("unfollow/<identifier>/", views.Unfollow.as_view(), name="unfollow"),
]
