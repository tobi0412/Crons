# FUTBIN Price Scraper

Scraper automático para obtener los precios más baratos de jugadores en FUTBIN con notificaciones por ntfy y almacenamiento en Supabase.

## Descripción

Este proyecto ejecuta un scraper que obtiene los precios de los jugadores más baratos de FUTBIN para los ratings 83-90, y:
- Envía notificaciones por ntfy
- Almacena los datos en Supabase
- Se ejecuta automáticamente cada hora

## Configuración

### 1. Secrets de GitHub Actions

Configura estos secrets en tu repositorio:

1. Ve a tu repositorio → **Settings** → **Secrets and variables** → **Actions**
2. Agrega los siguientes secrets:

- **`NTFY_TOPIC`**: Tu tópico de ntfy (ej: `8gCrkggZioO7OWrr`)
- **`SUPABASE_URL`**: URL de tu proyecto Supabase (ej: `https://xxxxx.supabase.co`)
- **`SUPABASE_KEY`**: Tu API Key anon/public de Supabase

### 2. Configurar Supabase

1. Crea una cuenta en [supabase.com](https://supabase.com)
2. Crea un nuevo proyecto
3. Ejecuta el SQL que está en `SUPABASE_SETUP.md` para crear la tabla
4. Copia tu URL y API Key a los secrets de GitHub

### 3. Para desarrollo local

Crea un archivo `.env` con:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-supabase-anon-key
NTFY_TOPIC=tu_topico_de_ntfy
```

## Ejecutar localmente

```bash
# Instalar dependencias
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# Ejecutar el pipeline completo
python run_pipeline.py
```

## GitHub Actions

El workflow se encuentra en `.github/workflows/scraper.yml` y:

- ✅ Se ejecuta cada hora automáticamente
- ✅ Ejecuta el scraper de FUTBIN
- ✅ Guarda los precios en Supabase
- ✅ Envía notificaciones por ntfy
- ✅ Se puede ejecutar manualmente desde GitHub Actions

### Cron Schedule

```yaml
schedule:
  - cron: '0 * * * *'  # Cada hora a los 0 minutos
```

## Estructura del proyecto

```
.
├── run_pipeline.py           # Pipeline completo (scraper + BD + notificaciones)
├── database/                 # Módulo de base de datos
│   ├── __init__.py
│   └── database.py           # Manejo de Supabase
├── notifications/            # Módulo de notificaciones
│   ├── __init__.py
│   └── notifications.py      # Envío de notificaciones por ntfy
├── scraping/                 # Módulo de scraping
│   ├── __init__.py
│   ├── main.py               # Función principal del scraper
│   ├── scraper.py            # Scraping con Playwright
│   ├── price_extractor.py    # Extracción de precios
│   └── ratings_processor.py  # Procesamiento de ratings
└── .github/workflows/
    └── scraper.yml           # Workflow de GitHub Actions
```

## Ventajas de Supabase

- ✅ Dashboard visual para ver gráficos de precios
- ✅ API REST automática para consultar datos
- ✅ No genera commits en el repositorio
- ✅ Escala mejor con más datos
- ✅ Plan gratuito generoso (500MB de BD)
- ✅ Permite análisis avanzados de tendencias de precios

## Ver logs

1. Ve a la pestaña **Actions** en tu repositorio
2. Selecciona la ejecución más reciente
3. Revisa los logs del workflow

## Notificaciones

Para recibir notificaciones:

1. Descarga la app **ntfy** desde [ntfy.sh/app](https://ntfy.sh/app)
2. Suscríbete al tópico que configuraste en `NTFY_TOPIC`
3. Recibirás notificaciones cada hora con los precios actualizados

## Licencia

Privado - Todos los derechos reservados.
