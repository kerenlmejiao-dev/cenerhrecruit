"""
test_quick.py - Testing rápido de endpoints
No requiere pytest, solo requests
"""

import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Verificar que API está viva"""
    print("\n✅ TEST 1: Health Check")
    r = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
    assert r.status_code == 200
    print("   ✓ PASSED\n")

def test_tests_disponibles():
    """Obtener banco completo de tests (9 base + 5 de Roles Estratégicos)"""
    print("✅ TEST 2: GET /api/tests/disponibles")
    r = requests.get(f"{BASE_URL}/api/tests/disponibles")
    print(f"   Status: {r.status_code}")
    data = r.json()
    print(f"   Total tests: {data['total_tests']}")
    print(f"   Total preguntas: {data['total_preguntas']}")
    print(f"   Tests:")
    for test in data['tests']:
        print(f"      - {test['nombre']} ({test['num_preguntas']} preg)")
    assert r.status_code == 200
    assert data['total_tests'] == 14
    assert data['total_preguntas'] == 340
    print("   ✓ PASSED\n")

def test_test_info():
    """Obtener información de un test"""
    print("✅ TEST 3: GET /api/tests/{test_id}/info")
    r = requests.get(f"{BASE_URL}/api/tests/verbal/info")
    print(f"   Status: {r.status_code}")
    data = r.json()
    print(f"   Test: {data['nombre']}")
    print(f"   Preguntas esperadas: {data['num_preguntas_esperadas']}")
    print(f"   Calidad: {data['calidad']}/100")
    assert r.status_code == 200
    assert data['nombre'] == 'Razonamiento Verbal'
    print("   ✓ PASSED\n")

def test_vacante_config():
    """Obtener configuración de vacante"""
    print("✅ TEST 4: GET /api/vacantes/{vacante_id}/config")
    r = requests.get(f"{BASE_URL}/api/vacantes/contador_paraiso/config")
    print(f"   Status: {r.status_code}")
    data = r.json()
    print(f"   Vacante: {data['nombre']}")
    print(f"   Cliente: {data['cliente']}")
    print(f"   Tests a aplicar: {', '.join(data['tests_a_aplicar'])}")
    print(f"   Pesos:")
    for cat, peso in data['pesos_scoring'].items():
        print(f"      - {cat}: {peso * 100:.0f}%")
    assert r.status_code == 200
    assert data['vacante_id'] == 'contador_paraiso'
    print("   ✓ PASSED\n")

def test_obtener_preguntas():
    """Obtener preguntas de un test"""
    print("✅ TEST 5: GET /api/tests/{test_id}/{candidato_id}")
    r = requests.get(f"{BASE_URL}/api/tests/verbal/cand_001")
    print(f"   Status: {r.status_code}")
    data = r.json()
    print(f"   Test: {data['test_nombre']}")
    print(f"   Candidato: {data['candidato_id']}")
    print(f"   Total preguntas: {data['total_preguntas']}")
    print(f"   Tiempo estimado: {data['tiempo_estimado']} segundos")
    if data['preguntas']:
        print(f"   Primera pregunta:")
        q = data['preguntas'][0]
        print(f"      ID: {q['id']}")
        print(f"      Número: {q['numero']}")
        print(f"      Pregunta: {q['pregunta'][:70]}...")
    assert r.status_code == 200
    print("   ✓ PASSED\n")

def test_error_test_no_existe():
    """Test de error: Test no existe"""
    print("✅ TEST 6: Error handling - Test no existe")
    r = requests.get(f"{BASE_URL}/api/tests/test_inexistente/info")
    print(f"   Status: {r.status_code}")
    assert r.status_code == 404
    print("   ✓ PASSED (Error manejado correctamente)\n")

def test_error_vacante_no_existe():
    """Test de error: Vacante no existe"""
    print("✅ TEST 7: Error handling - Vacante no existe")
    r = requests.get(f"{BASE_URL}/api/vacantes/vacante_inexistente/config")
    print(f"   Status: {r.status_code}")
    assert r.status_code == 404
    print("   ✓ PASSED (Error manejado correctamente)\n")

def main():
    """Ejecutar todos los tests"""
    print("\n" + "=" * 70)
    print("🧪 TESTING RÁPIDO - CENERH RECRUIT OS")
    print("=" * 70)
    
    try:
        test_health()
        test_tests_disponibles()
        test_test_info()
        test_vacante_config()
        test_obtener_preguntas()
        test_error_test_no_existe()
        test_error_vacante_no_existe()
        
        print("=" * 70)
        print("✅ TODOS LOS TESTS PASARON")
        print("=" * 70)
        print("\n📊 Resumen:")
        print("   ✓ API funcionando correctamente")
        print("   ✓ 14 tests cargados (9 base + 5 Roles Estratégicos)")
        print("   ✓ 340 preguntas disponibles")
        print("   ✓ Endpoints de lectura funcionando")
        print("   ✓ Error handling correcto")
        print("\n🚀 API funcionando - Fase 1 (multi-portal)\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FALLÓ: {e}\n")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se puede conectar a la API")
        print("   Asegúrate de que la API está corriendo:")
        print("   python api.py\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")

if __name__ == "__main__":
    main()
