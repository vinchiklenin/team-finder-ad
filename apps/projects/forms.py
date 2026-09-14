from django import forms

from team_finder.validators import validate_github_url

from .models import Project


class ProjectForm(forms.Form):
    name = forms.CharField(label="Название проекта", max_length=200)
    description = forms.CharField(label="Описание", required=False, widget=forms.Textarea)
    github_url = forms.URLField(label="Ссылка на GitHub", required=False)
    status = forms.ChoiceField(label="Статус", choices=Project.Status.choices)

    def __init__(self, *args, project: Project | None = None, **kwargs):
        self.project = project
        if project and "initial" not in kwargs:
            kwargs["initial"] = {
                "name": project.name,
                "description": project.description,
                "github_url": project.github_url,
                "status": project.status,
            }
        super().__init__(*args, **kwargs)

    def clean_github_url(self) -> str:
        return validate_github_url(self.cleaned_data["github_url"])

    def save(self, owner=None) -> Project:
        if self.project is None:
            if owner is None:
                raise ValueError("Для нового проекта нужен автор.")
            self.project = Project(owner=owner)
        self.project.name = self.cleaned_data["name"]
        self.project.description = self.cleaned_data["description"]
        self.project.github_url = self.cleaned_data["github_url"]
        self.project.status = self.cleaned_data["status"]
        self.project.save()
        return self.project
