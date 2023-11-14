class Venta:

    def __init__(self,id_venta=0,id_producto=0, nombre_producto=None, precio_producto=0, cantidad_producto=0):
        self._id_venta = id_venta
        self._id_producto = id_producto
        self._nombre_producto = nombre_producto
        self._precio_producto = precio_producto
        self._cantidad_producto = cantidad_producto

    @property
    def id_venta(self):
        return self._id_venta
    
    id_venta.setter
    def id_venta(self, id_venta):
        self._id_venta = id_venta
    
    @property
    def id_producto(self):
        return self._id_producto
    
    @id_producto.setter
    def id_producto(self, id_producto):
        self._id_producto = id_producto
    
    @property
    def nombre_producto(self):
        return self._nombre_producto

    @nombre_producto.setter
    def nombre_producto(self, nombre_producto):
        self._nombre_producto = nombre_producto
    
    @property
    def precio_producto(self):
        return self._precio_producto
    
    @precio_producto.setter
    def precio_producto(self, precio_producto):
        self._precio_producto = precio_producto
    
    @property
    def cantidad_producto(self):
        return self._cantidad_producto
    
    @cantidad_producto.setter
    def cantidad_producto(self, cantidad_producto):
        self._cantidad_producto = cantidad_producto
        
    def __str__(self):
        return f'''
                ID venta: {self._id_venta} | |ID producto: {self._id_producto} | Nombre producto: {self._nombre_producto}
                Venta total: ${self._precio_producto} | Cantidad vendida: {self._cantidad_producto}
                '''        



