"""
Módulo principal de scraping para FUTBIN
"""

from playwright.async_api import async_playwright
import asyncio
import re
from .price_extractor import extract_price_value
from .ratings_processor import calculate_price_for_rating


async def scrape_futbin_cheapest(headless=True):
    """
    Scrapea la página de jugadores más baratos de FUTBIN usando Playwright
    
    Args:
        headless (bool): Si ejecutar el navegador en modo headless (sin ventana visible)
    
    Returns:
        list: Lista de 8 valores de precios [rating83, rating84, ..., rating90]
    """
    try:
        print("🔄 Iniciando navegador...")
        async with async_playwright() as p:
            # Configuración más robusta del navegador
            browser = await p.chromium.launch(
                headless=headless,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            # Crear contexto con configuración de timeout más larga
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            
            # Configurar timeouts más largos
            page.set_default_timeout(60000)  # 60 segundos
            page.set_default_navigation_timeout(60000)  # 60 segundos
            
            print("🌐 Navegando a futbin.com...")
            try:
                await page.goto("https://www.futbin.com", wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(3)
            except Exception as e:
                print(f"⚠️ Error al cargar futbin.com: {e}")
                print("🔄 Intentando con timeout más corto...")
                await page.goto("https://www.futbin.com", timeout=30000)
                await asyncio.sleep(2)
            
            # Navegar a la página específica
            print("🔗 Navegando a la página de jugadores más baratos...")
            try:
                await page.goto("https://www.futbin.com/squad-building-challenges/cheapest", wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(5)  # Esperar más tiempo para que cargue completamente
            except Exception as e:
                print(f"⚠️ Error al cargar la página de cheapest: {e}")
                print("🔄 Intentando con timeout más corto...")
                await page.goto("https://www.futbin.com/squad-building-challenges/cheapest", timeout=30000)
                await asyncio.sleep(3)
            
            # Selector específico para el player column not ps
            selector = ".stc-player-column.xs-column.hide-not-ps"
            
            # Ratings a buscar: 83, 84, 85, 86, 87, 88, 89, 90
            ratings = [83, 84, 85, 86, 87, 88, 89, 90]
            
            print(f"🔍 Buscando player column not ps para ratings {ratings}...")
            print(f"Selector: {selector}")
            
            # Verificar que la página cargó correctamente
            try:
                page_title = await page.title()
                print(f"📄 Título de la página: {page_title}")
                
                # Esperar un poco más para asegurar que el contenido dinámico se carga
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"⚠️ Error al verificar la página: {e}")
            
            try:
                # Buscar todos los elementos con ese selector
                print("🔍 Buscando elementos con el selector específico...")
                elements = await page.query_selector_all(selector)
                
                if elements and len(elements) > 0:
                    print(f"✅ Se encontraron {len(elements)} elementos con ese selector")
                    
                    # Lista para almacenar resultados (8 valores)
                    all_results = []
                    
                    # Iterar sobre cada rating
                    for rating in ratings:
                        print(f"\n{'='*70}")
                        print(f"🔍 PROCESANDO RATING {rating}")
                        print(f"{'='*70}")
                        
                        # Buscar el elemento que contiene el texto del rating
                        target_element = None
                        for idx, element in enumerate(elements):
                            try:
                                text = await element.text_content()
                                if text:
                                    # Usar word boundary para buscar rating exacto, no parcial
                                    # Buscar el rating como palabra completa o como inicio de línea
                                    text_cleaned = text.strip()
                                    
                                    # Patrón para encontrar el rating exacto: "\b83\b" o "83 " o "83\n"
                                    # pero no "835" o "183"
                                    rating_pattern = rf'\b{rating}\b'
                                    
                                    if re.search(rating_pattern, text_cleaned):
                                        target_element = element
                                        print(f"✅ Encontrado elemento #{idx+1} con rating {rating}")
                                        print(f"   Texto del elemento: {text_cleaned[:200]}...")  # Primeros 200 chars
                                        break
                                    
                                    # Debugging: mostrar todos los elementos para identificar el patrón
                                    if idx < 5:  # Solo mostrar los primeros 5 para no saturar
                                        print(f"   Elemento #{idx+1}: {text_cleaned[:100]}")
                            except Exception as e:
                                print(f"   ⚠️ Error al leer elemento #{idx+1}: {e}")
                                continue
                        
                        if target_element:
                            # Buscar TODAS las apariciones de platform-price-wrapper-small
                            print(f"🔍 Buscando 'platform-price-wrapper-small' dentro del elemento de rating {rating}...")
                            
                            # Buscar dentro de target_element - obtener TODOS los elementos
                            inner_selector = ".platform-price-wrapper-small"
                            price_wrappers = await target_element.query_selector_all(inner_selector)
                            
                            if price_wrappers and len(price_wrappers) > 0:
                                print(f"✅ Se encontraron {len(price_wrappers)} elementos 'platform-price-wrapper-small' para rating {rating}")
                                
                                # Extraer texto y valores de los primeros 5 elementos
                                all_prices_text = []
                                all_prices_values = []
                                
                                print(f"\n📋 Precios encontrados para rating {rating}:")
                                print(f"{'─'*70}")
                                
                                for i, wrapper in enumerate(price_wrappers[:5], 1):
                                    try:
                                        price_text = await wrapper.text_content()
                                        if price_text:
                                            price_text = price_text.strip()
                                        all_prices_text.append(price_text)
                                        
                                        # Extraer valor numérico
                                        value = extract_price_value(price_text)
                                        all_prices_values.append(value)
                                        
                                        # IMPRIMIR CADA PRECIO ENCONTRADO
                                        print(f"  Precio #{i}:")
                                        print(f"    Texto original: '{price_text}'")
                                        print(f"    Valor extraído: {value}")
                                        
                                    except Exception as e:
                                        all_prices_values.append(None)
                                        print(f"  Precio #{i}: ERROR - {e}")
                                
                                # Mostrar todos los valores antes del cálculo
                                print(f"\n  📊 Valores antes del cálculo: {all_prices_values}")
                                
                                # Calcular precio según reglas del rating
                                result_price = calculate_price_for_rating(rating, all_prices_values)
                                print(f"  ✅ Precio final calculado: {result_price}")
                                print(f"{'─'*70}")
                                
                                all_results.append(result_price)
                            else:
                                print(f"❌ No se encontró ningún elemento 'platform-price-wrapper-small' para rating {rating}")
                                all_results.append(None)
                        else:
                            print(f"❌ No se encontró ningún elemento con rating {rating}")
                            all_results.append(None)
                    
                    # Retornar todos los resultados
                    print(f"\n{'='*70}")
                    print(f"📊 RESUMEN DE RESULTADOS")
                    print(f"{'='*70}")
                    for i, (rating, price) in enumerate(zip(ratings, all_results)):
                        if price is not None:
                            print(f"Rating {rating}: Precio = {price} coins")
                        else:
                            print(f"Rating {rating}: No se pudo calcular el precio")
                    
                    return all_results
                else:
                    print("❌ No se encontró ningún elemento con el selector especificado")
                    
                    # Debugging adicional
                    print("🔍 Intentando buscar selectores alternativos...")
                    try:
                        # Buscar elementos similares
                        alt_selectors = [
                            ".stc-player-column",
                            ".player-column",
                            ".xs-column",
                            "[class*='player']",
                            "[class*='stc']"
                        ]
                        
                        for alt_selector in alt_selectors:
                            alt_elements = await page.query_selector_all(alt_selector)
                            if alt_elements:
                                print(f"🔍 Selector alternativo '{alt_selector}' encontró {len(alt_elements)} elementos")
                        
                        # Buscar cualquier elemento que contenga "rating" o números
                        rating_elements = await page.query_selector_all("[class*='rating'], [class*='83'], [class*='84'], [class*='85']")
                        if rating_elements:
                            print(f"🔍 Elementos relacionados con ratings: {len(rating_elements)}")
                            
                    except Exception as debug_e:
                        print(f"⚠️ Error en debugging: {debug_e}")
                    
                    return None
                    
            except Exception as e:
                print(f"❌ Error al buscar el elemento: {e}")
                return None
            
    except Exception as e:
        print(f"❌ Error general: {e}")
        return None