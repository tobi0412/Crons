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
        # Para rating 90: primer elemento (índice 0)
        print(f"  ⚙️ Regla para rating 90: usar el primer elemento (índice 0)")
        if len(all_prices_values) > 0 and all_prices_values[0] is not None:
            print(f"  ✅ Valor encontrado: {all_prices_values[0]}")
            return all_prices_values[0]
        else:
            print(f"  ❌ Primer elemento no disponible")
            return None
            
    elif rating == 89:
        # Para rating 89: tercer elemento (índice 2)
        print(f"  ⚙️ Regla para rating 89: usar el tercer elemento (índice 2)")
        if len(all_prices_values) > 2 and all_prices_values[2] is not None:
            print(f"  ✅ Valor encontrado: {all_prices_values[2]}")
            return all_prices_values[2]
        else:
            print(f"  ❌ Tercer elemento no disponible")
            return None
            
    elif rating == 88:
        # Para rating 88: cuarto elemento (índice 3)
        print(f"  ⚙️ Regla para rating 88: usar el cuarto elemento (índice 3)")
        if len(all_prices_values) > 3 and all_prices_values[3] is not None:
            print(f"  ✅ Valor encontrado: {all_prices_values[3]}")
            return all_prices_values[3]
        else:
            print(f"  ❌ Cuarto elemento no disponible")
            return None
            
    else:
        # Para el resto (83-87): quinto elemento (índice 4)
        print(f"  ⚙️ Regla para rating {rating}: usar el quinto elemento (índice 4)")
        if len(all_prices_values) > 4 and all_prices_values[4] is not None:
            print(f"  ✅ Valor encontrado: {all_prices_values[4]}")
            return all_prices_values[4]
        else:
            print(f"  ❌ Quinto elemento no disponible")
            return None

