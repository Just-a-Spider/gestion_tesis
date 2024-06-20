from .views import RegisterView, LoginView
from django.urls import path

urlpatterns = [
    # Registration Related
    path('register/', RegisterView.as_view(), name='register'), # For registration

    # Login Related
    path('login/', LoginView.as_view(), name='login'), # For login

]
