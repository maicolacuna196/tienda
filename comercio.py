from producto import Producto
from vendedor import Vendedor
from venta import Venta
from producto_dao import ProductoDAO
from vendedor_dao import VendedorDAO
from ventas_dao import VentaDAO
from logger_base import log


class Tienda:
    def __init__(self, nombre_negocio, direccion, telefono, sitio_web):
        self._nombre_negocio = nombre_negocio
        self._direccion = direccion
        self._telefono = telefono
        self._sitio_web = sitio_web
        self._lista_vendedores = []
        self._lista_productos = []
        self._lista_ventas = []
        self._lista_temporal = []

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

    def agregar_vendedor(self, vendedor):
        self._lista_vendedores.append(vendedor)
    
    def agregar_venta_temporal(self, venta):
        self._lista_temporal.append(venta)

    def agregar_venta_acumulado(self, venta):
        self._lista_ventas.append(venta)

    def actualizar_acumulado_venta(self, total, validar_vendedor):
        try:
            validar_vendedor.suma_vendedor += total  
            vendedor = Vendedor(id_vendedor=validar_vendedor.id_vendedor, suma_vendedor=validar_vendedor.suma_vendedor)
            vendedor_actualizado = VendedorDAO.actualizar(vendedor)
            log.info(f'Vendedores actualizados: {vendedor_actualizado}')
        except Exception as e:
            print(f'Error al actualizar el acumulado de ventas del vendedor: {e}')

    def actualizar_inventario(self, producto, cantidad):
        if cantidad <= 0:
            raise ValueError('La cantidad debe ser un número entero positivo.')

        if producto.cantidad_producto >= cantidad:
            producto.cantidad_producto -= cantidad
            ProductoDAO.actualizar(producto)
            return True
        else:
            return False

    def eliminar_venta(self, id_venta):
        venta = Venta(id_venta= id_venta)
        ventas_eliminadas = VentaDAO.eliminar(venta)
        if ventas_eliminadas > 0:
            log.info(f'Ventas eliminados: {ventas_eliminadas}')
        else:
            log.warning(f'No se encontraron ventas para el ID: {id_venta}')

    def eliminar_producto(self, id_producto):
        producto = Producto(id_producto=id_producto)
        productos_eliminados = ProductoDAO.eliminar(producto)
        if productos_eliminados > 0:
            log.info(f'Productos eliminados: {productos_eliminados}')
        else:
            log.warning(f'No se encontraron productos para el ID: {id_producto}')

    def eliminar_vendedor(self, id_vendedor):
        vendedor = Vendedor(id_vendedor=id_vendedor)
        vendedores_eliminados = VendedorDAO.eliminar(vendedor)
        if vendedores_eliminados > 0:
            log.info(f'Vendedores eliminados: {vendedores_eliminados}')
        else:
            log.warning(f'No se encontraron vendedores para el ID: {id_vendedor}')
    
    def imprimir_productos(self, lista_productos):
        for producto in lista_productos:
            log.info(producto)

    def imprimir_vendedores(self, lista_vendedores):
        for vendedor in lista_vendedores:
            log.info(vendedor)

    def imprimir_ventas(self, lista):
        # Inicializar la suma total
        suma_total = 0

        # Iterar sobre las ventas e imprimir cada una
        for venta in lista:
            suma_total += venta.precio_producto
            log.info(venta)
        log.info(f'Total acumulado ventas: {suma_total}')

    def imprimir_factura(self, validar_vendedor):
        nombre_comercial = self._nombre_negocio.center(len(self._nombre_negocio) + 30, '-')
        print(nombre_comercial)
        print(f'Cajero: {validar_vendedor._nombre_vendedor}')
        tipo_alimento = 'ALIMENTOS'
        print(tipo_alimento.ljust(len(tipo_alimento) + 20, '*'))
        print('CANT. DESCRIPCIÓN')
        
        descuento = 0 
        subtotal = 0
        for item_venta in self._lista_temporal:
            total_venta = item_venta.precio_producto * item_venta.cantidad_producto
            print(f"{item_venta.cantidad_producto} {item_venta.nombre_producto.ljust(len(item_venta.nombre_producto) + 20, '-')} {total_venta}")
            subtotal += total_venta

        if subtotal > 100000:
            descuento = subtotal * 0.05
            print(f'¡Felicidades por tu compra! Al superar los $100,000 en tus compras, has obtenido un descuento del 5% en tu total. El descuento aplicado es de: ${descuento}.')
            iva = subtotal * 0.19
            total = subtotal + iva - descuento
        else:
            iva = subtotal * 0.19
            total = subtotal + iva - descuento


        print(f'SUBTOTAL: {subtotal}')
        print(f'IVA 19%: {iva}')
        print(f'TOTAL: {total}')
        return total

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
            Ingrese O para eliminar una venta
            Ingrese Q para salir
            '''
            operacion = input(instrucciones).strip().upper()
                
            try:
                if operacion == 'A':
                    self.registro_producto()
                elif operacion == 'B':
                    productos = ProductoDAO.seleccionar()
                    self.imprimir_productos(productos)
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
                elif operacion == 'O':
                    id_venta = int(input('Ingrese el ID de la venta que desea eliminar: '))
                    self.eliminar_venta(id_venta)
                elif operacion == 'Q':
                    break
                else:
                    print('Opción no válida. Introduce una opción válida')
            except ValueError as ve:
                print(f'Error: Ingrese un valor válido. Detalle: {ve}')
            except Exception as e:
                print(f'Error inesperado: {e}')

    def obtener_cantidad(self):
        try:
            cantidad = int(input('Ingrese la cantidad del producto a comprar: '))
            return cantidad
        except ValueError:
            raise ValueError('La cantidad debe ser un número entero válido.')

    def registrar_venta(self, nombre_producto, validar_producto):
        try:
            # Obtener la cantidad del usuario
            cantidad = self.obtener_cantidad()
            # Validar que la cantidad sea un número entero positivo
            self.validar_cantidad(cantidad)

            # Actualizar el inventario si hay suficientes productos disponibles
            if self.actualizar_inventario(validar_producto, cantidad):
                # Crear una nueva venta temporal
                nueva_venta_temporal = Producto(
                    id_producto=validar_producto.id_producto,
                    nombre_producto=nombre_producto,
                    precio_producto=validar_producto.precio_producto,
                    cantidad_producto=cantidad
                )
                # Agregar la venta temporal a la lista
                self.agregar_venta_temporal(nueva_venta_temporal)

                # Crear una nueva venta acumulada
                nueva_venta_acumulado = Venta( 
                        id_producto= validar_producto.id_producto,
                        nombre_producto=nombre_producto,
                        precio_producto=validar_producto.precio_producto* cantidad,
                        cantidad_producto=cantidad
                )
                

                # Agregar la venta acumulada a la lista
                venta_insertada = VentaDAO.insertar(nueva_venta_acumulado)
                log.info(f'Ventas insertadas: {venta_insertada}')
                self.agregar_venta_acumulado(nueva_venta_acumulado)
                

                # Actualizar la cantidad restante de unidades en la base de datos
                producto_actualizado = Producto(
                    id_producto=validar_producto.id_producto,
                    cantidad_producto=validar_producto.cantidad_producto
                )
                ProductoDAO.actualizar(producto_actualizado)
                log.info(f'Producto actualizado: {producto_actualizado}')

                # Calcular el valor total de la venta
                valor_total = cantidad * validar_producto.precio_producto
                return valor_total
            else:
                # Mensaje si la cantidad requerida supera la cantidad disponible
                print('La cantidad requerida supera la cantidad disponible.')
                return 0
        except ValueError as e:
            # Manejar errores relacionados con la entrada del usuario
            print(f'Error: {e}')
            return 0
        
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
        try:
            documento_vendedor = int(input('Ingrese el documento del vendedor: '))
            validar_vendedor = self.validar_vendedor(documento_vendedor)
        except ValueError:
            print('Error: Ingresa un numero válido para el documento del vendedor.')
            return

        if not validar_vendedor:
            nombre_vendedor = input('Ingrese el nombre del vendedor: ')
            nuevo_vendedor = Vendedor(documento_vendedor=documento_vendedor, nombre_vendedor=nombre_vendedor, suma_vendedor=0)
            vendedor_insertado = VendedorDAO.insertar(nuevo_vendedor)
            log.info(f'Vendedores insertados: {vendedor_insertado}')
            self.agregar_vendedor(nuevo_vendedor)
            print('Vendedor añadido con éxito.')
        else:
            print('El vendedor ya está registrado.')

    def validar_cantidad(self, cantidad):
        if cantidad <= 0:
            raise ValueError('La cantidad debe ser un número entero positivo.')


    def validar_venta(self):
        try:
            documento_vendedor = int(input('Ingrese el documento del vendedor a buscar: '))
            validar_vendedor = self.validar_vendedor(documento_vendedor)
        except ValueError:
            print('Error: Ingresa un número válido para el documento del vendedor.')
            return
            

        if not validar_vendedor:
            print('Error: El vendedor no se encuentra registrado en la base de datos.')
            return
        else:
            nombre_producto = input('Ingrese el nombre del producto a comprar: ')
            validar_producto = self.validar_producto(nombre_producto)
            if not validar_producto:
                print('Error: El producto no se encuentra en el inventario.')
            else:
                total_venta = self.registrar_venta(nombre_producto, validar_producto)

        while True:
            instrucciones_venta = '''
                                    Ingrese 1 para imprimir la factura de venta
                                    Ingrese 2 para agregar otro producto a la factura
                                    Ingrese 3 para finalizar la venta
                                    '''
            operacion_venta = input(instrucciones_venta).strip()
            if operacion_venta == '1':
                total_venta= self.imprimir_factura(validar_vendedor)
            elif operacion_venta == '2':
                nombre_producto = input('Ingrese el nombre del producto a comprar:')
                validar_producto = self.validar_producto(nombre_producto)
                if not validar_producto:
                    print('El producto no se encuentra en el inventario.')
                else:
                    total_venta= self.registrar_venta(nombre_producto, validar_producto)
            elif operacion_venta == '3':
                self.actualizar_acumulado_venta(total_venta, validar_vendedor)
                self._lista_temporal.clear()
                break
            else:
                print('Error: Opción no válida. Introduce una opción válida.')

    def validar_producto(self, nombre_producto):
        # Validar si un vendedor existe en la lista de vendedores
        producto_encontrado = next((p for p in ProductoDAO._productos if p.nombre_producto == nombre_producto), None)
        return producto_encontrado

    def validar_vendedor(self, documento_vendedor):
        # Validar si un vendedor existe en la lista de vendedores
        vendedor_encontrado = next((v for v in VendedorDAO._vendedores if v.documento_vendedor == documento_vendedor), None)
        return vendedor_encontrado



# Iniciar la aplicación
if __name__ == '__main__':
    tienda = Tienda("Mi Tienda", "123 Calle Principal", "555-555-5555", "www.mitienda.com")
    tienda.menu_interactivo()
