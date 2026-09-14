from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ChangePasswordForm, LoginForm, ProfileForm, RegistrationForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect("projects:list")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("projects:list")
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("projects:list")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(request, user)
            return redirect("projects:list")
        form.add_error(None, "Неверный email или пароль.")
    return render(request, "users/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("projects:list")


def user_detail(request, user_id):
    profile_user = get_object_or_404(
        User.objects.prefetch_related("owned_projects__participants"),
        pk=user_id,
    )
    return render(request, "users/user-details.html", {"user": profile_user})


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Профиль сохранён.")
        return redirect("users:detail", user_id=request.user.pk)
    return render(request, "users/edit_profile.html", {"form": form, "user": request.user})


@login_required
def change_password(request):
    form = ChangePasswordForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Пароль изменён.")
        return redirect("users:detail", user_id=request.user.pk)
    return render(request, "users/change_password.html", {"form": form})


def user_list(request):
    participants = User.objects.order_by("-id")
    paginator = Paginator(participants, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "users/participants.html",
        {
            "participants": participants,
            "page_obj": page_obj,
            "query_prefix": "",
            "active_filter": None,
        },
    )
