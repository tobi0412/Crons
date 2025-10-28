#!/usr/bin/env python3
"""
Módulo para manejar la base de datos Supabase que almacena los precios de FUTBIN
"""

import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_supabase_client() -> Client:
    """
    Obtiene el cliente de Supabase
    
    Returns:
        Client: Cliente de Supabase configurado
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar configurados")
    
    return create_client(supabase_url, supabase_key)

def init_database():
    """
    Inicializa la tabla en Supabase (se ejecuta automáticamente si la tabla no existe)
    No es necesario para Supabase, pero mantiene la interfaz compatible
    """
    try:
        client = get_supabase_client()
        # Supabase crea la tabla automáticamente o se debe crear desde el dashboard
        print("[INFO] Conectado a Supabase")
        return True
    except Exception as e:
        print(f"[ERROR] Error al conectar con Supabase: {e}")
        return False

def save_prices(prices_dict):
    """
    Guarda los precios en Supabase usando el esquema de dos tablas
    
    Args:
        prices_dict (dict): Diccionario con {rating: precio}
        
    Returns:
        bool: True si se guardaron correctamente, False en caso contrario
    """
    try:
        client = get_supabase_client()
        
        # Obtener timestamp actual
        timestamp = datetime.now().isoformat()
        
        # Preparar datos para insertar en pricehistory
        records = []
        for rating, price in prices_dict.items():
            if price is not None:
                records.append({
                    "rating": rating,
                    "timestamp": timestamp,
                    "price": price
                })
        
        if not records:
            print("[ADVERTENCIA] No hay datos para guardar")
            return False
        
        # Insertar todos los registros en pricehistory
        response = client.table("pricehistory").insert(records).execute()
        
        print(f"[OK] Precios guardados en Supabase ({len(records)} registros)")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error al guardar precios en Supabase: {e}")
        return False

def get_latest_prices():
    """
    Obtiene los precios más recientes de Supabase usando el esquema de dos tablas
    
    Returns:
        dict: Diccionario con {rating: precio} o None si hay error
    """
    try:
        client = get_supabase_client()
        
        # Obtener el timestamp más reciente
        max_timestamp_response = client.table("pricehistory").select("timestamp").order("timestamp", desc=True).limit(1).execute()
        
        if not max_timestamp_response.data:
            return None
        
        latest_timestamp = max_timestamp_response.data[0]["timestamp"]
        
        # Obtener todos los precios de ese timestamp
        prices_response = client.table("pricehistory").select("rating,price").eq("timestamp", latest_timestamp).order("rating").execute()
        
        prices_dict = {}
        for row in prices_response.data:
            prices_dict[row["rating"]] = row["price"]
        
        return prices_dict
        
    except Exception as e:
        print(f"[ERROR] Error al leer precios de Supabase: {e}")
        return None

def get_price_history(rating, limit=10):
    """
    Obtiene el historial de precios para un rating específico usando el esquema de dos tablas
    
    Args:
        rating (int): El rating del que se quiere obtener el historial
        limit (int): Número máximo de registros a obtener
        
    Returns:
        list: Lista de tuplas (timestamp, price) o None si hay error
    """
    try:
        client = get_supabase_client()
        
        response = client.table("pricehistory").select("timestamp,price").eq("rating", rating).order("timestamp", desc=True).limit(limit).execute()
        
        history = [(row["timestamp"], row["price"]) for row in response.data]
        
        return history
        
    except Exception as e:
        print(f"[ERROR] Error al obtener historial: {e}")
        return None
