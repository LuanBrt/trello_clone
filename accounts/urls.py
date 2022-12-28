from django.urls import path
from .views import login_view, logout_view, register_view

app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout')
]