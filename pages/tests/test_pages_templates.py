from pytest_django.asserts import assertTemplateUsed


# Home Page tests

def test_homepage_url_exists_at_correct_location(homepage):
    assert homepage.status_code == 200


def test_homepage_template(homepage):
    assertTemplateUsed(homepage, 'home.html')


def test_homepage_contains_correct_html(homepage):
    assert 'Hello!' in homepage.content.decode('UTF-8')


def test_homepage_does_not_contain_incorrect_html(homepage):
    assert 'something that should not be here' not in homepage.content.decode('UTF-8')


# About Page test

def test_about_url_exists_at_correct_location(about):
    assert about.status_code == 200


def test_about_template(about):
    assertTemplateUsed(about, 'about.html')


def test_about_contains_correct_html(about):
    assert 'o aplikacji' in about.content.decode('UTF-8')


def test_about_does_not_contain_incorrect_html(about):
    assert 'something that should not be here' not in about.content.decode('UTF-8')

