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
    # Primero buscar si hay un número seguido de 'k' o 'K'
    k_pattern = re.search(r'(\d+(?:[.,]\d+)?)\s*[kK]', text)
    if k_pattern:
        value_str = k_pattern.group(1)
        try:
            # Si tiene punto o coma, es decimal: 15.5k = 15500
            if '.' in value_str or ',' in value_str:
                value_float = float(value_str.replace(',', '.'))
                return int(value_float * 1000)
            else:
                # Si es entero: 15k = 15000
                return int(value_str) * 1000
        except:
            return None
    
    # Si no hay 'k', buscar números normales
    # Buscar números con formato de miles (ej: 1,500, 1.500, 1500)
    numbers = re.findall(r'(\d{1,3}(?:[.,]\d{3})+)', text)
    if not numbers:
        # Si no encuentra formato de miles, buscar cualquier número
        numbers = re.findall(r'\d+', text)
    
    if numbers:
        # Tomar el primer número encontrado y limpiar separadores de miles
        value = numbers[0].replace(',', '').replace('.', '')
        try:
            return int(value)
        except:
            return None
    return None

