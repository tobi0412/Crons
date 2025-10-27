#!/usr/bin/env python3
"""
Pipeline completo del scraper de FUTBIN
Ejecuta el scraper y envía las notificaciones
"""

import sys
import asyncio

def run_complete_pipeline():
    """
    Ejecuta el pipeline completo: scraper + notificaciones
    """
    print("=" * 60)
    print("INICIANDO PIPELINE COMPLETO")
    print("=" * 60)
    print()
    
    try:
        # Paso 1: Ejecutar el scraper
        from scraping.main import main as scraper_main
        
        print("[INFO] Ejecutando scraper...")
        print()
        
        result = asyncio.run(scraper_main())
        
        # Verificar si el scraper fue exitoso
        if not result:
            print()
            print("[ERROR] EL SCRAPER FALLO")
            print("=" * 60)
            return 1
        
        print()
        print("=" * 60)
        print("[OK] SCRAPER COMPLETADO")
        print("=" * 60)
        print()
        
        # Paso 2: Enviar notificaciones
        print("[INFO] Enviando notificaciones...")
        print()
        
        # Usar los resultados directamente del scraper (sin JSON)
        from send_scraper_notification import send_scraper_notification
        success = send_scraper_notification(result)
        
        if success:
            print()
            print("=" * 60)
            print("[OK] PIPELINE COMPLETADO EXITOSAMENTE")
            print("=" * 60)
            return 0
        else:
            print()
            print("=" * 60)
            print("[ERROR] FALLO EL ENVIO DE NOTIFICACIONES")
            print("=" * 60)
            return 1
            
    except KeyboardInterrupt:
        print("\n[INFO] Pipeline interrumpido por el usuario")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Error en el pipeline: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(run_complete_pipeline())
