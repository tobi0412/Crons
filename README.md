# Crons

Este es un repositorio privado para gestionar tareas programadas (crons) usando GitHub Actions con envío de emails.

## Descripción

Este repositorio contiene un cron job configurado con GitHub Actions que se ejecuta una vez al día (9 AM UTC) y envía un email de confirmación usando SendGrid.

## GitHub Actions

### Cron Job Diario con Email

El workflow se encuentra en `.github/workflows/cron-test.yml` y realiza las siguientes acciones:

- ✅ Se ejecuta una vez al día a las 9 AM UTC (`0 9 * * *`)
- ✅ Envía un email de confirmación usando SendGrid API
- ✅ Muestra información del sistema y del repositorio
- ✅ Genera logs de cada ejecución
- ✅ Se puede ejecutar manualmente desde GitHub Actions

### Configuración de GitHub Secrets

Para que el cron job funcione correctamente, necesitas configurar los siguientes secrets en tu repositorio de GitHub:

1. Ve a tu repositorio en GitHub
2. Haz clic en **Settings** → **Secrets and variables** → **Actions**
3. Haz clic en **New repository secret** y agrega:

#### Secrets Requeridos:

- **`MAIL_API_KEY`**: Tu API key de SendGrid
  - Obtén tu API key desde [SendGrid Dashboard](https://app.sendgrid.com/settings/api_keys)
  
- **`EMAIL_FROM`**: Email del remitente
  - Debe estar verificado en SendGrid
  - Ejemplo: `noreply@tudominio.com`
  
- **`EMAIL_TO`**: Email del destinatario
  - Ejemplo: `tu-email@gmail.com`

### Ejecutar manualmente

1. Ve a la pestaña **Actions** en tu repositorio de GitHub
2. Selecciona el workflow "Daily Email Cron Job"
3. Haz clic en **Run workflow** → **Run workflow**

## Scripts locales

También puedes ejecutar los scripts localmente para probar:

```bash
# Ejecutar script en bash (Linux/Mac)
bash test-cron.sh

# Ejecutar script en Python
python3 test-cron.py

# Ejecutar script de email (requiere variables de entorno)
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
2. El workflow se ejecutará automáticamente cada día a las 9 AM UTC
3. Haz clic en "Run workflow" para ejecutarlo manualmente y probar
4. Revisa los logs para confirmar que el email se envió correctamente

## Contribución

Este es un repositorio privado.

## Licencia

Privado - Todos los derechos reservados.
