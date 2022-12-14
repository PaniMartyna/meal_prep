from django.urls import resolve, reverse


def test_home_not_logged_in(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert 'planuj!' not in str(response.content)
    assert 'zakupy' not in str(response.content)
    assert 'kucharska' not in str(response.content)
    assert 'dodaj przepis' not in str(response.content)


def test_home_logged_in(client, user):
    client.force_login(user)
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert 'planuj!' in str(response.content)
    assert 'zakupy' in str(response.content)
    assert 'kucharska' in str(response.content)
    assert 'dodaj przepis' in str(response.content)


def test_about(client):
    url = reverse('about')
    response = client.get(url)

    assert response.status_code == 200
    assert 'informacje' in str(response.content)