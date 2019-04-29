from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.db.models.fields.files import ImageFieldFile, FileField

from django.http import HttpResponse

from accounts.forms import LoginForm, RegistrationForm, UserEditForm, ProfileEditForm
from accounts.models import Profile

class LoginView(View): # см. urls.py - если auth_view.LoginView - не этот обработчик
	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(
				request,
				username=cd['username'],
				password=cd['password']
			)
			if user is None:
				return HttpResponse('Неправильный логин и/или пароль')

			if not user.is_active:
				return HttpResponse('Ваш аккаунт заблокирован')

			login(request, user)
			
			return HttpResponse('Добро пожаловать! Успешный вход')

		return render(request, 'accounts/login.html', {'form': form})

	def get(self, request, *args, **kwargs):
		form = LoginForm()
		return render(request, 'accounts/login.html', {'form': form})

def register(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			new_user = form.save(commit=False)
			new_user.set_password(form.cleaned_data["password"])
			new_user.save()
			if settings.AVATAR_SITE:
				Profile.objects.create(user = new_user, avatar = ImageFieldFile(instance=None, field=FileField(), name='user_avatars/default.png'))
			else:
				Profile.objects.create(user = new_user, field=FileField(), name='user_avatars/default.png')

# from django.contrib.auth.models import User
# from django.db.models.fields.files import ImageFieldFile, FileField
# from accounts.forms import Profile

# u = User.objects.get(username = "gogol")
# p = Profile.objects.get(user = u)
# p.avatar = ImageFieldFile(instance=None, field=FileField(), name='user_avatars/default.png')

			return render(request, "accounts/registration_complete.html",
						  {"new_user": new_user})
	else:
		form = RegistrationForm()

	return render(request, "accounts/register.html", {"user_form": form})

@login_required
def edit(request):
    # send_mail("Привет от django", f"Пользователь changes his profile", settings.EMAIL_HOST_USER, ["usikovone@gmail.com"], fail_silently=False)
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse("tasks:list"))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        "accounts/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )