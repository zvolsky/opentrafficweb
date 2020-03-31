from django.urls import path

from users import views as users_views


urlpatterns = [
    path('profile/', users_views.UpdateProfileView.as_view(
            template_name='users/update_profile.html'),
            name='update_profile'),
]
