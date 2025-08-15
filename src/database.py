import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str = "lista_compras.db"):
        self.db_path = Path(db_path)
        self._initialize_db()

    def _initialize_db(self):
        """Inicializa la base de datos con las tablas necesarias"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla de usuarios
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id INTEGER PRIMARY KEY,
                username TEXT
            )
            """)
            
            # Tabla de categorías
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                nombre TEXT,
                FOREIGN KEY (user_id) REFERENCES usuarios (user_id),
                UNIQUE (user_id, nombre)
            )
            """)
            
            # Tabla de productos
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                producto_id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria_id INTEGER,
                nombre TEXT,
                comprado BOOLEAN DEFAULT 0,
                FOREIGN KEY (categoria_id) REFERENCES categorias (categoria_id),
                UNIQUE (categoria_id, nombre)
            )
            """)
            conn.commit()

    def _get_connection(self):
        """Retorna una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)

    def get_or_create_user(self, user_id: int, username: str = None):
        """Registra un usuario si no existe o actualiza el username si cambió"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Insertar si no existe
            cursor.execute(
                "INSERT OR IGNORE INTO usuarios (user_id, username) VALUES (?, ?)",
                (user_id, username)
            )

            # Actualizar el username si cambió
            cursor.execute(
                "SELECT username FROM usuarios WHERE user_id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            if row and row[0] != username:
                cursor.execute(
                    "UPDATE usuarios SET username = ? WHERE user_id = ?",
                    (username, user_id)
                )

            conn.commit()


    def crear_categoria(self, user_id: int, nombre: str) -> bool:
        """Crea una nueva categoría para un usuario"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO categorias (user_id, nombre) VALUES (?, ?)",
                    (user_id, nombre.lower())
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def eliminar_categoria(self, user_id: int, nombre: str) -> bool:
        """Elimina una categoría y sus productos"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Primero obtenemos el ID de la categoría
            cursor.execute(
                "SELECT categoria_id FROM categorias WHERE user_id = ? AND nombre = ?",
                (user_id, nombre.lower())
            )
            categoria = cursor.fetchone()
            
            if categoria:
                categoria_id = categoria[0]
                # Eliminamos los productos asociados
                cursor.execute(
                    "DELETE FROM productos WHERE categoria_id = ?",
                    (categoria_id,)
                )
                # Eliminamos la categoría
                cursor.execute(
                    "DELETE FROM categorias WHERE categoria_id = ?",
                    (categoria_id,)
                )
                conn.commit()
                return True
            return False

    def obtener_categorias(self, user_id: int) -> list:
        """Obtiene todas las categorías de un usuario con conteo de productos"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT c.nombre, COUNT(p.producto_id)
            FROM categorias c
            LEFT JOIN productos p ON c.categoria_id = p.categoria_id
            WHERE c.user_id = ?
            GROUP BY c.categoria_id
            """, (user_id,))
            return cursor.fetchall()
            
    def agregar_producto(self, user_id: int, categoria_nombre: str, producto_nombre: str) -> bool:
        """Agrega un producto a una categoría (creando la categoría si no existe)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Buscar o crear la categoría
            cursor.execute(
                "SELECT categoria_id FROM categorias WHERE user_id = ? AND nombre = ?",
                (user_id, categoria_nombre.lower())
            )
            categoria = cursor.fetchone()

            if not categoria:
                try:
                    cursor.execute(
                        "INSERT INTO categorias (user_id, nombre) VALUES (?, ?)",
                        (user_id, categoria_nombre.lower())
                    )
                    categoria_id = cursor.lastrowid
                except sqlite3.IntegrityError:
                    return False  # Falló al crear categoría
            else:
                categoria_id = categoria[0]

            # Intentar insertar el producto
            try:
                cursor.execute(
                    "INSERT INTO productos (categoria_id, nombre) VALUES (?, ?)",
                    (categoria_id, producto_nombre.lower())
                )
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False  # Producto ya existe

    def eliminar_producto(self, user_id: int, categoria_nombre: str, producto_nombre: str) -> bool:
        """Elimina un producto de una categoría"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
            SELECT c.categoria_id 
            FROM categorias c
            WHERE c.user_id = ? AND c.nombre = ?
            """, (user_id, categoria_nombre.lower()))
            categoria = cursor.fetchone()
            
            if categoria:
                categoria_id = categoria[0]
                cursor.execute("""
                DELETE FROM productos 
                WHERE categoria_id = ? AND nombre = ?
                """, (categoria_id, producto_nombre.lower()))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    
                    # Verificamos si la categoría quedó vacía
                    cursor.execute(
                        "SELECT COUNT(*) FROM productos WHERE categoria_id = ?",
                        (categoria_id,)
                    )
                    if cursor.fetchone()[0] == 0:
                        cursor.execute(
                            "DELETE FROM categorias WHERE categoria_id = ?",
                            (categoria_id,)
                        )
                        conn.commit()
                    return True
            return False

    def obtener_productos(self, user_id: int) -> list:
        """Obtiene todos los productos de un usuario organizados por categoría"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT c.nombre, p.nombre, p.comprado
            FROM categorias c
            JOIN productos p ON c.categoria_id = p.categoria_id
            WHERE c.user_id = ?
            ORDER BY c.nombre, p.nombre
            """, (user_id,))
            return cursor.fetchall()

    def marcar_producto(self, user_id: int, categoria_nombre: str, producto_nombre: str, estado: bool) -> bool:
        """Marca/desmarca un producto como comprado"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
            SELECT p.producto_id
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.categoria_id
            WHERE c.user_id = ? AND c.nombre = ? AND p.nombre = ?
            """, (user_id, categoria_nombre.lower(), producto_nombre.lower()))
            
            producto = cursor.fetchone()
            
            if producto:
                producto_id = producto[0]
                cursor.execute(
                    "UPDATE productos SET comprado = ? WHERE producto_id = ?",
                    (1 if estado else 0, producto_id)
                )
                conn.commit()
                return True
            return False