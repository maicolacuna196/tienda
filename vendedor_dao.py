from cursor_pool import CursorPool
from vendedor import Vendedor
from logger_base import log

class VendedorDAO:
    _SELECCIONAR = 'SELECT * FROM vendedor ORDER BY id_vendedor'
    _INSERTAR = 'INSERT INTO vendedor(documento, nombre_completo, acumulado_ventas) VALUES(%s,%s, %s)'
    _ACTUALIZAR = 'UPDATE vendedor SET acumulado_ventas=%s WHERE id_vendedor=%s'
    _ELIMINAR = 'DELETE FROM vendedor WHERE id_vendedor=%s'
    
    _vendedores = []  # Inicialmente vacía

    @classmethod
    def cargar_datos(cls):
        cls._vendedores = []  # Limpia la lista antes de cargar datos
        with CursorPool() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            for registro in registros:
                vendedor = Vendedor(registro[0], registro[1], registro[2], registro[3])
                VendedorDAO._vendedores.append(vendedor)

    @classmethod
    def seleccionar(cls):
        if not cls._vendedores:
            cls.cargar_datos()  # Carga los datos si la lista está vacía
        return cls._vendedores

    @classmethod
    def insertar(cls, vendedor):
         with CursorPool() as cursor:
             valores = (vendedor.documento_vendedor, vendedor._nombre_vendedor, vendedor.suma_vendedor)
             cursor.execute(cls._INSERTAR, valores)
             log.debug(f'Vendedor insertado: {vendedor}')
             return cursor.rowcount

    @classmethod
    def actualizar(cls, vendedor):
         with CursorPool() as cursor:
             valores = (vendedor.suma_vendedor, vendedor.id_vendedor)
             cursor.execute(cls._ACTUALIZAR, valores)
             log.debug(f'Vendedor actualizado: {vendedor}')
             return cursor.rowcount

    @classmethod
    def eliminar(cls, vendedor):
        with CursorPool() as cursor:
            valores = (vendedor.id_vendedor,)
            cursor.execute(cls._ELIMINAR, valores)
            log.debug(f'Objeto eliminado: {vendedor}')
            return cursor.rowcount

# Ejemplo de uso:
if __name__ == '__main__':
    vendedores = VendedorDAO.seleccionar()  # Cargar datos si la lista está vacía
    for vendedor in vendedores:
        print(f'ID: {vendedor.id_vendedor}, Documento: {vendedor.documento_vendedor}')

