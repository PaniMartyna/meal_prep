from django.urls import resolve

from pages.views import HomePageView, AboutPageView


# Home Page test

def test_homepage_url_resolves_homepage_view():
    view = resolve("/")
    assert view.func.__name__ == HomePageView.as_view().__name__


# About Page test

def test_about_resolves_about_view():
    view = resolve("/about/")
    assert view.func.__name__ == AboutPageView.as_view().__name__