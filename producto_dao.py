from cursor_pool import CursorPool
from producto import Producto
from logger_base import log

class ProductoDAO:
    _SELECCIONAR = 'SELECT * FROM producto ORDER BY id_producto'
    _INSERTAR = 'INSERT INTO producto(nombre_producto, precio_producto, cantidad_producto) VALUES(%s,%s, %s)'
    _ACTUALIZAR = 'UPDATE producto SET cantidad_producto=%s WHERE id_producto=%s'
    _ELIMINAR = 'DELETE FROM producto WHERE id_producto=%s'
    _productos = []

    @classmethod
    def cargar_datos(cls):
        cls._productos = []  # Limpia la lista antes de cargar datos
        with CursorPool() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            for registro in registros:
                producto = Producto(registro[0], registro[1], registro[2], registro[3])
                ProductoDAO._productos.append(producto)

    @classmethod
    def seleccionar(cls):
        if not cls._productos:
            cls.cargar_datos()  # Carga los datos si la lista está vacía
        return cls._productos

    @classmethod
    def insertar(cls, producto):
         with CursorPool() as cursor:
             valores = (producto.nombre_producto, producto.precio_producto, producto.cantidad_producto)
             cursor.execute(cls._INSERTAR, valores)
             log.debug(f'Producto insertado: {producto}')
             return cursor.rowcount

    @classmethod
    def actualizar(cls, producto):
        with CursorPool() as cursor:
            valores = (producto.cantidad_producto, producto.id_producto)
            cursor.execute(cls._ACTUALIZAR, valores)
            log.debug(f'Producto actualizado: {producto}')
            return cursor.rowcount

    @classmethod
    def eliminar(cls, vendedor):
         with CursorPool() as cursor:
            valores = (vendedor.id_producto,)
            cursor.execute(cls._ELIMINAR, valores)
            log.debug(f'Objeto eliminado: {vendedor}')
            return cursor.rowcount

# Ejemplo de uso:
if __name__ == '__main__':
    productos = ProductoDAO.seleccionar()  # Cargar datos si la lista está vacía
    for producto in productos:
        print(f'ID: {producto.id_producto}, Nombre: {producto.nombre_producto}, Cantidad: {producto.cantidad_producto}')