"""
Módulo para extraer valores numéricos de precios en diferentes formatos
"""

import re


def extract_price_value(text):
    """
    Extrae un valor numérico del texto (típicamente un precio en coins)
    Maneja valores con 'k' (ej: 15k = 15000, 15.5k = 15500)
    
    Args:
        text (str): Texto que contiene el precio
        
    Returns:
        int: Valor numérico extraído, None si no se puede extraer
    """
    if not text or not isinstance(text, str):
        print(f"    ⚠️ Texto inválido para extraer: {text}")
        return None
    
    # Primero buscar si hay un número seguido de 'k' o 'K'
    k_pattern = re.search(r'(\d+(?:[.,]\d+)?)\s*[kK]', text)
    if k_pattern:
        value_str = k_pattern.group(1)
        try:
            # Si tiene punto o coma, es decimal: 15.5k = 15500
            if '.' in value_str or ',' in value_str:
                value_float = float(value_str.replace(',', '.'))
                result = int(value_float * 1000)
                print(f"    ✓ Extraído con formato 'k' decimal: {value_str}k = {result}")
                return result
            else:
                # Si es entero: 15k = 15000
                result = int(value_str) * 1000
                print(f"    ✓ Extraído con formato 'k' entero: {value_str}k = {result}")
                return result
        except Exception as e:
            print(f"    ⚠️ Error al convertir valor con 'k': {e}")
            return None
    
    # Si no hay 'k', buscar números normales
    # Buscar números con formato de miles (ej: 1,500, 1.500, 1500)
    numbers = re.findall(r'(\d{1,3}(?:[.,]\d{3})+)', text)
    if not numbers:
        # Si no encuentra formato de miles, buscar cualquier número
        numbers = re.findall(r'\d+', text)
    
    if numbers:
        # Tomar el primer número encontrado y limpiar separadores de miles
        original_number = numbers[0]
        value = original_number.replace(',', '').replace('.', '')
        try:
            result = int(value)
            print(f"    ✓ Extraído como número normal: '{original_number}' = {result}")
            return result
        except Exception as e:
            print(f"    ⚠️ Error al convertir número: {e}")
            return None
    
    print(f"    ❌ No se pudo extraer ningún valor de: '{text}'")
    return None

