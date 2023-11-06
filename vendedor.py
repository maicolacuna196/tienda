class Vendedor:

    cont_id = 0
    @classmethod
    def vendedor_id(cls):
        cls.cont_id += 1
        return cls.cont_id

    def __init__(self, id_vendedor = 0, documento_vendedor= None, nombre_vendedor= None, suma_vendedor= 0):
        self._id_vendedor = id_vendedor
        self._documento_vendedor = documento_vendedor
        self._nombre_vendedor = nombre_vendedor
        self._suma_vendedor = suma_vendedor 
    
    def __str__(self):
        return f'''
                ID vendedor: {self._id_vendedor}
                Nombre vendedor: {self._nombre_vendedor} | Documento vendedor: {self._documento_vendedor}
                Total ventas acumuladas: {self._suma_vendedor}
                '''
    
    @property
    def id_vendedor(self):
        return self._id_vendedor
    
    @id_vendedor.setter
    def id_vendedor(self, id_vendedor):
        self._id_vendedor = id_vendedor
    
    @property
    def nombre_vendedor(self):
         self._nombre_vendedor

    @nombre_vendedor.setter
    def nombre_vendedor(self, nombre_vendedor):
         self._nombre_vendedor = nombre_vendedor
    
    @property
    def documento_vendedor(self):
        return self._documento_vendedor
    
    @documento_vendedor.setter
    def documento_vendedor(self, documento_vendedor):
        self._documento_vendedor = documento_vendedor
    
    @property
    def suma_vendedor(self):
        return self._suma_vendedor
    
    @suma_vendedor.setter
    def suma_vendedor(self, suma_vendedor):
        self._suma_vendedor = suma_vendedor