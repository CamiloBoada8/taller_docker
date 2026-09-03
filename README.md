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

### Obtener un numero romano

`GET /obtenerNumeroRomano`

Genera un entero aleatorio entre 50 y 100, ambos incluidos, y devuelve tambien su
representacion en numeros romanos.

```powershell
Invoke-RestMethod http://localhost:8000/obtenerNumeroRomano
```

Respuesta `200 OK`:

```json
{
  "numero": 74,
  "numero_romano": "LXXIV"
}
```

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

## Despliegue continuo gratuito en Render

El workflow [`.github/workflows/deploy-render.yml`](.github/workflows/deploy-render.yml)
valida la aplicacion y solicita a Render el despliegue del commit exacto cada vez que
se hace `push` a la rama `main`. Tambien se puede ejecutar manualmente desde la
pestana **Actions** de GitHub.

### 1. Publicar el repositorio

Sube el proyecto a GitHub y comprueba que la rama de produccion se llame `main`.

### 2. Crear el Web Service gratuito

1. Crea una cuenta en [Render](https://render.com/) e inicia sesion.
2. Selecciona **New > Web Service**, conecta GitHub y elige este repositorio.
3. Configura el servicio con estos valores:
   - **Branch:** `main`
   - **Language/Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path:** `/openapi.json`
   - **Instance Type/Compute:** `Free`
4. Crea el servicio y espera a que termine el primer despliegue.

### 3. Conectar GitHub Actions con Render

1. En Render, abre el servicio y entra a **Settings**.
2. Copia su **Deploy Hook**. Esta URL es secreta y no debe guardarse en el codigo.
3. En GitHub, abre el repositorio y entra a **Settings > Secrets and variables >
   Actions**.
4. Selecciona **New repository secret**.
5. Usa el nombre `RENDER_DEPLOY_HOOK_URL`, pega como valor la URL copiada de
   Render y guarda el secreto.
6. En Render, desactiva **Auto-Deploy** para evitar que Render y GitHub Actions
   inicien dos despliegues para el mismo `push`.

### 4. Activar el despliegue continuo

Haz commit de los cambios y subelos a `main`:

```powershell
git add .github/workflows/deploy-render.yml README.md
git commit -m "Configurar despliegue continuo en Render"
git push origin main
```

En GitHub, consulta **Actions > Validar y desplegar en Render**. Cuando el workflow
finalice, la API estara disponible en la URL `https://<nombre-del-servicio>.onrender.com`
y Swagger en `https://<nombre-del-servicio>.onrender.com/docs`.

> Render apaga los servicios gratuitos despues de un periodo sin trafico. La primera
> solicitud posterior puede tardar alrededor de un minuto mientras el servicio vuelve
> a iniciar. El sistema de archivos local del servicio gratuito es efimero.

## Solucion de problemas

- Si el puerto `8000` esta ocupado, cambia `"8000:8000"` en `docker-compose.yml` por otro puerto, por ejemplo `"8080:8000"`, y usa `http://localhost:8080`.
- Si modificas `requirements.txt` o `Dockerfile`, vuelve a construir con `docker compose up --build`.
