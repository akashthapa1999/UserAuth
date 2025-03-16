from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



# class ForgotPasswordForm(forms.Form):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Password',
#         'icon_class': 'fa fa-lock',
#     }))
#     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Confirm Password',
#         'icon_class': 'fa fa-lock',
#     }))

#   def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if password and confirm_password and password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")

#         return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ForgetPassword(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address',
        'icon_class': 'fa fa-envelope-o'
        }))


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput, label="New Password", required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password", required=True
    )
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
