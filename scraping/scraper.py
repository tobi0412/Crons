"""
Módulo principal de scraping para FUTBIN
"""

import os
import nodriver as uc
import asyncio
from .price_extractor import extract_price_value
from .ratings_processor import calculate_price_for_rating


async def scrape_futbin_cheapest():
    """
    Scrapea la página de jugadores más baratos de FUTBIN usando nodriver
    
    Returns:
        list: Lista de 8 valores de precios [rating83, rating84, ..., rating90]
    """
    browser = None
    try:
        print("🔄 Iniciando navegador...")
        
        try:
            # Configuración específica para CI/GitHub Actions
            is_ci = os.getenv('CI') == 'true'
            
            if is_ci:
                print("🤖 Modo CI detectado - configurando para GitHub Actions...")
                
                # Configuración para nodriver en CI
                config = uc.Config(
                    browser_executable_path='/usr/bin/chromium-browser',
                    headless=True,
                    browser_args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--disable-software-rasterizer',
                        '--disable-extensions',
                        '--disable-setuid-sandbox',
                        '--single-process',
                        '--no-zygote',
                    ]
                )
                browser = await uc.start(config=config)
            else:
                print("🤖 Iniciando navegador en modo headless...")
                browser = await uc.start(headless=True)
                
        except Exception as init_error:
            print(f"❌ Error al inicializar el navegador: {init_error}")
            print(f"   Tipo: {type(init_error).__name__}")
            import traceback
            traceback.print_exc()
            return None
        
        # Verificar que el navegador se inicializó
        if browser is None:
            print("❌ Error: No se pudo inicializar el navegador (browser es None)")
            print("   Verifica que Chrome/Chromium esté instalado")
            return None
        
        print(f"✅ Navegador inicializado: {type(browser)}")
        
        print("🌐 Navegando a futbin.com...")
        start_page = await browser.get("https://www.futbin.com")
        await asyncio.sleep(2)
        
        # Navegar a la página específica
        print("🔗 Navegando a la página de jugadores más baratos...")
        cheapest_page = await browser.get("https://www.futbin.com/squad-building-challenges/cheapest")
        await asyncio.sleep(3)
        
        # Selector específico para el player column not ps
        selector = ".stc-player-column.xs-column.hide-not-ps"
        
        # Ratings a buscar: 83, 84, 85, 86, 87, 88, 89, 90
        ratings = [83, 84, 85, 86, 87, 88, 89, 90]
        
        print(f"🔍 Buscando player column not ps para ratings {ratings}...")
        print(f"Selector: {selector}")
        
        try:
            # Buscar todos los elementos con ese selector
            elements = await cheapest_page.select_all(selector)
            
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
                    for element in elements:
                        try:
                            text = element.text.strip()
                            if str(rating) in text:
                                target_element = element
                                print(f"✅ Encontrado elemento con rating {rating}")
                                break
                        except:
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
                            
                            for i, wrapper in enumerate(price_wrappers[:5], 1):
                                try:
                                    price_text = wrapper.text
                                    all_prices_text.append(price_text)
                                    
                                    # Extraer valor numérico
                                    value = extract_price_value(price_text)
                                    all_prices_values.append(value)
                                    
                                except Exception as e:
                                    all_prices_values.append(None)
                            
                            # Calcular precio según reglas del rating
                            result_price = calculate_price_for_rating(rating, all_prices_values)
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
                return None
                
        except Exception as e:
            print(f"❌ Error al buscar el elemento: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if browser is not None:
            try:
                print("🔒 Cerrando navegador...")
                # Verificar si browser tiene método stop y es awaitable
                if hasattr(browser, 'stop'):
                    stop_method = browser.stop
                    # Verificar si es coroutine
                    import inspect
                    if inspect.iscoroutinefunction(stop_method):
                        await stop_method()
                    else:
                        stop_method()
                print("✅ Navegador cerrado")
            except Exception as close_error:
                print(f"⚠️ Error al cerrar navegador: {close_error}")
                pass
            