from producto import Producto
class Venta(Producto):

    def __init__(self, id_producto, nombre_producto, precio_producto, cantidad_producto):
        super().__init__(id_producto, nombre_producto, precio_producto, cantidad_producto)

        
    def __str__(self):
        return f'''
                ID producto: {self._id_producto} | Nombre producto: {self._nombre_producto}
                Venta total: ${self._precio_producto} | Cantidad vendida: {self._cantidad_producto}
                '''        



