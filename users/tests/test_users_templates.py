from django.urls import resolve
from pytest_django.asserts import assertTemplateUsed

from users.views import SignUpView


def test_signup_url_exists_at_correct_location(signup):
    assert signup.status_code == 200


def test_signup_template(signup):
    assertTemplateUsed(signup, 'registration/signup.html')


def test_signup_contains_correct_html(signup):
    assert 'Rejestracja' in signup.content.decode('UTF-8')


def test_signup_does_not_contain_incorrect_html(signup):
    assert 'Something that should not be here' not in signup.content.decode('UTF-8')


def test_signup_url_resolves_signup_view():
    view = resolve("/users/signup/")
    assert view.func.__name__ == SignUpView.as_view().__name__

