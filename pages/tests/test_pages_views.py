from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed

from pages.views import HomePageView


def test_url_exists_at_correct_location(homepage):
    assert homepage.status_code == 200


def test_homepage_template(homepage):
    assertTemplateUsed(homepage, 'home.html')


def test_homepage_contains_correct_html(homepage):
    assert 'Hello!' in homepage.content.decode('UTF-8')


def test_homepage_does_not_contain_incorrect_html(homepage):
    assert 'Something that should not be here' not in homepage.content.decode('UTF-8')


def test_homepage_url_resolves_homepage_view():
    view = resolve("/")
    assert view.func.__name__ == HomePageView.as_view().__name__
