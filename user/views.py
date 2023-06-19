from django.contrib.auth import authenticate, logout ,login
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView, DeleteView, CreateView, TemplateView
from os import path
from django.utils.translation import gettext_lazy as _

from django.views.generic.base import View
from .forms import UserCreationForm, UserUpdateForm
from django.shortcuts import redirect
from pathlib import Path

User = get_user_model()

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
USER_TEMPLATES_DIR = path.join(ROOT_DIR, 'templates/user/')


class SuperUserMixin(PermissionRequiredMixin, LoginRequiredMixin):
    def has_permission(self):
        return self.request.user.is_superuser


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UseCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = path.join(USER_TEMPLATES_DIR, 'user_register.html')


user_create_view = UseCreateView.as_view()


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User

    def get_success_url(self):
        return reverse("home")


user_delete_view = UserDeleteView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = path.join(USER_TEMPLATES_DIR, 'user_update.html')

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Updated with success")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


# Create your views here.


class LoginView(View):

    def post(self, request):
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # correct username and password login the user
            print(auth.login(request, user))
            return redirect('home')

        else:
            messages.error(request,
                           "Error user/password is wrong")

            return redirect('account_login')

    def get(self, request):
        logout(request)
        response = JsonResponse({'message': 'Logout done'})
        return response
