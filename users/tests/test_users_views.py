from django.urls import resolve, reverse
from pytest_django.asserts import assertTemplateUsed

from users.views import SignUpView





def test_signup(client):
    url = reverse('users:signup')
    response = client.get(reverse('users:signup'))
    form_used = response.context.get("form")

    assert response.status_code == 200
    assertTemplateUsed(response, 'registration/signup.html')
    assert 'Rejestracja' in str(response.content)
    from users.forms import CustomUserCreationForm
    assert isinstance(form_used, CustomUserCreationForm)

