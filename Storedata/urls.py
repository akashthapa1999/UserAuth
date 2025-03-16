from django.urls import path
from .views import HomeView, CreateUserView,ResetPasswordDoneView, LoginUserView, ResetPasswordValidateView, ForgotPasswordView, ResetPasswordView,  UserLogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='Home'),
    path('CreateUser/', CreateUserView.as_view(), name='CreateUser'),
    path('Login/', LoginUserView.as_view(), name='Login'),
    path('Logout/', UserLogoutView.as_view(), name='Logout'),

    path('ForgotPassword/', ForgotPasswordView.as_view(), name='ForgotPassword'),
    path("reset-password/<uidb64>/<token>/", ResetPasswordValidateView.as_view(), name="reset_password_validate"),
    path('reset-password/confirm/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password_confirm'),
    path("reset/done", ResetPasswordDoneView.as_view(), name="PasswordResetDone"),

]
