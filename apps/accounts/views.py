from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from apps.pages.site_data import site_context

from .forms import CustomerLoginForm, CustomerProfileForm, CustomerSignupForm
from .models import CustomerProfile


class CustomerLoginView(LoginView):
    authentication_form = CustomerLoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(site_context())
        return context


class CustomerLogoutView(LogoutView):
    next_page = reverse_lazy("pages:home")


def signup(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    if request.method == "POST":
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()
            CustomerProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data["phone_number"],
                delivery_location=form.cleaned_data["delivery_location"],
            )
            login(request, user)
            messages.success(request, "Your account is ready.")
            return redirect("accounts:profile")
    else:
        form = CustomerSignupForm()

    context = site_context()
    context["form"] = form
    return render(request, "accounts/signup.html", context)


@login_required
def profile(request):
    profile_obj, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=profile_obj)
        if form.is_valid():
            request.user.first_name = form.cleaned_data["first_name"]
            request.user.last_name = form.cleaned_data["last_name"]
            request.user.email = form.cleaned_data["email"]
            request.user.save()
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = CustomerProfileForm(
            instance=profile_obj,
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            },
        )

    context = site_context()
    context["form"] = form
    return render(request, "accounts/profile.html", context)
