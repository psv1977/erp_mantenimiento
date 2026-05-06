import sqlite3
import pandas as pd

def crear_tabla():
    """Crea las tablas de activos y AMEF si no existen."""
    conn = sqlite3.connect("confiabilidad.db")
    cursor = conn.cursor()
    
    # Tabla 1: Activos (AHORA CON JERARQUÍA DE SISTEMA)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sistema TEXT NOT NULL,
            tag TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            frecuencia INTEGER,
            consecuencia INTEGER,
            criticidad INTEGER,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla 2: AMEF (Relacionada a los activos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS amef (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_activo TEXT NOT NULL,
            funcion TEXT NOT NULL,
            falla_funcional TEXT NOT NULL,
            modo_falla TEXT NOT NULL,
            efecto TEXT NOT NULL,
            FOREIGN KEY (tag_activo) REFERENCES activos(tag)
        )
    """)
    
    conn.commit()
    conn.close()

def guardar_activo(sistema, tag, nombre, frec_falla, cons_falla):
    # 1. El motor calcula la criticidad por su cuenta (¡no hay que pedirla en app.py!)
    criticidad = frec_falla * cons_falla
    
    # 2. Se conecta a la base de datos
    conn = sqlite3.connect("confiabilidad.db")
    cursor = conn.cursor()
    
    # 3. Guarda los 6 datos (Fíjate que hay 6 signos de interrogación)
    cursor.execute("""
        INSERT INTO activos (sistema, tag, nombre, frecuencia, consecuencia, criticidad)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (sistema, tag, nombre, frec_falla, cons_falla, criticidad))
    
    conn.commit()
    conn.close()

def cargar_activos():
    """Retorna todos los activos registrados como DataFrame."""
    conn = sqlite3.connect("confiabilidad.db")
    df = pd.read_sql_query("SELECT * FROM activos", conn)
    conn.close()
    return df

def guardar_amef(tag_activo, funcion, falla_funcional, modo_falla, efecto):
    """Inserta un nuevo modo de falla asociado a un activo."""
    conn = sqlite3.connect("confiabilidad.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO amef (tag_activo, funcion, falla_funcional, modo_falla, efecto)
        VALUES (?, ?, ?, ?, ?)
    """, (tag_activo, funcion, falla_funcional, modo_falla, efecto))
    conn.commit()
    conn.close()

def cargar_amef_por_equipo(tag_activo):
    """Retorna el AMEF de un equipo específico como DataFrame."""
    conn = sqlite3.connect("confiabilidad.db")
    df = pd.read_sql_query(f"SELECT funcion, falla_funcional, modo_falla, efecto FROM amef WHERE tag_activo = '{tag_activo}'", conn)
    conn.close()
    return df