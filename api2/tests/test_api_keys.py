import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from ..app.main import app
from ..app.core.api_key_manager import APIKeyManager
from ..app.db.database import get_db

client = TestClient(app)

# Datos de prueba
TEST_ADMIN_EMAIL = "admin@test.com"
TEST_USER_EMAIL = "user@test.com"
TEST_ADMIN_PASSWORD = "admin123"  # Asegúrate de que coincida con tu configuración

def test_generate_admin_api_key():
    """Test generating an admin API key"""
    response = client.post(
        "/api/v1/admin/generate-api-key",
        json={
            "email": TEST_ADMIN_EMAIL,
            "name": "Test Admin",
            "requests_per_month": 100000,
            "expires_in_days": 30
        },
        headers={"Authorization": f"Basic {TEST_ADMIN_PASSWORD}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "api_key" in data
    assert data["email"] == TEST_ADMIN_EMAIL
    assert data["name"] == "Test Admin"
    return data["api_key"]

def test_generate_user_api_key(admin_api_key):
    """Test generating a user API key"""
    response = client.post(
        "/api/v1/admin/generate-api-key",
        json={
            "email": TEST_USER_EMAIL,
            "name": "Test User",
            "requests_per_month": 10000,
            "expires_in_days": 30
        },
        headers={"X-API-KEY": admin_api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert "api_key" in data
    assert data["email"] == TEST_USER_EMAIL
    return data["api_key"]

def test_duplicate_email_api_key(admin_api_key):
    """Test that you can't create two API keys for the same email"""
    response = client.post(
        "/api/v1/admin/generate-api-key",
        json={
            "email": TEST_USER_EMAIL,
            "name": "Test User 2",
            "requests_per_month": 10000
        },
        headers={"X-API-KEY": admin_api_key}
    )
    assert response.status_code == 400
    assert "already has an API key" in response.json()["detail"]

def test_search_with_api_key(user_api_key):
    """Test using the search endpoint with an API key"""
    response = client.get(
        "/api/v1/search",
        params={"query": "test"},
        headers={"X-API-KEY": user_api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert "api_key_info" in data
    assert data["api_key_info"]["email"] == TEST_USER_EMAIL
    assert "requests_remaining" in data["api_key_info"]

def test_invalid_api_key():
    """Test using an invalid API key"""
    response = client.get(
        "/api/v1/search",
        params={"query": "test"},
        headers={"X-API-KEY": "invalid_key"}
    )
    assert response.status_code == 401

def test_list_api_keys(admin_api_key):
    """Test listing all API keys"""
    response = client.get(
        "/api/v1/admin/api-keys",
        headers={"X-API-KEY": admin_api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Should have at least admin and user keys

def test_revoke_api_key(admin_api_key, user_api_key):
    """Test revoking an API key"""
    response = client.post(
        f"/api/v1/admin/keys/revoke/{user_api_key}",
        headers={"X-API-KEY": admin_api_key}
    )
    assert response.status_code == 200
    
    # Try to use revoked key
    response = client.get(
        "/api/v1/search",
        params={"query": "test"},
        headers={"X-API-KEY": user_api_key}
    )
    assert response.status_code == 401

@pytest.fixture
def admin_api_key():
    """Fixture to get admin API key"""
    return test_generate_admin_api_key()

@pytest.fixture
def user_api_key(admin_api_key):
    """Fixture to get user API key"""
    return test_generate_user_api_key(admin_api_key) 