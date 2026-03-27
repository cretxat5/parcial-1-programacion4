# ===============================================
# SISTEMA DE VENTAS - PARCIAL I
# ===============================================

import xml.etree.ElementTree as ET


# ----------------------------------------------
# FUNCIONES AUXILIARES DE LECTURA
# ----------------------------------------------

def leer_entero(mensaje):
    """Lee un número entero positivo con validación."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("Error: el valor no puede ser negativo")
                continue
            return valor
        except ValueError:
            print("Error: debe ingresar un número entero")


def leer_flotante(mensaje):
    """Lee un número flotante positivo con validación."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("Error: el valor no puede ser negativo")
                continue
            return valor
        except ValueError:
            print("Error: debe ingresar un número válido")


def leer_texto(mensaje):
    """Lee texto alfabético con validación."""
    while True:
        valor = input(mensaje)
        if valor.replace(" ", "").isalpha():
            return valor.title()
        else:
            print("Error: solo se permiten letras")


# ----------------------------------------------
# CLASES
# ----------------------------------------------

class Producto:
    """Clase que representa un producto en la tienda."""

    def __init__(self, nombre, id_producto, precio, cantidad):
        self.nombre = nombre
        self.id = id_producto
        self.precio = precio
        self.cantidad = cantidad

    def disminuir_inventario(self, cantidad):
        """Disminuye el inventario si hay stock suficiente."""
        if cantidad <= self.cantidad:
            self.cantidad -= cantidad
            return True
        else:
            print("No hay suficiente inventario")
            return False

    def aumentar_inventario(self, cantidad):
        """Aumenta el inventario de forma segura."""
        if cantidad < 0:
            print("Error: no se puede aumentar inventario con cantidad negativa")
            return False
        self.cantidad += cantidad
        return True

    def mostrar_informacion(self):
        """Muestra la información del producto."""
        print(f"Producto: {self.nombre}")
        print(f"ID: {self.id}")
        print(f"Precio: ${self.precio:.2f}")
        if self.cantidad == 0:
            print("Cantidad: Ya no hay existencias en inventario")
        else:
            print(f"Cantidad: {self.cantidad}")
        print("------------------")


class Cliente:
    """Clase que representa un cliente de la tienda."""

    def __init__(self, nombre, id_cliente, saldo):
        self.nombre = nombre
        self.id = id_cliente
        self.saldo = saldo

    def realizar_compra(self, producto: Producto, cantidad: int) -> bool:
        """Realiza una compra si se cumplen condiciones de stock y saldo."""
        costo = producto.precio * cantidad

        if cantidad > producto.cantidad:
            print("Error: no hay suficiente inventario")
            return False

        if costo > self.saldo:
            print("Error: saldo insuficiente")
            return False

        self.saldo -= costo
        producto.disminuir_inventario(cantidad)
        print("✓ Compra realizada exitosamente")
        return True

    def mostrar_informacion(self):
        """Muestra la información del cliente."""
        print(f"Cliente: {self.nombre}")
        print(f"ID: {self.id}")
        print(f"Saldo: ${self.saldo:.2f}")
        print("------------------")


class Tienda:
    """Clase gestora del sistema de ventas."""

    def __init__(self):
        """Inicializa la tienda con listas vacías."""
        self.productos = []
        self.clientes = []

    def agregar_producto(self, producto: Producto):
        """Agrega un nuevo producto a la lista de productos."""
        if any(p.id == producto.id for p in self.productos):
            print("Advertencia: ya existe un producto con ese ID")
            return False
        self.productos.append(producto)
        return True
    
    def aumentar_inventario_producto(self, id_producto: int, cantidad: int):
        """Aumenta el inventario de un producto buscándolo por ID."""
    
        producto_encontrado = next((p for p in self.productos if p.id == id_producto), None)

        if not producto_encontrado:
            print("Error: producto no encontrado")
            return False

        if producto_encontrado.aumentar_inventario(cantidad):
            print("✓ Inventario actualizado correctamente")
            return True

        return False

    def agregar_cliente(self, cliente: Cliente):
        """Agrega un cliente a la lista de clientes."""
        if any(c.id == cliente.id for c in self.clientes):
            print("Advertencia: ya existe un cliente con ese ID")
            return False
        self.clientes.append(cliente)
        return True

    def realizar_venta(self, id_cliente: int, id_producto: int, cantidad: int) -> bool:
        """Realiza una venta de un producto a un cliente."""
        cliente_encontrado = next((c for c in self.clientes if c.id == id_cliente), None)
        producto_encontrado = next((p for p in self.productos if p.id == id_producto), None)

        if not cliente_encontrado or not producto_encontrado:
            print("Error: cliente o producto no encontrado")
            return False

        return cliente_encontrado.realizar_compra(producto_encontrado, cantidad)

    def mostrar_productos(self):
        """Muestra todos los productos disponibles."""
        if not self.productos:
            print("No hay productos registrados.")
            return
        print("\n===== PRODUCTOS DISPONIBLES =====")
        for producto in self.productos:
            producto.mostrar_informacion()

    def mostrar_clientes(self):
        """Muestra todos los clientes registrados."""
        if not self.clientes:
            print("No hay clientes registrados.")
            return
        print("\n===== CLIENTES REGISTRADOS =====")
        for cliente in self.clientes:
            cliente.mostrar_informacion()

    def guardar_datos(self, archivo: str):
        """Guarda los productos y clientes en un archivo XML."""
        try:
            raiz = ET.Element("tienda")

            productos_xml = ET.SubElement(raiz, "productos")
            for p in self.productos:
                prod = ET.SubElement(productos_xml, "producto")
                ET.SubElement(prod, "nombre").text = p.nombre
                ET.SubElement(prod, "id").text = str(p.id)
                ET.SubElement(prod, "precio").text = str(p.precio)
                ET.SubElement(prod, "cantidad").text = str(p.cantidad)

            clientes_xml = ET.SubElement(raiz, "clientes")
            for c in self.clientes:
                cli = ET.SubElement(clientes_xml, "cliente")
                ET.SubElement(cli, "nombre").text = c.nombre
                ET.SubElement(cli, "id").text = str(c.id)
                ET.SubElement(cli, "saldo").text = str(c.saldo)

            arbol = ET.ElementTree(raiz)
            arbol.write(archivo, encoding="utf-8", xml_declaration=True)
            print(f"✓ Datos guardados en {archivo}")

        except Exception as e:
            print(f"Error al guardar XML: {e}")

    def cargar_datos(self, archivo: str):
        """Carga los productos y clientes desde un archivo XML."""
        try:
            arbol = ET.parse(archivo)
            raiz = arbol.getroot()

            self.productos.clear()
            self.clientes.clear()

            productos_elem = raiz.find("productos")
            if productos_elem is not None:
                for prod in productos_elem:
                    nombre = prod.find("nombre").text
                    id_producto = int(prod.find("id").text)
                    precio = float(prod.find("precio").text)
                    cantidad = int(prod.find("cantidad").text)
                    self.productos.append(Producto(nombre, id_producto, precio, cantidad))

            clientes_elem = raiz.find("clientes")
            if clientes_elem is not None:
                for cli in clientes_elem:
                    nombre = cli.find("nombre").text
                    id_cliente = int(cli.find("id").text)
                    saldo = float(cli.find("saldo").text)
                    self.clientes.append(Cliente(nombre, id_cliente, saldo))

            print(f"✓ Datos cargados desde {archivo}")

        except FileNotFoundError:
            print(f"Archivo '{archivo}' no encontrado")
        except Exception as e:
            print(f"Error al cargar XML: {e}")


# ====================
# PROGRAMA PRINCIPAL
# ====================

def main():
    """Función principal del sistema de ventas."""
    tienda = Tienda()

    while True:
        print("\n----- MENU TIENDA -----")
        print("1. Agregar producto")
        print("2. Agregar cliente")
        print("3. Realizar venta")
        print("4. Mostrar productos")
        print("5. Mostrar clientes")
        print("6. Guardar datos (XML)")
        print("7. Cargar datos (XML)")
        print("8. Aumentar inventario")
        print("9. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            nombre      = leer_texto("Nombre del producto: ")
            id_producto = leer_entero("ID del producto: ")
            precio      = leer_flotante("Precio: ")
            cantidad    = leer_entero("Cantidad en inventario: ")

            if cantidad < 0:
                print("Error: la cantidad no puede ser negativa")
                continue

            producto = Producto(nombre, id_producto, precio, cantidad)
            if tienda.agregar_producto(producto):
                print("✓ Producto agregado")

        elif opcion == "2":
            nombre     = leer_texto("Nombre del cliente: ")
            id_cliente = leer_entero("ID del cliente: ")
            saldo      = leer_flotante("Saldo del cliente: ")

            cliente = Cliente(nombre, id_cliente, saldo)
            if tienda.agregar_cliente(cliente):
                print("✓ Cliente agregado")

        elif opcion == "3":
            id_cliente  = leer_entero("ID del cliente: ")
            id_producto = leer_entero("ID del producto: ")
            cantidad    = leer_entero("Cantidad a comprar: ")
            tienda.realizar_venta(id_cliente, id_producto, cantidad)

        elif opcion == "4":
            tienda.mostrar_productos()

        elif opcion == "5":
            tienda.mostrar_clientes()

        elif opcion == "6":
            archivo = input("Nombre del archivo XML (ej: tienda.xml): ")
            tienda.guardar_datos(archivo)

        elif opcion == "7":
            archivo = input("Nombre del archivo XML a cargar: ")
            tienda.cargar_datos(archivo)

        elif opcion == "8":
            id_producto = leer_entero("ID del producto: ")
            cantidad = leer_entero("Cantidad a agregar al inventario: ") 
            tienda.aumentar_inventario_producto(id_producto, cantidad)

        elif opcion == "9":
            print("saliendo del sistema de ventas")
            break

        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()