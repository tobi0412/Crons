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
    print(f"  🧮 Calculando precio para rating {rating}...")
    print(f"  📥 Valores recibidos: {all_prices_values}")
    
    if rating == 90:
        # Para rating 90: solo el primer elemento
        print(f"  ⚙️ Regla para rating 90: usar solo el primer elemento (índice 0)")
        if all_prices_values[0] is not None:
            print(f"  ✅ Valor encontrado: {all_prices_values[0]}")
            return all_prices_values[0]
        else:
            print(f"  ❌ Primer elemento es None")
            return None
            
    elif rating == 89:
        # Para rating 89: promedio de elementos 1-3 (índices 0-2)
        print(f"  ⚙️ Regla para rating 89: promedio de elementos 0-2 (primeros 3)")
        values_to_average = all_prices_values[0:3]
        print(f"  📊 Elementos para promediar: {values_to_average}")
        valid_values = [v for v in values_to_average if v is not None]
        print(f"  ✅ Valores válidos: {valid_values}")
        
        if valid_values and len(valid_values) > 0:
            average_price = sum(valid_values) / len(valid_values)
            print(f"  🧮 Promedio calculado: {average_price}")
            result = round(average_price)
            print(f"  💰 Resultado redondeado: {result}")
            return result
        else:
            print(f"  ❌ No hay valores válidos para promediar")
            return None
            
    else:
        # Para el resto: promedio de elementos 2-5 (índices 1-4, ignorando el primero)
        print(f"  ⚙️ Regla para rating {rating}: promedio de elementos 1-4 (ignorando el primero)")
        values_to_average = all_prices_values[1:5]
        print(f"  📊 Elementos para promediar: {values_to_average}")
        valid_values = [v for v in values_to_average if v is not None]
        print(f"  ✅ Valores válidos: {valid_values}")
        
        if valid_values and len(valid_values) > 0:
            average_price = sum(valid_values) / len(valid_values)
            print(f"  🧮 Promedio calculado: {average_price}")
            result = round(average_price)
            print(f"  💰 Resultado redondeado: {result}")
            return result
        else:
            print(f"  ❌ No hay valores válidos para promediar")
            return None

