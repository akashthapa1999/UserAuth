from django.urls import path
from .views import HomeView, CreateUserView, LoginUserView, ResetPasswordValidateView, ForgotPasswordView, ResetPasswordView,  UserLogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='Home'),
    path('CreateUser/', CreateUserView.as_view(), name='CreateUser'),
    path('Login/', LoginUserView.as_view(), name='Login'),
    path('Logout/', UserLogoutView.as_view(), name='Logout'),

    path('ForgotPassword/', ForgotPasswordView.as_view(), name='ForgotPassword'),
    path('ResetPassword/', ResetPasswordView.as_view(), name='ResetPassword'),
    path("reset-password/<uidb64>/<token>/", ResetPasswordValidateView.as_view(), name="reset_password_validate"),

]
