from producto import Producto
from vendedor import Vendedor
from vendedor_dao import VendedorDAO
from producto_dao import ProductoDAO
from logger_base import log
from venta import Venta
from ventas_dao import VentaDAO

class Tienda:
    def __init__(self, nombre_negocio, direccion, telefono, sitio_web):
        self._nombre_negocio = nombre_negocio
        self._direccion = direccion
        self._telefono = telefono
        self._sitio_web = sitio_web
        self._lista_vendedores = []
        self._lista_productos = []
        self._lista_ventas = []
        self._lista_total = []
        self._lista_actualizada = []

    def __str__(self):
        return f'''
                Nombre Comercial: {self._nombre_negocio} | Dirección: {self._direccion}
                Teléfono: {self._telefono} | Sitio Web: {self._sitio_web}
                '''

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
    def sitio_web(self):
        return self._sitio_web
    
    @sitio_web.setter
    def sitio_web(self, sitio_web):
        self._sitio_web = sitio_web

    def agregar_producto(self, producto):
        self._lista_productos.append(producto)

    def actualizar_inventario_gestion(self, lista_productos, id_producto, cantidad_nueva):
        for producto in lista_productos:
            if producto.id_producto == id_producto:
                producto.cantidad_producto += cantidad_nueva
                productos_actualizados = ProductoDAO.actualizar(producto)
                if productos_actualizados > 0:
                    log.info(f'Productos actualizados: {productos_actualizados}')
                    break  # Termina la iteración después de la actualización
                else:
                    log.warning(f'No se pudieron actualizar los productos para el ID: {id_producto}')
        else:
            log.warning(f'No se encontraron productos para el ID: {id_producto}')

    def imprimir_productos(self, lista_productos):
        for producto in lista_productos:
            log.info(producto)

    def eliminar_producto(self, id_producto):
        producto = Producto(id_producto=id_producto)
        productos_eliminados = ProductoDAO.eliminar(producto)
        if productos_eliminados > 0:
            log.info(f'Productos eliminados: {productos_eliminados}')
        else:
            log.warning(f'No se encontraron productos para el ID: {id_producto}')

    def agregar_vendedor(self, vendedor):
        self._lista_vendedores.append(vendedor)

    def imprimir_vendedores(self, lista_vendedores):
        for vendedor in lista_vendedores:
            log.info(vendedor)

    def eliminar_vendedor(self, id_vendedor):
        vendedor = Vendedor(id_vendedor=id_vendedor)
        vendedores_eliminados = VendedorDAO.eliminar(vendedor)
        if vendedores_eliminados > 0:
            log.info(f'Vendedores eliminados: {vendedores_eliminados}')
        else:
            log.warning(f'No se encontraron vendedores para el ID: {id_vendedor}')

    def validar_producto(self, nombre_producto):
        # Validar si un vendedor existe en la lista de vendedores
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
        self._lista_ventas.append(venta)
        self._lista_total.append(venta)

    def actualizar_inventario(self, producto, cantidad):
        if producto.cantidad_producto >= cantidad:
            producto.cantidad_producto -= cantidad
            return True
        else:
            return False
    
    def registrar_venta(self, nombre_producto, validar_producto):
        try:
            cantidad = int(input('Ingrese la cantidad del producto a comprar: '))
            if cantidad <= 0:
                print('La cantidad debe ser un número entero positivo.')
                return 0
            
            if self.actualizar_inventario(validar_producto, cantidad):
                nueva_venta = Producto(id_producto=validar_producto.id_producto, nombre_producto=nombre_producto, precio_producto=validar_producto.precio_producto, cantidad_producto=cantidad)
                self.agregar_venta(nueva_venta)
                producto = Producto( cantidad_producto=validar_producto.cantidad_producto,id_producto=validar_producto.id_producto)
                producto_actualizado = ProductoDAO.actualizar(producto)
                log.info(f'Producto actualizado: {producto_actualizado}')
                venta = Venta(id_producto=validar_producto.id_producto, producto_vendido=validar_producto.nombre_producto, valor_producto=validar_producto.precio_producto * cantidad, cantidad_vendida=cantidad)
                self._lista_actualizada.append(venta)
                venta_insertada = VentaDAO.insertar(venta)
                log.info(f'Ventas insertadas {venta_insertada}')
                valor_total = cantidad * validar_producto.precio_producto
                return valor_total
            else:
                print('La cantidad requerida supera la cantidad disponible.')
                return 0
        except ValueError as e:
            print(f'Error: La cantidad debe ser un número entero válido. Sin letras. {e}')
            return 0
        
       
    def imprimir_ventas(self, lista_ventas):
        for venta in lista_ventas:
            print(venta)

    def imprimir_factura(self, validar_vendedor):
        nombre_comercial = self._nombre_negocio.center(len(self._nombre_negocio) + 30, '-')
        print(nombre_comercial)
        print(f'Cajero: {validar_vendedor._nombre_vendedor}')
        tipo_alimento = 'ALIMENTOS'
        print(tipo_alimento.ljust(len(tipo_alimento) + 20, '*'))
        print('CANT. DESCRIPCIÓN')
        subtotal = 0
        
        for venta in self._lista_total:
            total_venta = venta.precio_producto * venta.cantidad_producto
            print(f"{venta.cantidad_producto} {venta.nombre_producto.ljust(len(venta.nombre_producto) + 20, '-')} {total_venta}")
            subtotal += total_venta
        
        print(f'SUBTOTAL: ${subtotal}')
        descuento = self.aplicar_descuento(subtotal)
        
        print(f'IVA 19%: ${subtotal * 0.19}')
        print(f'Descuento: ${descuento}')
        
        total = subtotal + (subtotal * 0.19) - descuento
        print(f'TOTAL: ${total}')
        return total

    def aplicar_descuento(self, subtotal):
        descuento = 0
        
        if subtotal >= 100000:
            descuento = subtotal * 5 / 100
        elif subtotal >= 200000:
            descuento = subtotal * 10 / 100
        
        return descuento



    def agregar_total(self, total, validar_vendedor):
        validar_vendedor.suma_vendedor += total  
        print(validar_vendedor.suma_vendedor)
        vendedor = Vendedor(id_vendedor=validar_vendedor.id_vendedor, suma_vendedor=validar_vendedor.suma_vendedor)
        vendedor_actualizado = VendedorDAO.actualizar(vendedor)
        log.info(f'Vendedores actualizados: {vendedor_actualizado}')

    def registro_producto(self):
        nombre_producto = input('Ingrese el nombre del producto: ')
        validar_producto = self.validar_producto(nombre_producto)
        if not validar_producto:
            while True:
                try:
                    precio_producto = int(input('Ingrese el precio del producto: '))
                    cantidad_producto = int(input('Ingrese la cantidad total del producto: '))
                    if precio_producto > 0 and cantidad_producto > 0:
                        nuevo_producto = Producto(nombre_producto=nombre_producto, precio_producto=precio_producto, cantidad_producto=cantidad_producto)
                        producto_insertado = ProductoDAO.insertar(nuevo_producto)
                        log.info(f'Productos insertados: {producto_insertado}')
                        self.agregar_producto(nuevo_producto)
                        print('Producto añadido con éxito.')
                        break
                    else:
                        print('El precio y la cantidad deben ser números enteros positivos.')
                except ValueError as e:
                    print(f'Error: El precio y la cantidad deben ser números enteros válidos. No letras. {e}')
        else:
            print('El producto ya está registrado.')

    def registrar_vendedor(self):
        documento_vendedor = int(input('Ingrese el documento del vendedor: '))
        validar_vendedor = self.validar_vendedor(documento_vendedor)
        if not validar_vendedor:
            nombre_vendedor = input('Ingrese el nombre del vendedor: ')
            nuevo_vendedor = Vendedor(documento_vendedor=documento_vendedor, nombre_vendedor=nombre_vendedor, suma_vendedor=0)
            vendedor_insertado = VendedorDAO.insertar(nuevo_vendedor)
            log.info(f'Vendedores insertados: {vendedor_insertado}')
            self.agregar_vendedor(nuevo_vendedor)
            print('Vendedor añadido con éxito.')
        else:
            print('El vendedor ya está registrado.')

    def validar_venta(self):
        documento_vendedor = int(input('Ingrese el documento del vendedor a buscar: '))
        validar_vendedor = self.validar_vendedor(documento_vendedor)
        
        if not validar_vendedor:
            print('El vendedor no se encuentra registrado en la base de datos.')
            return

        nombre_producto = input('Ingrese el nombre del producto a comprar: ')
        validar_producto = self.validar_producto(nombre_producto)
        
        if not validar_producto:
            print('El producto no se encuentra en el inventario.')
            return

        total_venta = self.registrar_venta(nombre_producto, validar_producto)

        while True:
            instrucciones_venta = '''
                                    Ingrese 1 para imprimir la factura de venta
                                    Ingrese 2 para agregar otro producto a la factura
                                    Ingrese 3 para finalizar la venta
                                    '''
            operacion_venta = input(instrucciones_venta).strip()
            
            if operacion_venta == '1':
                total_venta = self.imprimir_factura(validar_vendedor)
            elif operacion_venta == '2':
                nombre_producto = input('Ingrese el nombre del producto a comprar:')
                validar_producto = self.validar_producto(nombre_producto)
                
                if not validar_producto:
                    print('El producto no se encuentra en el inventario.')
                else:
                    total_venta = self.registrar_venta(nombre_producto, validar_producto)
            elif operacion_venta == '3':
                self.agregar_total(total_venta, validar_vendedor)
                self._lista_total.clear()
                break
            else:
                print('Opción no válida. Introduce una opción válida.')

    def menu_interactivo(self):
        while True:
            instrucciones = '''
            Ingrese A para registrar un nuevo producto
            Ingrese B para imprimir la lista de productos
            Ingrese M para actualizar la lista de productos
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
                    self.registro_producto()
                elif operacion == 'B':
                    productos = ProductoDAO.seleccionar()
                    self.imprimir_productos(productos)
                elif operacion == 'M':
                    id_producto = int(input('Ingrese el ID del producto que desea actualizar: '))
                    cantidad_producto = int(input('Ingrese la cantidad de producto añadido al inventario: '))
                    productos = ProductoDAO.seleccionar()
                    self.actualizar_inventario_gestion(productos, id_producto, cantidad_producto)
                elif operacion == 'X':
                    id_producto = int(input('Ingrese el ID del producto que desea eliminar: '))
                    self.eliminar_producto(id_producto)
                elif operacion == 'C':
                    self.registrar_vendedor()
                elif operacion == 'D':
                    vendedores = VendedorDAO.seleccionar()
                    self.imprimir_vendedores(vendedores)
                elif operacion == 'Z':
                    id_vendedor = int(input('Ingrese el ID del vendedor que desea eliminar: '))
                    self.eliminar_vendedor(id_vendedor)
                elif operacion == 'E':
                    self.validar_venta()
                elif operacion == 'V':
                    ventas = VentaDAO.seleccionar()
                    self.imprimir_ventas(ventas)
                elif operacion == 'Q':
                    break
                else:
                    print('Opción no válida. Introduce una opción válida')
            except Exception as e:
                print(f'Error inesperado: {e}')

# Iniciar la aplicación
if __name__ == '__main__':
    tienda = Tienda("Mi Tienda", "123 Calle Principal", "555-555-5555", "www.mitienda.com")
    tienda.menu_interactivo()
