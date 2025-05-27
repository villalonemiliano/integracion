import requests
import json
from datetime import datetime, timedelta
import time

# Configuración
BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@test.com"
USER_EMAIL = "user@test.com"
ADMIN_PASSWORD = "admin123"  # Asegúrate de que coincida con tu configuración

def print_response(response, title):
    """Print response in a readable format"""
    print(f"\n{title}")
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_complete_system():
    print("Iniciando pruebas del sistema completo...")
    
    # 1. Crear Planes
    print("\n1. Creando planes...")
    plans = [
        {
            "name": "Plan Básico",
            "description": "Plan para usuarios principiantes",
            "requests_per_second": 5,
            "requests_per_month": 10000,
            "duration_days": 30,
            "price": 29.99
        },
        {
            "name": "Plan Pro",
            "description": "Plan para usuarios avanzados",
            "requests_per_second": 20,
            "requests_per_month": 50000,
            "duration_days": 30,
            "price": 99.99
        }
    ]
    
    created_plans = []
    for plan in plans:
        response = requests.post(
            f"{BASE_URL}/api/v1/admin/plans",
            json=plan,
            headers={"Authorization": f"Basic {ADMIN_PASSWORD}"}
        )
        print_response(response, f"Creando plan: {plan['name']}")
        created_plans.append(response.json())
    
    # 2. Generar API Key Administrativa
    print("\n2. Generando API key administrativa...")
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
    print_response(response, "API Key Administrativa")
    admin_api_key = response.json()["api_key"]
    
    # 3. Generar API Keys de Usuario
    print("\n3. Generando API keys de usuario...")
    user_api_keys = []
    for i, plan in enumerate(created_plans):
        response = requests.post(
            f"{BASE_URL}/api/v1/admin/generate-api-key",
            json={
                "email": f"user{i+1}@test.com",
                "name": f"Test User {i+1}",
                "plan_id": plan["id"]
            },
            headers={"X-API-KEY": admin_api_key}
        )
        print_response(response, f"API Key Usuario {i+1}")
        user_api_keys.append(response.json()["api_key"])
    
    # 4. Probar Límites de Uso
    print("\n4. Probando límites de uso...")
    for i, api_key in enumerate(user_api_keys):
        print(f"\nProbando límites para usuario {i+1}...")
        # Hacer múltiples peticiones rápidas
        for j in range(3):
            response = requests.get(
                f"{BASE_URL}/api/v1/search",
                params={"query": f"test{j}"},
                headers={"X-API-KEY": api_key}
            )
            print_response(response, f"Petición {j+1}")
            time.sleep(0.2)  # Pequeña pausa entre peticiones
    
    # 5. Verificar Estadísticas de Cliente
    print("\n5. Verificando estadísticas de cliente...")
    for i, api_key in enumerate(user_api_keys):
        response = requests.get(
            f"{BASE_URL}/api/v1/usage/client",
            headers={"X-API-KEY": api_key}
        )
        print_response(response, f"Estadísticas Usuario {i+1}")
    
    # 6. Verificar Estadísticas de Admin
    print("\n6. Verificando estadísticas de administrador...")
    response = requests.get(
        f"{BASE_URL}/api/v1/usage/admin",
        headers={"X-API-KEY": admin_api_key}
    )
    print_response(response, "Estadísticas Administrador")
    
    # 7. Listar Planes
    print("\n7. Listando planes...")
    response = requests.get(
        f"{BASE_URL}/api/v1/admin/plans",
        headers={"X-API-KEY": admin_api_key}
    )
    print_response(response, "Lista de Planes")
    
    # 8. Listar API Keys
    print("\n8. Listando API keys...")
    response = requests.get(
        f"{BASE_URL}/api/v1/admin/api-keys",
        headers={"X-API-KEY": admin_api_key}
    )
    print_response(response, "Lista de API Keys")
    
    # 9. Probar Revocación de API Key
    print("\n9. Probando revocación de API key...")
    if user_api_keys:
        response = requests.post(
            f"{BASE_URL}/api/v1/admin/keys/revoke/{user_api_keys[0]}",
            headers={"X-API-KEY": admin_api_key}
        )
        print_response(response, "Revocación de API Key")
        
        # Intentar usar API key revocada
        response = requests.get(
            f"{BASE_URL}/api/v1/search",
            params={"query": "test"},
            headers={"X-API-KEY": user_api_keys[0]}
        )
        print_response(response, "Intento de uso de API Key revocada")
    
    # 10. Probar Límites de Plan
    print("\n10. Probando límites de plan...")
    if len(user_api_keys) > 1:
        # Intentar exceder límites de peticiones por segundo
        print("Probando límite de peticiones por segundo...")
        for i in range(10):
            response = requests.get(
                f"{BASE_URL}/api/v1/search",
                params={"query": f"test{i}"},
                headers={"X-API-KEY": user_api_keys[1]}
            )
            print(f"Petición {i+1}: Status {response.status_code}")
            time.sleep(0.1)
    
    print("\nPruebas completadas!")

if __name__ == "__main__":
    test_complete_system() 