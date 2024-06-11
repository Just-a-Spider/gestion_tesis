from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path

urlpatterns = [
    # Registration Related
    path('register/', RegisterView.as_view(), name='register'), # For registration

    # Login Related
    path('login/', LoginView.as_view(), name='login'), # For login
    path('logout/', LogoutView.as_view(), name='logout'), # For logout

    # User Related
    path('user/', UserDetailsView.as_view(), name='user'), # For user details
]
