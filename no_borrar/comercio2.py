from producto import Producto
from vendedor import Vendedor
from vendedor_dao import VendedorDAO
from producto_dao import ProductoDAO
from logger_base import log

class Comercio:
    def __init__(self, nombre_negocio, direccion, telefono, pagina_web):
        # Constructor de la clase Comercio
        self._nombre_negocio = nombre_negocio
        self._direccion = direccion
        self._telefono = telefono
        self._pagina_web = pagina_web
        self._lista_vendedores = []
        self._lista_productos = []
        self._lista_ventas = []
        self._lista_total = []
        self._lista_actualizada = []

    def __str__(self):
        # Método para representar la instancia de Comercio en forma de cadena
        return f'''
                Nombre comercial: {self._nombre_negocio} | Dirección: {self._direccion}
                Teléfono: {self._telefono} | Página Web: {self._pagina_web}
                '''
    # Propiedades y setters para los atributos
    @property
    def nombre_negocio(self):
        return self._nombre_negocio
    
    @nombre_negocio.setter
    def nombre_negocio(self, nombre_negocio):
        self._nombre_negocio = nombre_negocio
    
    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, direccion):
        self._direccion = direccion
    
    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, telefono):
        self._telefono = telefono
    
    @property
    def pagina_web(self):
        return self._pagina_web
    
    @pagina_web.setter
    def pagina_web(self, pagina_web):
        self._pagina_web = pagina_web

    # Métodos para agregar, imprimir y gestionar productos y vendedores

    def agregar_producto(self, producto):
        # Agregar un producto a la lista de productos
        self._lista_productos.append(producto)


    def imprimir_productos(self, lista_productos):
        # Imprimir la lista de productos
        for producto in lista_productos:
            log.info(producto)
    
    def eliminar_producto(self, producto):
        producto = Producto(id_producto= producto)
        productos_eliminados = ProductoDAO.eliminar(producto)
        log.info(f'Productos eliminados: {productos_eliminados}')

    def agregar_vendedor(self, vendedor):
        # Agregar un vendedor a la lista de vendedores
        self._lista_vendedores.append(vendedor)


    def imprimir_vendedores(self, lista_vendedores):
        # Imprimir la lista de vendedores
        for vendedor in lista_vendedores:
            log.info(vendedor)

    def eliminar_vendedor(self, vendedor):
        vendedor = Vendedor(id_vendedor= vendedor)
        vendedores_eliminados = VendedorDAO.eliminar(vendedor)
        log.info(f'Vendedores eliminados: {vendedores_eliminados}')
    # def imprimir_ventas(self):
    #     #Imprimir la lista de venta total
    #     for venta in self._lista_total:
    #         print(venta)
    
    def validar_producto(self, nombre_producto):
        # Validar si un vendedor existe en la lista de vendedores
        # for producto in self._lista_productos:
        for producto in ProductoDAO._productos:
            if producto.nombre_producto == nombre_producto:
                return producto
        else:
            return None

    def validar_vendedor(self, documento_vendedor):
        # Validar si un vendedor existe en la lista de vendedores
        for vendedor in VendedorDAO._vendedores:
            if vendedor.documento_vendedor == documento_vendedor:
                return vendedor
        else:
            return None
        
    def agregar_venta(self, venta):
        # Agregar una venta a la lista de acumulado ventas
        self._lista_ventas.append(venta)
        self._lista_total.append(venta)

    def actualizar_inventario(self, producto, cantidad):
        # Actualizar el inventario de un producto
        if producto.cantidad_producto > cantidad:
            producto.cantidad_producto -= cantidad
            return producto.cantidad_producto
        else:
            return False
    
    # def imprimir_lista_actualizada(self):
    #     for producto in self._lista_actualizada:
    #         return producto_actualizado
        
    def registrar_venta(self, nombre_producto, validar_producto):
        cantidad_producto = int(input('Ingrese la cantidad del producto a comprar: '))
        # Registrar una venta
        cantidad = self.actualizar_inventario(validar_producto, cantidad_producto)
        
        if not cantidad:
            print('El número de unidades requeridas supera al número de unidades disponibles.')
        else:
            venta_nueva_producto = Producto(id_producto=validar_producto._id_producto,nombre_producto = nombre_producto, precio_producto= validar_producto.precio_producto, cantidad_producto= cantidad_producto)
            self.agregar_venta(venta_nueva_producto)
            producto = Producto(id_producto= validar_producto.id_producto, cantidad_producto= validar_producto.cantidad_producto)
            producto_actualizado = ProductoDAO.actualizar(producto)
            print('Venta exitosa')
            log.info(f'Productos actualizados: {producto_actualizado}')
            self._lista_actualizada.append(producto)
            #venta_nueva_venta = Venta(validar_producto._id_producto,nombre_producto, validar_producto.precio_producto, cantidad_producto)
            #self.agregar_venta_total(venta_nueva)
            valor_total = cantidad_producto * validar_producto.precio_producto
            return valor_total
    
    def imprimir_factura(self, validar_vendedor):
        # Imprimir una factura de venta
        nombre_comercio = self._nombre_negocio.center(len(self._nombre_negocio) + 30, '-')
        print(nombre_comercio)
        print(f'Cajero: {validar_vendedor._nombre_vendedor}')
        tipo_alimento = 'ALIMENTOS'
        print(tipo_alimento.ljust(len(tipo_alimento) + 20, '*'))
        print('CANT. DESCRIPCIÓN')
        subtotal = 0
        total = 0
        for venta in self._lista_total:
            total_venta = venta.precio_producto * venta.cantidad_producto
            print(f"{venta.cantidad_producto} {venta.nombre_producto.ljust(len(venta.nombre_producto) + 20, '-')} {total_venta}")
            subtotal += total_venta
            total = subtotal + (subtotal * 19 / 100)
        print(f'SUBTOTAL: {subtotal}')
        print(f'IVA 19%: {subtotal * 19 / 100}')
        print(f'TOTAL: {total}')
        return total

    def agregar_total(self, total, validar_vendedor):
        # Agregarle el total de venta realizada a el empleado correspondiente
        validar_vendedor.suma_vendedor += total  
        print(validar_vendedor.suma_vendedor)
        vendedor = Vendedor(id_vendedor= validar_vendedor.id_vendedor, suma_vendedor= validar_vendedor.suma_vendedor)
        vendedor_actualizado = VendedorDAO.actualizar(vendedor)
        log.info(f'Vendedores actualizados: {vendedor_actualizado}')

    def registro_producto(self):
        # Solicitar el nombre del producto al usuario
        nombre_producto = input('Ingrese el nombre del producto: ')
        # Validar si el producto ya está registrado
        validar_producto = self.validar_producto(nombre_producto)
        if not validar_producto:
            while True:
                try:
                    # Solicitar el precio del producto y la cantidad
                    precio_producto = int(input('Ingrese el precio del producto: '))
                    cantidad_producto = int(input('Ingrese la cantidad total del producto: '))
                    if precio_producto > 0 and cantidad_producto > 0:
                        # Crear una instancia de Producto y agregarlo
                        producto = Producto(nombre_producto = nombre_producto, precio_producto = precio_producto, cantidad_producto = cantidad_producto)
                        producto_insertado = ProductoDAO.insertar(producto)
                        log.info(f'Usuarios insertados: {producto_insertado}')
                        self.agregar_producto(producto)
                        print('Producto añadido con éxito.')
                        break
                    else:
                        print('El precio y la cantidad deben ser números enteros positivos.')
                except ValueError as e:
                    print(f'Error: El precio y la cantidad deben ser números enteros válidos. No letras. {e}')
        else:
            print('Producto se encuentra registrado.')
    

    def registrar_vendedor(self):
        # Solicitar el documento del vendedor al usuario
        documento_vendedor = int(input('Ingrese el documento del vendedor: '))
        # Validar si el vendedor ya está registrado
        validar_vendedor = self.validar_vendedor(documento_vendedor)
        if not validar_vendedor:
            #Solicitar el nombre del vendedor
            nombre_vendedor = input('Ingrese el nombre del vendedor: ')
            #Crear una instancia de Vendedor y agregarlo
            vendedor = Vendedor(documento_vendedor= documento_vendedor, nombre_vendedor= nombre_vendedor, suma_vendedor= 0)
            vendedor_insertado = VendedorDAO.insertar(vendedor)
            log.info(f'Usuarios insertados: {vendedor_insertado}')
            self.agregar_vendedor(vendedor)
            print('Vendedor añadido con éxito.')
        else:
            print('Vendedor se encuentra registrado.')
            
    def validar_venta(self):
        documento_vendedor = int(input('Ingrese el documento del vendedor a buscar: '))
        validar_vendedor = self.validar_vendedor(documento_vendedor)
        if not validar_vendedor:
            print('El vendedor no se encuentra registrado en la base de datos.')
        else:
            nombre_producto = input('Ingrese el nombre del producto a comprar: ')
            validar_producto = self.validar_producto(nombre_producto)
        if not validar_producto:
            print('Producto no encontrado en el inventario.')
        else:
            total_venta = self.registrar_venta(nombre_producto,validar_producto)
        while True:
            instrucciones_venta = '''
                Ingrese 1 para imprimir la factura de venta
                Ingrese 2 para agregar otro producto a la factura
                Ingrese 3 para finalizar la venta
                                '''
            operacion_venta = input(instrucciones_venta).strip()
            if operacion_venta == '1':
                total_venta = self.imprimir_factura(validar_vendedor) # Comentario: Imprime la factura de venta.
            elif operacion_venta == '2':
                nombre_producto = input('Ingrese el nombre del producto a comprar:')
                validar_producto = self.validar_producto(nombre_producto)
                if not validar_producto:
                    print('Producto no encontrado en el inventario.')
                else:
                    total_venta = self.registrar_venta(nombre_producto,validar_producto)
            elif operacion_venta == '3':
                self.agregar_total(total_venta, validar_vendedor)
                self._lista_total.clear()
                break
            else:
                print('Opción no válida. Introduce una opción válida.') # Comentario: Maneja errores inesperados.


    def menu_interactivo(self):
        while True:
            instrucciones = '''
            Ingrese A para registrar un nuevo producto
            Ingrese B para imprimir la lista de productos
            Ingrese X para eliminar un producto
            Ingrese C para registrar un vendedor
            Ingrese D para imprimir la lista de vendedores
            Ingrese Z para eliminar un vendedor
            Ingrese E para registrar una venta
            Ingrese V para imprimir la lista de ventas
            Ingrese Q para salir
            '''
            
            operacion = input(instrucciones).strip().upper()

            try:
                if operacion == 'A':
                    self.registro_producto() # Comentario: Llama a la función de registro de productos.
                elif operacion == 'B':
                    productos = ProductoDAO.seleccionar()
                    self.imprimir_productos(productos) # Comentario: Imprime la lista de productos.
                elif operacion == 'X':
                    id_producto = int(input('Ingrese el ID producto que desea eliminar: '))
                    self.eliminar_producto(id_producto)
                elif operacion == 'C':
                    self.registrar_vendedor() # Comentario: Llama a la función de registro de vendedores.
                elif operacion == 'D':
                    vendedores = VendedorDAO.seleccionar()
                    self.imprimir_vendedores(vendedores) # Comentario: Imprime la lista de vendedores.
                elif operacion == 'Z':
                    id_vendedor = int(input('Ingrese el ID vendedor que desea eliminar: '))
                    self.eliminar_vendedor(id_vendedor)
                elif operacion == 'E':
                    self.validar_venta()
                elif operacion == 'V':
                    self.imprimir_ventas()
                elif operacion == 'Q':
                    break
                else:
                    print('Opción no válida. Introduce una opción válida')
            except Exception as e:
                print(f'Error inesperado: {e}')