"""
Módulo para procesar los valores extraídos según el rating
"""


def calculate_price_for_rating(rating, all_prices_values):
    """
    Calcula el precio resultante según las reglas específicas del rating
    
    Args:
        rating (int): El rating a procesar
        all_prices_values (list): Lista de valores extraídos
        
    Returns:
        int: Precio calculado, None si no se pudo calcular
    """
    if rating == 90:
        # Para rating 90: solo el primer elemento
        if all_prices_values[0] is not None:
            return all_prices_values[0]
        else:
            return None
            
    elif rating == 89:
        # Para rating 89: promedio de elementos 1-3 (índices 0-2)
        values_to_average = all_prices_values[0:3]
        valid_values = [v for v in values_to_average if v is not None]
        
        if valid_values and len(valid_values) > 0:
            average_price = sum(valid_values) / len(valid_values)
            return round(average_price)
        else:
            return None
            
    else:
        # Para el resto: promedio de elementos 2-5 (índices 1-4, ignorando el primero)
        values_to_average = all_prices_values[1:5]
        valid_values = [v for v in values_to_average if v is not None]
        
        if valid_values and len(valid_values) > 0:
            average_price = sum(valid_values) / len(valid_values)
            return round(average_price)
        else:
            return None

