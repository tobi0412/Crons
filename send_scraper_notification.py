#!/usr/bin/env python3
"""
Script para enviar notificaciones con los resultados del scraper
"""

import os
import json
import sys
import datetime
import requests

def format_prices(prices_dict):
    """
    Formatea los precios para mostrar en la notificación
    
    Args:
        prices_dict (dict): Diccionario con {rating: precio}
        
    Returns:
        str: Texto formateado con los precios
    """
    if not prices_dict:
        return "❌ No se pudieron obtener precios"
    
    text = "💰 Precios FUTBIN:\n\n"
    
    for rating in [83, 84, 85, 86, 87, 88, 89, 90]:
        price = prices_dict.get(rating)
        if price is not None:
            # Formatear con separadores de miles
            formatted_price = f"{price:,}".replace(",", ".")
            text += f"🔸 Rating {rating}: {formatted_price} coins\n"
        else:
            text += f"🔸 Rating {rating}: N/A\n"
    
    return text

def send_scraper_notification(prices_dict):
    """
    Envía una notificación con los resultados del scraper
    
    Args:
        prices_dict (dict): Diccionario con los precios por rating
    """
    
    # Obtener variables de entorno
    ntfy_topic = os.getenv('NTFY_TOPIC')
    
    # Verificar que el tópico esté configurado
    if not ntfy_topic:
        print("⚠️ NTFY_TOPIC no está configurado, no se enviará notificación")
        return False
    
    # Información de la ejecución
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # Contenido de la notificación
    title = "⚽ FUTBIN - Precios Actualizados"
    
    message = f"""⏰ {timestamp}

{format_prices(prices_dict)}

✅ Scraper completado exitosamente"""
    
    try:
        # URL de la API de ntfy
        url = f"https://ntfy.sh/{ntfy_topic}"
        
        # Headers para la notificación
        headers = {
            "Title": title,
            "Priority": "default",
            "Tags": "soccer,soccer_ball",
            "Content-Type": "text/plain; charset=utf-8"
        }
        
        # Enviar la notificación
        # Codificar el mensaje explícitamente como UTF-8 para soportar emojis
        response = requests.post(url, data=message.encode('utf-8'), headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Notificación enviada exitosamente")
            print(f"📱 Tópico: {ntfy_topic}")
            return True
        else:
            print(f"❌ Error al enviar notificación: Status {response.status_code}")
            return False
        
    except Exception as e:
        print(f"❌ Error al enviar notificación: {str(e)}")
        return False

def main():
    """Función principal"""
    
    # Verificar si existe el archivo de resultados
    results_file = 'scraping_results.json'
    
    if not os.path.exists(results_file):
        print(f"⚠️ No se encontró el archivo {results_file}")
        print("💡 El scraper debería ejecutarse primero para generar este archivo")
        return 0
    
    # Leer los resultados del scraper
    try:
        with open(results_file, 'r') as f:
            prices_dict = json.load(f)
    except Exception as e:
        print(f"❌ Error al leer {results_file}: {e}")
        return 1
    
    # Enviar la notificación
    success = send_scraper_notification(prices_dict)
    
    if success:
        print("✅ Proceso completado exitosamente")
        return 0
    else:
        print("❌ Proceso falló")
        return 1

if __name__ == "__main__":
    sys.exit(main())

