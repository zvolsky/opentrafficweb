from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.conf.urls import url

from accounts import views as accounts_views


urlpatterns = [
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # send me a username, I am not sure if I use a correct one
    path('get_username/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/pwd/get_username.html',
            email_template_name='accounts/pwd/get_username_email.html',
            subject_template_name='accounts/pwd/get_username_subject.txt',
            success_url = reverse_lazy('accounts:get_username_done')
        ),
        name='get_username'),
    path('get_username/done/',
        accounts_views.CustomPasswordResetDoneView.as_view(template_name='accounts/pwd/get_username_done.html'),
        name='get_username_done'),

    # send me a link with possibility change my password while I am not logged in
    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/pwd/reset.html',
            email_template_name='accounts/pwd/reset_email.html',
            subject_template_name='accounts/pwd/reset_subject.txt',
            success_url = reverse_lazy('accounts:password_reset_done')
        ),
        name='password_reset'),
    path('reset/done/',
        accounts_views.CustomPasswordResetDoneView.as_view(template_name='accounts/pwd/reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/pwd/reset_confirm.html',
            success_url = reverse_lazy('accounts:password_reset_complete')
        ),
        name='password_reset_confirm'),
    path('reset/complete/',
        accounts_views.CustomPasswordResetCompleteView.as_view(template_name='accounts/pwd/reset_complete.html'),
        name='password_reset_complete'),

    # change the password while I am logged
    path('settings/password/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/pwd/change.html',
            success_url = reverse_lazy('accounts:password_change_done')
        ),
        name='password_change'),
    path('settings/password/done/',
        accounts_views.CustomPasswordChangeDoneView.as_view(template_name='accounts/pwd/change_done.html'),
        name='password_change_done'),
]
