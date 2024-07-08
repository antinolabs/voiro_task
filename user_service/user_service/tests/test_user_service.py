import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse

User = get_user_model()

@pytest.fixture(scope='function')
def user_factory(db):
    def create_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return create_user

@pytest.fixture
def user(user_factory):
    return user_factory(username='testuser', email='test@example.com', password='password')

@pytest.fixture
def api_client():
    return APIClient()

def test_register_user(api_client, db):
    payload = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123'
    }
    response = api_client.post(reverse('cr_users'), payload)
    assert response.status_code == 201
    assert User.objects.filter(username='newuser').exists()

def test_retrieve_user(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.get(reverse('rud_users', kwargs={'id': user.id}))
    assert response.status_code == 200
    assert response.data['username'] == user.username

def test_update_user(api_client, user):
    api_client.force_authenticate(user=user)
    payload = {
        'username': 'updateduser'
    }
    response = api_client.put(reverse('rud_users', kwargs={'id': user.id}), payload)
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.username == 'updateduser'

def test_delete_user(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.delete(reverse('rud_users', kwargs={'id': user.id}))
    assert response.status_code == 204
    assert not User.objects.filter(id=user.id).exists()
