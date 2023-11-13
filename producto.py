
class Producto:

    cont_id = 0
    @classmethod
    def producto_id(cls):
        cls.cont_id += 1
        return cls.cont_id

    def __init__(self, id_producto = 0, nombre_producto= None, precio_producto= 0, cantidad_producto= 0):
        self.id_producto = id_producto
        self._nombre_producto = nombre_producto
        self._precio_producto = precio_producto
        self._cantidad_producto = cantidad_producto
    
    def __str__(self):
        return f'''
                ID producto: {self._id_producto} | Nombre producto: {self._nombre_producto}
                Precio producto: ${self._precio_producto} | Cantidad {self._cantidad_producto}
                '''
    
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
    
