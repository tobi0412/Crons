# Crons

Este es un repositorio privado para gestionar tareas programadas (crons) usando GitHub Actions con notificaciones ntfy.

## Descripción

Este repositorio contiene un cron job configurado con GitHub Actions que se ejecuta una vez al día (3 PM UTC) y envía una notificación de confirmación usando ntfy.

## GitHub Actions

### Cron Job Diario con Notificaciones

El workflow se encuentra en `.github/workflows/cron-test.yml` y realiza las siguientes acciones:

- ✅ Se ejecuta una vez al día a las 3 PM UTC (`0 15 * * *`)
- ✅ Envía una notificación de confirmación usando ntfy API
- ✅ Muestra información del sistema y del repositorio
- ✅ Genera logs de cada ejecución
- ✅ Se puede ejecutar manualmente desde GitHub Actions

### Configuración de GitHub Secrets

Para que el cron job funcione correctamente, necesitas configurar los siguientes secrets en tu repositorio de GitHub:

1. Ve a tu repositorio en GitHub
2. Haz clic en **Settings** → **Secrets and variables** → **Actions**
3. Haz clic en **New repository secret** y agrega:

#### Secrets Requeridos:

- **`NTFY_TOPIC`**: Tu tópico personalizado de ntfy
  - Ve a [ntfy.sh](https://ntfy.sh) y crea un tópico personalizado
  - Ejemplo: `mi-cron-job` (se convertirá en `https://ntfy.sh/mi-cron-job`)
  - Puedes usar cualquier nombre que quieras, pero evita espacios y caracteres especiales

### Ejecutar manualmente

1. Ve a la pestaña **Actions** en tu repositorio de GitHub
2. Selecciona el workflow "Daily Email Cron Job"
3. Haz clic en **Run workflow** → **Run workflow**

## Configuración de ntfy

Para recibir las notificaciones en tu dispositivo:

1. **Descarga la app ntfy** desde [ntfy.sh/app](https://ntfy.sh/app)
2. **Suscríbete a tu tópico** usando el mismo nombre que configuraste en `NTFY_TOPIC`
3. **Recibirás notificaciones** cada vez que se ejecute el cron job

## Scripts locales

También puedes ejecutar los scripts localmente para probar:

```bash
# Ejecutar script en bash (Linux/Mac)
bash test-cron.sh

# Ejecutar script en Python
python3 test-cron.py

# Ejecutar script de notificación (requiere variables de entorno)
export NTFY_TOPIC="mi-cron-job"
python3 send_notification.py

# Ejecutar script de email (requiere variables de entorno) - OPCIONAL
export MAIL_API_KEY="tu_api_key"
export EMAIL_FROM="tu_email@dominio.com"
export EMAIL_TO="destinatario@email.com"
python3 send_email.py
```

## Uso

### Configuración de GitHub Actions

1. Inicializar Git (si no lo has hecho):
```bash
git init
```

2. Agregar archivos:
```bash
git add .
```

3. Hacer commit:
```bash
git commit -m "feat: Add daily email cron job with SendGrid integration"
```

4. Subir a GitHub:
```bash
# Crear el repositorio en GitHub y luego:
git remote add origin https://github.com/TU_USUARIO/Crons.git
git branch -M main
git push -u origin main
```

### Verificar que funciona

Una vez configurados los secrets y subido a GitHub:
1. Ve a la pestaña **Actions**
2. El workflow se ejecutará automáticamente cada día a las 3 PM UTC
3. Haz clic en "Run workflow" para ejecutarlo manualmente y probar
4. Revisa los logs para confirmar que la notificación se envió correctamente
5. Verifica que recibiste la notificación en tu dispositivo con la app ntfy

## Contribución

Este es un repositorio privado.

## Licencia

Privado - Todos los derechos reservados.
