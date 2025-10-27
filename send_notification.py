#!/usr/bin/env python3
"""
Script para enviar notificaciones usando ntfy API
Este script se ejecuta desde GitHub Actions como parte del cron job diario
"""

import os
import sys
import datetime
import requests

def send_daily_notification():
    """Envía una notificación diaria con información de la ejecución del cron job"""
    
    # Obtener variables de entorno
    ntfy_topic = os.getenv('NTFY_TOPIC')
    
    # Verificar que el tópico esté configurado
    if not ntfy_topic:
        print("❌ Error: Falta variable de entorno requerida")
        print("Se necesita: NTFY_TOPIC")
        return False
    
    # Información de la ejecución
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    date_only = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Contenido de la notificación
    title = "Cron Job Ejecutado"
    
    message = f"""📅 {timestamp}
🔔 Repositorio: {os.getenv('GITHUB_REPOSITORY', 'N/A')}
👤 Usuario: {os.getenv('GITHUB_ACTOR', 'N/A')}
🔢 Commit: {os.getenv('GITHUB_SHA', 'N/A')[:8]}

✅ El cron job se ejecutó exitosamente"""
    
    try:
        # URL de la API de ntfy
        url = f"https://ntfy.sh/{ntfy_topic}"
        
        # Headers para la notificación
        headers = {
            "Title": title,
            "Priority": "default",
            "Tags": "white_check_mark"
        }
        
        # Enviar la notificación
        response = requests.post(url, data=message, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Notificación enviada exitosamente")
            print(f"📱 Tópico: {ntfy_topic}")
            print(f"📅 Timestamp: {timestamp}")
            print(f"🔢 Status Code: {response.status_code}")
            return True
        else:
            print(f"❌ Error al enviar notificación: Status {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
        
    except Exception as e:
        print(f"❌ Error al enviar notificación: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando envío de notificación diaria...")
    
    success = send_daily_notification()
    
    if success:
        print("✅ Proceso completado exitosamente")
        return 0
    else:
        print("❌ Proceso falló")
        return 1

if __name__ == "__main__":
    sys.exit(main())
