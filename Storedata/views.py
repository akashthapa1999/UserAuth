from django.shortcuts import render, redirect

# from django.contrib.auth.forms import UserCreationForm
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
from .form import ResetPasswordForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin,View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, "HomeScreen.html")


class CreateUserView(View):
    def get(self, request):
        form = CustomUserCreationForm(initial={
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        })
        return render(request, "CreateUserScreen.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['username'].initial = ''
        context['form'].fields['password'].initial = ''
        return context


class ForgotPasswordView(View):
    def get(self, request):
        form = ForgetPassword()
        return render(
            request, "ForgotPasswordScreen/ForgotPasswordForm.html", {"form": form}
        )

    def post(self, request):
        form = ForgetPassword(request.POST)
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if user.is_active:
                print("Inside a if condition")
                self.send_password_reset_email(request, user)
                print("Inside a if condition15")
                messages.success(request, "Password reset email has been sent.")
                return redirect("ForgotPassword")
            else:
                print("Inside a Else condition")
                messages.warning(request, "Your email address is not verified.")
        else:
            messages.error(request, "Account with this email does not exist.")

        return render(request, "ForgotPasswordScreen/ForgotPassword.html", {"form": form})

    def send_password_reset_email(self, request, User):
        current_site = get_current_site(request)

        mail_subject = "Reset your password | C3D"

        message = render_to_string(
            "ForgotPasswordScreen/ResetpasswordEmail.html",
            {
                "user": User,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(User.pk)),
                "token": default_token_generator.make_token(User),
            },
        )
        print("Inside a if condition5789", message)

        to_email = User.email

        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()


class ResetPasswordValidateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = int(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "This link is invalid.")
            return redirect("Login")

        if default_token_generator.check_token(user, token):
            request.session["uid"] = uid
            messages.success(request, "Please reset your password.")
            return redirect("reset_password_confirm", uidb64=uidb64, token=token)
        else:
            messages.error(request, "This link is expired.")
            return redirect("Login")


class ResetPasswordView(View, LoginRequiredMixin):
    login_url = '/Login/'
    def get(self, request, uidb64, token):
        try:
            uid = int(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "This link is invalid.")
            return redirect("Login")

        if default_token_generator.check_token(user, token):
            form = ResetPasswordForm()
            return render(request, "ForgotPasswordScreen/SetResetPassword.html", {"form": form, "uidb64": uidb64, "token": token})
        else:
            messages.error(request, "This link is expired.")
            return redirect("Login")

    def post(self, request, uidb64, token):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["new_password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if password == confirm_password:
                try:
                    uid = int(urlsafe_base64_decode(uidb64))
                    user = User.objects.get(pk=uid)
                    if default_token_generator.check_token(user, token):
                        user.set_password(password)
                        user.save()
                        messages.success(request, "Password reset successful.")
                        return redirect("PasswordResetDone")
                except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                    pass
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, "ForgotPasswordScreen/SetResetPassword.html", {"form": form, "uidb64": uidb64, "token": token})

class ResetPasswordDoneView(View):
    def get(self, request):
        messages.success(request, "Your password has been successfully reset. You can now log in.")
        return render(request, "ForgotPasswordScreen/PasswordResetDone.html")

class UserLogoutView(LogoutView):
    next_page = "Login"
