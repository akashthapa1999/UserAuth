from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.contrib.auth.views import LoginView, LogoutView
from .form import ForgetPassword
from django.utils.http import urlsafe_base64_decode

from .form import ResetPasswordForm



class HomeView(View):
    def get(self, request):
        return render(request, "HomeScreen.html")


class CreateUserView(View):
    def get(self, request):
        form = UserCreationForm(initial={"username": "","email":"","password1": "", "password2": "" })
        return render(request, "CreateUserScreen.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        import pdb
        pdb.set_trace()
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("Home")
        return render(request, "CreateUserScreen.html", {"form": form})


class LoginUserView(LoginView):
    template_name = "UserLoginScreen.html"

    def form_invalid(self, form):
        form.add_error(None, "Invalid username or password.")
        return self.render_to_response({"form": form})

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect("Home")


class ForgotPasswordView(View):
    def get(self, request):
        form = ForgetPassword()
        return render(request, "ForgotPasswordScreen/ForgotPasswordForm.html",{"form": form})

    def post(self, request):
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.is_active:
                self.send_password_reset_email(request, user)
                messages.success(request, "Password reset email has been sent.")
                return redirect("login")
            else:
                messages.warning(request, "Your email address is not verified.")
        else:
            messages.error(request, "Account with this email does not exist.")
        return redirect("ForgotPassword")

    def send_password_reset_email(self, request, User):
        current_site = get_current_site(request)
        mail_subject = "Reset your password | C3D"
        message = render_to_string(
            "ResetpasswordEmail.html",
            {
                "user": User,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(User.pk)),
                "token": default_token_generator.make_token(User),
            },
        )
        to_email = User.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()


class ResetPasswordValidateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = int(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                request.session["uid"] = uid
                messages.success(request, "Please reset your password.")
                return redirect("reset_password")
            else:
                messages.error(request, "This link is expired.")
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "This link is invalid.")

        return redirect("login")

class ResetPasswordView(View):

    def get(self, request):
        form = ResetPasswordForm()
        return render(request, "reset_password.html",{"form": form})

    def post(self, request):
        password = request.POST.get("New Password")
        confirm_password = request.POST.get("Confirm Password")

        if password == confirm_password:
            uid = request.session.get("uid")
            if uid:
                try:
                    user = User.objects.get(pk=uid)
                    user.set_password(password)
                    user.save()
                    messages.success(request, "Password reset successful.")
                    return redirect("login")
                except User.DoesNotExist:
                    pass

        messages.error(request, "Passwords do not match.")
        return redirect("reset_password")


class UserLogoutView(LogoutView):
    next_page = 'Login'
