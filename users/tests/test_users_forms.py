from users.forms import CustomUserCreationForm


def test_signup_uses_correct_form(signup):
    form = signup.context.get("form")
    assert isinstance(form, CustomUserCreationForm)


def test_signup_form_uses_csrf_token(signup):
    form = signup.context.get("form")
    assert 'csrfmiddlewaretoken' in signup.content.decode('UTF-8')
