from django.test import SimpleTestCase

from .forms import ProjectForm


class ProjectFormTests(SimpleTestCase):
    def test_accepts_github_link(self):
        form = ProjectForm(
            data={
                "name": "TeamFinder",
                "description": "Тестовый проект",
                "github_url": "https://github.com/openai/teamfinder",
                "status": "open",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_rejects_non_github_link(self):
        form = ProjectForm(
            data={
                "name": "TeamFinder",
                "description": "Тестовый проект",
                "github_url": "https://github.com.example.org/teamfinder",
                "status": "open",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("github_url", form.errors)
