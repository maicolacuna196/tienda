from cursor_pool import CursorPool
from logger_base import log
from venta import Venta

class VentaDAO:
    _SELECCIONAR = 'SELECT * FROM ventas ORDER BY id_venta'
    _INSERTAR = 'INSERT INTO ventas(id_producto,nombre_producto, precio_producto, cantidad_producto) VALUES(%s,%s,%s,%s)'
    _ELIMINAR = 'DELETE FROM ventas WHERE id_venta=%s'
    _ventas = []

    @classmethod

    def cargar_datos(cls):
        cls._ventas = []  # Limpia la lista antes de cargar datos
        with CursorPool() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            for registro in registros:
                venta = Venta(registro[1], registro[2], registro[3], registro[4])
                VentaDAO._ventas.append(venta)
    
    @classmethod
    def seleccionar(cls):
        if not cls._ventas:
            cls.cargar_datos()  # Carga los datos si la lista está vacía
        return cls._ventas
    
    @classmethod
    def insertar(cls, venta):
         with CursorPool() as cursor:
             valores = (venta.id_producto,venta.producto_vendido, venta.valor_producto, venta.cantidad_vendida)
             cursor.execute(cls._INSERTAR, valores)
             log.debug(f'Venta insertada: {venta}')
             return cursor.rowcount
    
    @classmethod
    def eliminar(cls, venta):
         with CursorPool() as cursor:
            valores = (venta.id_venta,)
            cursor.execute(cls._ELIMINAR, valores)
            log.debug(f'Objeto eliminado: {venta}')
            return cursor.rowcount

# Ejemplo de uso:
if __name__ == '__main__':
    ventas = VentaDAO.seleccionar()  # Cargar datos si la lista está vacía
    for venta in ventas:
        print(f'ID Venta: {venta.id_venta} , ID Producto: {venta.id_producto}, Nombre: {venta.nombre_producto}, precio: {venta.precio_producto}, cantidad: {venta.cantidad_producto}')