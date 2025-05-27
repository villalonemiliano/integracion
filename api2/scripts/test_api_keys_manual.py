import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@test.com"
USER_EMAIL = "user@test.com"
ADMIN_PASSWORD = "admin123"  # Asegúrate de que coincida con tu configuración

def print_response(response):
    """Print response in a readable format"""
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_api_key_system():
    # 1. Generar API key administrativa
    print("\n1. Generando API key administrativa...")
    response = requests.post(
        f"{BASE_URL}/api/v1/admin/generate-api-key",
        json={
            "email": ADMIN_EMAIL,
            "name": "Test Admin",
            "requests_per_month": 100000,
            "expires_in_days": 30
        },
        headers={"Authorization": f"Basic {ADMIN_PASSWORD}"}
    )
    print_response(response)
    admin_api_key = response.json()["api_key"]

    # 2. Generar API key de usuario
    print("\n2. Generando API key de usuario...")
    response = requests.post(
        f"{BASE_URL}/api/v1/admin/generate-api-key",
        json={
            "email": USER_EMAIL,
            "name": "Test User",
            "requests_per_month": 10000,
            "expires_in_days": 30
        },
        headers={"X-API-KEY": admin_api_key}
    )
    print_response(response)
    user_api_key = response.json()["api_key"]

    # 3. Listar todas las API keys
    print("\n3. Listando todas las API keys...")
    response = requests.get(
        f"{BASE_URL}/api/v1/admin/api-keys",
        headers={"X-API-KEY": admin_api_key}
    )
    print_response(response)

    # 4. Probar búsqueda con API key de usuario
    print("\n4. Probando búsqueda con API key de usuario...")
    response = requests.get(
        f"{BASE_URL}/api/v1/search",
        params={"query": "test"},
        headers={"X-API-KEY": user_api_key}
    )
    print_response(response)

    # 5. Intentar crear API key duplicada
    print("\n5. Intentando crear API key duplicada...")
    response = requests.post(
        f"{BASE_URL}/api/v1/admin/generate-api-key",
        json={
            "email": USER_EMAIL,
            "name": "Test User 2",
            "requests_per_month": 10000
        },
        headers={"X-API-KEY": admin_api_key}
    )
    print_response(response)

    # 6. Revocar API key de usuario
    print("\n6. Revocando API key de usuario...")
    response = requests.post(
        f"{BASE_URL}/api/v1/admin/keys/revoke/{user_api_key}",
        headers={"X-API-KEY": admin_api_key}
    )
    print_response(response)

    # 7. Intentar usar API key revocada
    print("\n7. Intentando usar API key revocada...")
    response = requests.get(
        f"{BASE_URL}/api/v1/search",
        params={"query": "test"},
        headers={"X-API-KEY": user_api_key}
    )
    print_response(response)

if __name__ == "__main__":
    print("Iniciando pruebas del sistema de API keys...")
    test_api_key_system()
    print("\nPruebas completadas!") 