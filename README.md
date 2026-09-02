# Taller Docker

API REST pequena construida con FastAPI que genera una cedula aleatoria.

## Requisitos

- Docker Desktop con Docker Compose habilitado.
- Puerto `8000` disponible en el equipo local.

## Levantar el servicio

Desde la raiz del proyecto, ejecuta:

```powershell
docker compose up --build
```

Para levantarlo en segundo plano:

```powershell
docker compose up --build -d
```

El servicio quedara disponible en:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Especificacion OpenAPI JSON: http://localhost:8000/openapi.json

## Endpoint

### Obtener una cedula

`GET /obtenerCedula`

No requiere parametros ni body de entrada. Cada llamada genera un numero aleatorio de 10 digitos.

Ejemplo con PowerShell:

```powershell
Invoke-RestMethod http://localhost:8000/obtenerCedula
```

Ejemplo con cURL:

```bash
curl http://localhost:8000/obtenerCedula
```

Respuesta `200 OK`:

```json
{
  "cedula": 1234567890
}
```

El valor de `cedula` cambia en cada solicitud.

## Coleccion de Postman

La coleccion lista para importar esta en [postman_collection.json](postman_collection.json).

1. Abre Postman.
2. Selecciona **Import**.
3. Elige `postman_collection.json`.
4. Ejecuta la solicitud **Obtener cedula**.

La variable `baseUrl` apunta por defecto a `http://localhost:8000`.

## Swagger / OpenAPI

FastAPI genera Swagger automaticamente a partir de la aplicacion. No es necesario instalar ni configurar un servidor adicional: abre [http://localhost:8000/docs](http://localhost:8000/docs) con el contenedor ejecutandose.

Tambien se incluye una especificacion independiente en [openapi.yaml](openapi.yaml), util para importar el contrato en herramientas compatibles con OpenAPI.

## Detener y administrar el contenedor

Detener y eliminar el contenedor:

```powershell
docker compose down
```

Ver logs:

```powershell
docker compose logs -f api
```

Ver el estado de los servicios:

```powershell
docker compose ps
```

## Ejecucion local sin Docker

Opcionalmente, con Python instalado:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Luego visita http://localhost:8000/docs.

## Solucion de problemas

- Si el puerto `8000` esta ocupado, cambia `"8000:8000"` en `docker-compose.yml` por otro puerto, por ejemplo `"8080:8000"`, y usa `http://localhost:8080`.
- Si modificas `requirements.txt` o `DockerFile`, vuelve a construir con `docker compose up --build`.
