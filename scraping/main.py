#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal para ejecutar el scraper de FUTBIN
"""

import sys
import json
import asyncio
from .scraper import scrape_futbin_cheapest


async def main():
    """
    Función principal asíncrona
    """
    print("🚀 Iniciando scraper de FUTBIN con Playwright")
    print("=" * 50)
    
    results = await scrape_futbin_cheapest()
    
    if results:
        print("\n✅ Scraping completado exitosamente")
        
        # Mostrar resumen de lo obtenido
        if isinstance(results, list):
            print("\n📊 RESUMEN FINAL:")
            print("=" * 50)
            ratings = [83, 84, 85, 86, 87, 88, 89, 90]
            
            # Preparar diccionario para guardar
            results_dict = {}
            for rating, price in zip(ratings, results):
                if price is not None:
                    print(f"Rating {rating}: Precio = {price} monedas")
                    results_dict[rating] = price
                else:
                    print(f"Rating {rating}: Sin datos disponibles")
                    results_dict[rating] = None
            
            # Retornar los resultados directamente (sin guardar en archivo)
            return results_dict
    else:
        print("\n❌ El scraping no pudo completarse")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

