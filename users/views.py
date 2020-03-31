from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from users.forms import CustomUserChangeForm


@method_decorator(login_required, name='dispatch')
class UpdateProfileView(UpdateView):
    form = CustomUserChangeForm
    fields = ('email',)  # CustomUserChangeForm.fields
    template = 'users/update_profile.html'
    success_url = reverse_lazy('schemas_customers:home')

    def get_object(self):
        return self.request.user
