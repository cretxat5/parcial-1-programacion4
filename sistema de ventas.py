# ===============================================
# SISTEMA DE VENTAS - PARCIAL I
# ===============================================

# Nota importante: para este ejercicio debe implementar archivos XML,
# la documentación quedará adjunta en la actividad de "parcial I".

import xml.etree.ElementTree as ET

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

    def agregar_cliente(self, cliente: Cliente):
        """Agrega un cliente a la lista de clientes."""
        if any(c.id == cliente.id for c in self.clientes):
            print("Advertencia: ya existe un cliente con ese ID")
            return False
        self.clientes.append(cliente)
        return True

    def realizar_venta(self, id_cliente: int, id_producto: int, cantidad: int) -> bool:
        """
        Realiza una venta de un producto a un cliente.
        Valida condiciones de stock y saldo.
        """
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
        """
        Guarda los productos y clientes en un archivo XML.
        Nota importante: implementa archivos XML como se requiere.
        """
        try:
            raiz = ET.Element("tienda")

            # Guardar productos
            productos_xml = ET.SubElement(raiz, "productos")
            for p in self.productos:
                prod = ET.SubElement(productos_xml, "producto")
                ET.SubElement(prod, "nombre").text = p.nombre
                ET.SubElement(prod, "id").text = str(p.id)
                ET.SubElement(prod, "precio").text = str(p.precio)
                ET.SubElement(prod, "cantidad").text = str(p.cantidad)

            # Guardar clientes
            clientes_xml = ET.SubElement(raiz, "clientes")
            for c in self.clientes:
                cli = ET.SubElement(clientes_xml, "cliente")
                ET.SubElement(cli, "nombre").text = c.nombre
                ET.SubElement(cli, "id").text = str(c.id)
                ET.SubElement(cli, "saldo").text = str(c.saldo)

            # Escribir archivo XML
            arbol = ET.ElementTree(raiz)
            arbol.write(archivo, encoding="utf-8", xml_declaration=True)
            print(f"✓ Datos guardados en {archivo}")

        except Exception as e:
            print(f"Error al guardar XML: {e}")

    def cargar_datos(self, archivo: str):
        """
        Carga los productos y clientes desde un archivo XML.
        Nota importante: implementa archivos XML como se requiere.
        """
        try:
            arbol = ET.parse(archivo)
            raiz = arbol.getroot()

            self.productos.clear()
            self.clientes.clear()

            # Cargar productos
            productos_elem = raiz.find("productos")
            if productos_elem is not None:
                for prod in productos_elem:
                    nombre = prod.find("nombre").text
                    id_producto = int(prod.find("id").text)
                    precio = float(prod.find("precio").text)
                    cantidad = int(prod.find("cantidad").text)
                    nuevo_producto = Producto(nombre, id_producto, precio, cantidad)
                    self.productos.append(nuevo_producto)

            # Cargar clientes
            clientes_elem = raiz.find("clientes")
            if clientes_elem is not None:
                for cli in clientes_elem:
                    nombre = cli.find("nombre").text
                    id_cliente = int(cli.find("id").text)
                    saldo = float(cli.find("saldo").text)
                    nuevo_cliente = Cliente(nombre, id_cliente, saldo)
                    self.clientes.append(nuevo_cliente)

            print(f"✓ Datos cargados desde {archivo}")

        except FileNotFoundError:
            print(f"Archivo '{archivo}' no encontrado")
        except Exception as e:
            print(f"Error al cargar XML: {e}")


# ====================
# PROGRAMA PRINCIPAL
# ====================

def main():
    """
    Función principal del sistema de ventas.
    
    Nota importante: para este ejercicio debe implementar archivos XML,
    la documentación quedará adjunta en la actividad de "parcial I".
    """
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
        print("8. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            try:
                nombre = input("Nombre del producto: ")
                id_producto = int(input("ID del producto: "))
                precio = float(input("Precio: "))
                cantidad = int(input("Cantidad en inventario: "))
                
                if precio < 0 or cantidad < 0:
                    print("Error: precio y cantidad no pueden ser negativos")
                    continue
                    
                producto = Producto(nombre, id_producto, precio, cantidad)
                if tienda.agregar_producto(producto):
                    print("✓ Producto agregado")
            except ValueError:
                print("Error: ingrese datos válidos")

        elif opcion == "2":
            try:
                nombre = input("Nombre del cliente: ")
                id_cliente = int(input("ID del cliente: "))
                saldo = float(input("Saldo del cliente: "))
                
                if saldo < 0:
                    print("Error: saldo no puede ser negativo")
                    continue
                    
                cliente = Cliente(nombre, id_cliente, saldo)
                if tienda.agregar_cliente(cliente):
                    print("✓ Cliente agregado")
            except ValueError:
                print("Error: ingrese datos válidos")

        elif opcion == "3":
            try:
                id_cliente = int(input("ID del cliente: "))
                id_producto = int(input("ID del producto: "))
                cantidad = int(input("Cantidad a comprar: "))
                tienda.realizar_venta(id_cliente, id_producto, cantidad)
            except ValueError:
                print("Error: ingrese datos válidos")

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
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()