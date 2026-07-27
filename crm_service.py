"""
CENERH RECRUIT OS - Servicio de Integración CRM
Sincronización automática de candidatos con HubSpot
"""

import os
import json
import httpx
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class EstadoCRM(str, Enum):
    """Estados del candidato en CRM"""
    NUEVO = "appointment_scheduled"
    EVALUACION = "qualification_in_progress"
    SELECCIONADO = "decision_pending"
    CONTRATADO = "negotiation"
    NO_SELECCIONADO = "disqualified"


class HubSpotService:
    """Servicio para integración con HubSpot"""

    def __init__(self):
        self.api_key = os.getenv("HUBSPOT_API_KEY", "")
        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def crear_contacto(
        self,
        nombre: str,
        email: str,
        telefono: str = "",
        vacante_id: str = "",
        candidato_id: str = "",
    ) -> Optional[Dict[str, Any]]:
        """Crear contacto en HubSpot"""

        if not self.api_key:
            print("⚠️  HUBSPOT_API_KEY no configurada")
            return None

        # Dividir nombre
        partes_nombre = nombre.split(" ", 1)
        nombre_primero = partes_nombre[0]
        apellido = partes_nombre[1] if len(partes_nombre) > 1 else ""

        datos = {
            "properties": {
                "firstname": nombre_primero,
                "lastname": apellido,
                "email": email,
                "phone": telefono,
                "hs_lead_status": "OPEN",
                # Campos custom
                "candidato_id": candidato_id,
                "vacante_id": vacante_id,
                "source": "CENERH Recruit OS",
            }
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/crm/v3/objects/contacts",
                    json=datos,
                    headers=self.headers,
                    timeout=10,
                )

                if response.status_code in [200, 201]:
                    resultado = response.json()
                    return {
                        "hubspot_id": resultado["id"],
                        "email": email,
                        "estado": "creado",
                    }
                else:
                    print(f"Error HubSpot: {response.status_code} - {response.text}")
                    return None

        except Exception as e:
            print(f"Error creando contacto HubSpot: {e}")
            return None

    async def actualizar_contacto(
        self, hubspot_id: str, propiedades: Dict[str, Any]
    ) -> bool:
        """Actualizar contacto en HubSpot"""

        if not self.api_key:
            return False

        datos = {"properties": propiedades}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.base_url}/crm/v3/objects/contacts/{hubspot_id}",
                    json=datos,
                    headers=self.headers,
                    timeout=10,
                )

                return response.status_code in [200, 201]

        except Exception as e:
            print(f"Error actualizando contacto: {e}")
            return False

    async def crear_deal(
        self,
        nombre: str,
        contacto_id: str,
        vacante_id: str,
        monto: float,
        estado: EstadoCRM = EstadoCRM.NUEVO,
    ) -> Optional[Dict[str, Any]]:
        """Crear deal (oportunidad) en HubSpot"""

        if not self.api_key:
            return None

        datos = {
            "properties": {
                "dealname": f"{nombre} - {vacante_id}",
                "dealstage": estado.value,
                "amount": str(monto),
                "closedate": self._fecha_cierre(),
                "pipeline": "0",  # Pipeline default
                "hubspot_owner_id": "",  # Asignar a owner si existe
            },
            "associations": [
                {
                    "types": [{"associationType": "deal_contact", "direction": "FORWARD"}],
                    "id": contacto_id,
                }
            ],
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/crm/v3/objects/deals",
                    json=datos,
                    headers=self.headers,
                    timeout=10,
                )

                if response.status_code in [200, 201]:
                    resultado = response.json()
                    return {
                        "deal_id": resultado["id"],
                        "nombre": nombre,
                        "estado": estado.value,
                    }
                else:
                    print(f"Error creando deal: {response.status_code}")
                    return None

        except Exception as e:
            print(f"Error creando deal: {e}")
            return None

    async def actualizar_deal(
        self, deal_id: str, estado: EstadoCRM, propiedades: Dict[str, Any] = None
    ) -> bool:
        """Actualizar deal con nuevo estado"""

        if not self.api_key:
            return False

        props = {"dealstage": estado.value}
        if propiedades:
            props.update(propiedades)

        datos = {"properties": props}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.base_url}/crm/v3/objects/deals/{deal_id}",
                    json=datos,
                    headers=self.headers,
                    timeout=10,
                )

                return response.status_code in [200, 201]

        except Exception as e:
            print(f"Error actualizando deal: {e}")
            return False

    async def agregar_nota(
        self, contacto_id: str, nota: str, titulo: str = "Evaluación CENERH"
    ) -> bool:
        """Agregar nota (engagement) a contacto"""

        if not self.api_key:
            return False

        datos = {
            "properties": {
                "hs_note_body": nota,
                "hs_note_text": nota,
            }
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.base_url}/crm/v3/objects/contacts/{contacto_id}",
                    json=datos,
                    headers=self.headers,
                    timeout=10,
                )

                return response.status_code in [200, 201]

        except Exception as e:
            print(f"Error agregando nota: {e}")
            return False

    async def crear_tarea(
        self, contacto_id: str, titulo: str, descripcion: str, fecha_vencimiento: str
    ) -> bool:
        """Crear tarea en HubSpot"""

        if not self.api_key:
            return False

        datos = {
            "properties": {
                "hs_task_subject": titulo,
                "hs_task_body": descripcion,
                "hs_task_due_date": fecha_vencimiento,
                "hs_task_status": "OPEN",
            },
            "associations": [
                {
                    "types": [{"associationType": "contact_to_task", "direction": "FORWARD"}],
                    "id": contacto_id,
                }
            ],
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/crm/v3/objects/tasks",
                    json=datos,
                    headers=self.headers,
                    timeout=10,
                )

                return response.status_code in [200, 201]

        except Exception as e:
            print(f"Error creando tarea: {e}")
            return False

    async def buscar_contacto_por_email(self, email: str) -> Optional[str]:
        """Buscar contacto por email"""

        if not self.api_key:
            return None

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/crm/v3/objects/contacts",
                    params={"limit": 1, "filterGroups": [{"filters": [{"propertyName": "email", "operator": "EQ", "value": email}]}]},
                    headers=self.headers,
                    timeout=10,
                )

                if response.status_code == 200:
                    resultados = response.json().get("results", [])
                    if resultados:
                        return resultados[0]["id"]

                return None

        except Exception as e:
            print(f"Error buscando contacto: {e}")
            return None

    def _fecha_cierre(self) -> str:
        """Generar fecha de cierre (30 días desde hoy)"""
        from datetime import datetime, timedelta

        fecha = datetime.now() + timedelta(days=30)
        return fecha.strftime("%Y-%m-%dT%H:%M:%SZ")


class PipedrivService:
    """Servicio para integración con Pipedrive (alternativa)"""

    def __init__(self):
        self.api_token = os.getenv("PIPEDRIVE_API_TOKEN", "")
        self.base_url = "https://api.pipedrive.com/v1"

    async def crear_persona(
        self,
        nombre: str,
        email: str,
        telefono: str = "",
        candidato_id: str = "",
    ) -> Optional[Dict[str, Any]]:
        """Crear persona en Pipedrive"""

        if not self.api_token:
            return None

        datos = {
            "name": nombre,
            "email": email,
            "phone": telefono,
            "custom_fields": {
                "candidato_id": candidato_id,
            },
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/persons",
                    params={"api_token": self.api_token},
                    json=datos,
                    timeout=10,
                )

                if response.status_code in [200, 201]:
                    resultado = response.json()
                    if resultado.get("success"):
                        return {
                            "pipedrive_id": resultado["data"]["id"],
                            "email": email,
                            "estado": "creado",
                        }

                return None

        except Exception as e:
            print(f"Error creando persona Pipedrive: {e}")
            return None

    async def crear_deal(
        self, titulo: str, persona_id: str, monto: float, pipedrive_stage: int = 1
    ) -> Optional[Dict[str, Any]]:
        """Crear deal en Pipedrive"""

        if not self.api_token:
            return None

        datos = {
            "title": titulo,
            "person_id": persona_id,
            "value": monto,
            "currency": "USD",
            "stage_id": pipedrive_stage,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/deals",
                    params={"api_token": self.api_token},
                    json=datos,
                    timeout=10,
                )

                if response.status_code in [200, 201]:
                    resultado = response.json()
                    if resultado.get("success"):
                        return {
                            "deal_id": resultado["data"]["id"],
                            "titulo": titulo,
                            "estado": "creado",
                        }

                return None

        except Exception as e:
            print(f"Error creando deal Pipedrive: {e}")
            return None


# Inicializar servicios
hubspot_service = HubSpotService()
pipedrive_service = PipedrivService()
