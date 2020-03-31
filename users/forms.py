from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.forms import UserModel   # forms.py assigns: UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    # this looks more like a bug but it is a documented behaviour:
    # UserCreationForm fails if used with custom User model (because it has hard-coded (basic) User)
    # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel
        fields = ('email',)  # 'first_name', 'last_name',
