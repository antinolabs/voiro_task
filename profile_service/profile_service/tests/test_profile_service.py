import pytest
from django.contrib.auth import get_user_model
from ..models import Profile
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import patch
from ..helpers import UserHelper

User = get_user_model()

@pytest.fixture(scope='function')
def user_factory(db):
    def create_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return create_user

@pytest.fixture(scope='function')
def profile_factory(db):
    def create_profile(**kwargs):
        return Profile.objects.create(**kwargs)
    return create_profile

@pytest.fixture
def user(user_factory):
    user = user_factory(username='testuser', email='test@example.com', password='password')
    print(f"User created: {user}")  
    return user

@pytest.fixture
def profile(profile_factory, user):
    profile = profile_factory(user_id=user.id, firstname='Test', lastname='User', role='developer')
    print(f"Profile created: {profile}")  
    return profile

@pytest.fixture
def api_client():
    return APIClient()

@patch.object(UserHelper, 'getUserDetail')
def test_create_profile(mock_getUserDetail, api_client, user):
    mock_getUserDetail.return_value = {'status_code': 200, 'data': {'id': user.id}}
    payload = {
        'user_id': user.id,
        'firstname': 'Test',
        'lastname': 'User',
        'role': 'developer'
    }
    response = api_client.post(reverse('profile'), payload, format='json')
    print(f"Create profile response: {response.data}")  
    assert response.status_code == 201
    assert Profile.objects.filter(user_id=user.id).exists()

@patch.object(UserHelper, 'getUserDetail')
def test_retrieve_profile(mock_getUserDetail, api_client, profile):
    mock_getUserDetail.return_value = {
        'status_code': 200,
        'data': {
            'id': profile.user_id,
            'username': 'testuser',  
            'email': 'test@example.com',  
            'firstname': profile.firstname,
            'lastname': profile.lastname,
            'role': profile.role,
            'created_at': profile.created_at,
            'updated_at': profile.updated_at
        }
    }
    url = reverse('profile-detail', kwargs={'user_id': profile.user_id})
    response = api_client.get(url)
    
    assert response.status_code == 200
    assert response.data['firstname'] == profile.firstname
    assert response.data['email'] == 'test@example.com'  

@patch.object(UserHelper, 'getUserDetail')
def test_update_profile(mock_getUserDetail, api_client, profile):
    mock_getUserDetail.return_value = {'status_code': 200, 'data': {'id': profile.user_id}}
    url = reverse('profile-detail', kwargs={'user_id': profile.user_id})
    payload = {
        'firstname': 'UpdatedName'
    }
    response = api_client.patch(url, data=payload, format='json')
    assert response.status_code == 200
    profile.refresh_from_db()
    assert profile.firstname == 'UpdatedName'

@patch.object(UserHelper, 'getUserDetail')
def test_partial_update_profile(mock_getUserDetail, api_client, profile):
    mock_getUserDetail.return_value = {'status_code': 200, 'data': {'id': profile.user_id}}
    url = reverse('profile-detail', kwargs={'user_id': profile.user_id})
    payload = {
        'lastname': 'UpdatedLastName'
    }
    response = api_client.patch(url, data=payload, format='json')
    assert response.status_code == 200
    profile.refresh_from_db()
    assert profile.lastname == 'UpdatedLastName'

@patch.object(UserHelper, 'getUserDetail')
def test_delete_profile(mock_getUserDetail, api_client, profile):
    mock_getUserDetail.return_value = {'status_code': 200, 'data': {'id': profile.user_id}}
    url = reverse('profile-detail', kwargs={'user_id': profile.user_id})
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Profile.objects.filter(user_id=profile.user_id).exists()