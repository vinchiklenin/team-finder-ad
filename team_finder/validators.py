from urllib.parse import urlparse

from django.core.exceptions import ValidationError


GITHUB_HOSTS = {"github.com", "www.github.com"}


def validate_github_url(url: str) -> str:
    if not url:
        return ""

    parsed_url = urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or parsed_url.hostname not in GITHUB_HOSTS:
        raise ValidationError("Укажите ссылку на github.com.")
    return url
