from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserEmailCreationForm


class RegisterUser(CreateView):
    form_class = UserEmailCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'
