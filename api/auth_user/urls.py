from django.urls import path
from . import views

app_name = 'user' # used for test with reverse

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me')
]
