from comercio import Comercio
# Crear una instancia de la clase Comercio
comercio = Comercio('Supertienda Tropicana', 'Cra. 81c #1-23', '3115013540', 'www.latropicana.com')

# Crear un encabezado con guiones para el nombre del comercio
nombre_comercio = comercio.nombre_negocio.center(len(comercio.nombre_negocio) + 30, '-')
print(nombre_comercio)


# Inicio del menú interactivo
while True:
    comercio.menu_interactivo()
    continuar = input('¿Desea realizar más operaciones= (S/N): ').strip().upper()
    if continuar != 'S':
        break



