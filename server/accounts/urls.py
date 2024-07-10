from .views import *
from django.urls import path

urlpatterns = [
    # Registration Related
    path('register/', RegisterView.as_view(), name='register'),

    # Session Related
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # User Related
    path('me/', MeView.as_view(), name='me')
]
