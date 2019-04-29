from django.contrib.auth.models import User
from django import forms
from accounts.models import Profile

from django.conf import settings

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
	password2 = forms.CharField(
		label='Повторите пароль', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ("username", "first_name", "email")

	def clean_password2(self):
		cd = self.cleaned_data
		if cd["password"] != cd["password2"]:
			raise forms.ValidationError("Пароли не совпадают")
		return cd["password2"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("birthdate", "avatar") if settings.AVATAR_SITE else ("birthdate", )