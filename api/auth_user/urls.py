from django.urls import path
from . import views

app_name = 'user' # used for test with reverse

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='create')
]
