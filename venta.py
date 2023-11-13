class Venta:

    def __init__(self,id_venta=0,id_producto=0, nombre_producto=None, precio_producto=0, cantidad_producto=0):
        self.id_venta = id_venta
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.precio_producto = precio_producto
        self.cantidad_producto = cantidad_producto

        
    def __str__(self):
        return f'''
                ID venta: {self.id_venta} | |ID producto: {self.id_producto} | Nombre producto: {self.nombre_producto}
                Venta total: ${self.precio_producto} | Cantidad vendida: {self.cantidad_producto}
                '''        



