from django.urls import path
from . import views

urlpatterns = [
    path("mod/login", views.login_view, name="login"),
    path("mod/register", views.register, name="register"),
    path('logout', views.logout_view, name='logout'),
    path('profile/create', views.create_profile, name='create_profile'),
    path('profile/edit', views.edit_profile, name='edit_profile')
]