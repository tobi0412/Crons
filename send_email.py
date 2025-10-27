#!/usr/bin/env python3
"""
Script para enviar emails usando SendGrid API
Este script se ejecuta desde GitHub Actions como parte del cron job diario
"""

import os
import sys
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_daily_email():
    """Envía un email diario con información de la ejecución del cron job"""
    
    # Obtener variables de entorno
    api_key = os.getenv('MAIL_API_KEY')
    email_from = os.getenv('EMAIL_FROM')
    email_to = os.getenv('EMAIL_TO')
    
    # Verificar que todas las variables estén configuradas
    if not all([api_key, email_from, email_to]):
        print("❌ Error: Faltan variables de entorno requeridas")
        print("Se necesitan: MAIL_API_KEY, EMAIL_FROM, EMAIL_TO")
        return False
    
    # Información de la ejecución
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    date_only = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Contenido del email
    subject = f"📧 Cron Job Diario - {date_only}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
            <h2 style="color: #333; margin-top: 0;">🚀 Cron Job Ejecutado</h2>
            
            <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <p><strong>📅 Fecha y Hora:</strong> {timestamp}</p>
                <p><strong>📧 Estado:</strong> ✅ Ejecutado correctamente</p>
                <p><strong>🔔 Repositorio:</strong> {os.getenv('GITHUB_REPOSITORY', 'N/A')}</p>
                <p><strong>👤 Usuario:</strong> {os.getenv('GITHUB_ACTOR', 'N/A')}</p>
                <p><strong>🔢 Commit:</strong> {os.getenv('GITHUB_SHA', 'N/A')[:8]}</p>
            </div>
            
            <div style="background-color: #e8f5e8; padding: 10px; border-radius: 5px; margin: 10px 0;">
                <p style="margin: 0; color: #2d5a2d;">
                    <strong>✅ El cron job se ejecutó exitosamente</strong><br>
                    Este email confirma que el proceso automatizado funcionó correctamente.
                </p>
            </div>
            
            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
                <p>Este es un email automático generado por GitHub Actions.</p>
                <p>Workflow: Daily Email Cron Job</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Cron Job Ejecutado - {date_only}
    
    📅 Fecha y Hora: {timestamp}
    📧 Estado: ✅ Ejecutado correctamente
    🔔 Repositorio: {os.getenv('GITHUB_REPOSITORY', 'N/A')}
    👤 Usuario: {os.getenv('GITHUB_ACTOR', 'N/A')}
    🔢 Commit: {os.getenv('GITHUB_SHA', 'N/A')[:8]}
    
    ✅ El cron job se ejecutó exitosamente
    Este email confirma que el proceso automatizado funcionó correctamente.
    
    ---
    Este es un email automático generado por GitHub Actions.
    Workflow: Daily Email Cron Job
    """
    
    try:
        # Crear el objeto Mail
        message = Mail(
            from_email=email_from,
            to_emails=email_to,
            subject=subject,
            html_content=html_content,
            plain_text_content=text_content
        )
        
        # Enviar el email
        sg = SendGridAPIClient(api_key=api_key)
        response = sg.send(message)
        
        print(f"✅ Email enviado exitosamente")
        print(f"📧 Destinatario: {email_to}")
        print(f"📅 Timestamp: {timestamp}")
        print(f"🔢 Status Code: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando envío de email diario...")
    
    success = send_daily_email()
    
    if success:
        print("✅ Proceso completado exitosamente")
        return 0
    else:
        print("❌ Proceso falló")
        return 1

if __name__ == "__main__":
    sys.exit(main())
