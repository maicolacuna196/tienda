from cursor_pool import CursorPool
from logger_base import log
from venta import Venta

class ventaDAO:
    _SELECCIONAR = 'SELECT * FROM producto ORDER BY id_venta'
    _INSERTAR = 'INSERT INTO producto(nombre_producto, venta_total, cantidad_vendida, total_acumulado) VALUES(%s,%s, %s, %s)'
    _ELIMINAR = 'DELETE FROM producto WHERE id_venta=%s'
    _ventas = []