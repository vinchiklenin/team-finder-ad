from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProjectForm
from .models import Project


def project_list(request):
    projects = Project.objects.select_related("owner").prefetch_related("participants")
    paginator = Paginator(projects, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects,
            "page_obj": page_obj,
            "query_prefix": "",
        },
    )


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"),
        pk=project_id,
    )
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(owner=request.user)
        project.participants.add(request.user)
        messages.success(request, "Проект опубликован.")
        return redirect("projects:detail", project_id=project.pk)
    return render(request, "projects/create-project.html", {"form": form, "is_edit": False})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user != project.owner and not request.user.is_staff:
        return HttpResponseForbidden("Редактировать проект может только его автор.")
    form = ProjectForm(request.POST or None, project=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Проект сохранён.")
        return redirect("projects:detail", project_id=project.pk)
    return render(request, "projects/create-project.html", {"form": form, "is_edit": True})


@require_POST
@login_required
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user != project.owner and not request.user.is_staff:
        return JsonResponse({"status": "error", "message": "Недостаточно прав."}, status=403)
    if project.status != Project.Status.OPEN:
        return JsonResponse({"status": "error", "message": "Проект уже завершён."}, status=400)
    project.status = Project.Status.CLOSED
    project.save(update_fields=("status",))
    return JsonResponse({"status": "ok", "project_status": project.status})


@require_POST
@login_required
def toggle_participation(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user == project.owner:
        return JsonResponse({"status": "error", "message": "Автор уже состоит в проекте."}, status=400)
    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
        return JsonResponse({"status": "ok", "participant": False})
    if project.status != Project.Status.OPEN:
        return JsonResponse({"status": "error", "message": "Нельзя вступить в закрытый проект."}, status=400)
    project.participants.add(request.user)
    return JsonResponse({"status": "ok", "participant": True})

@require_POST
@login_required
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user.favorites.filter(pk=project.pk).exists():
        request.user.favorites.remove(project)
        return JsonResponse({"status": "ok", "favorited": False})
    request.user.favorites.add(project)
    return JsonResponse({"status": "ok", "favorited": True})


@login_required
def favorite_projects(request):
    projects = (
        request.user.favorites
        .select_related("owner")
        .prefetch_related("participants")
    )
    return render(
    request,
        "projects/favorite_projects.html",
        {"projects": projects},
    )
