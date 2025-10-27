#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar el scraper de FUTBIN
"""

import sys
import nodriver as uc

def run_scraper():
    """
    Función wrapper para ejecutar el scraper
    """
    try:
        uc.loop().run_until_complete(run_main())
    except KeyboardInterrupt:
        print("\n⚠️ Ejecución interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error al ejecutar el scraper: {e}")
        sys.exit(1)

async def run_main():
    """
    Importa y ejecuta el main del módulo scraping
    """
    from scraping.main import main
    await main()

if __name__ == "__main__":
    run_scraper()

