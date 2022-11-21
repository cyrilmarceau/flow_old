from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('api/auth/', include('auth_user.urls')),
]
