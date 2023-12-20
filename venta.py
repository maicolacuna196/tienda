class Venta:

    def __init__(self, id_producto, producto_vendido, valor_producto, cantidad_vendida):
        self._id_producto = id_producto
        self._producto_vendido = producto_vendido
        self._valor_producto = valor_producto
        self._cantidad_vendida = cantidad_vendida

    def __str__(self):
        return f'''
                ID producto: {self._id_producto} | Nombre producto: {self._producto_vendido}
                Precio producto: {self._valor_producto} | Cantidad vendida: {self._cantidad_vendida}
                '''        

    @property
    def id_producto(self):
        return self._id_producto
    
    @id_producto.setter
    def producto_vendido(self, id_producto):
        self._id_producto = id_producto

    @property
    def producto_vendido(self):
        return self._producto_vendido
    
    @producto_vendido.setter
    def producto_vendido(self, producto_vendido):
        self._producto_vendido = producto_vendido
    
    @property
    def valor_producto(self):
        return self._valor_producto
    
    @valor_producto.setter
    def valor_producto(self, valor_producto):
        self._valor_producto = valor_producto
    
    @property
    def cantidad_vendida(self):
        return self._cantidad_vendida
    
    @cantidad_vendida.setter
    def cantidad_vendida(self, cantidad_vendida):
        self._cantidad_vendida = cantidad_vendida

