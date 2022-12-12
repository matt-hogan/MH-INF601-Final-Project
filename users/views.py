from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from .forms import AdminUserCreation


class SignUpView(CreateView):
    form_class = AdminUserCreation
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        """ Authenticates and logs the user in after account creation """
        form.save()
        email = self.request.POST["email"]
        password = self.request.POST["password"]
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return HttpResponseRedirect(reverse('odds:odds_home'))
