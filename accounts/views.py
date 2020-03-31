from django.conf import settings
from django.contrib.auth import login, views as auth_views
from django.shortcuts import redirect, render

from users.forms import CustomUserCreationForm   # TODO: users vs accounts?


class AddHomeUrlMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = settings.HOME_URL
        return context


class CustomPasswordResetDoneView(AddHomeUrlMixin, auth_views.PasswordResetDoneView):
    pass


class CustomPasswordResetCompleteView(AddHomeUrlMixin, auth_views.PasswordResetCompleteView):
    pass


class CustomPasswordChangeDoneView(AddHomeUrlMixin, auth_views.PasswordChangeDoneView):
    pass


def signup(request):    # TODO: accounts vs users (which owns CustomUserCreationForm)?
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
