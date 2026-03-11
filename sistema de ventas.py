import xml.etree.ElementTree as ET

class Producto:

    def __init__(self, nombre, id_producto, precio, cantidad):
        self.nombre = nombre
        self.id = id_producto
        self.precio = precio
        self.cantidad = cantidad

    def disminuir_inventario(self, cantidad):
        if cantidad <= self.cantidad:
            self.cantidad -= cantidad
        else:
            print("No hay suficiente inventario")

    def aumentar_inventario(self, cantidad):
        self.cantidad += cantidad

    def mostrar_informacion(self):
        print("Producto:", self.nombre)
        print("ID:", self.id)
        print("Precio:", self.precio)
        print("Cantidad:", self.cantidad)
        print("------------------")


class Cliente:

    def __init__(self, nombre, id_cliente, saldo):
        self.nombre = nombre
        self.id = id_cliente
        self.saldo = saldo

    def realizar_compra(self, producto, cantidad):

        costo = producto.precio * cantidad

        if cantidad > producto.cantidad:
            print("No hay suficiente inventario")
            return

        if costo > self.saldo:
            print("Saldo insuficiente")
            return

        self.saldo -= costo
        producto.disminuir_inventario(cantidad)

        print("Compra realizada")

    def mostrar_informacion(self):
        print("Cliente:", self.nombre)
        print("ID:", self.id)
        print("Saldo:", self.saldo)
        print("------------------")


class Tienda:

    def __init__(self):
        self.productos = []
        self.clientes = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def realizar_venta(self, id_cliente, id_producto, cantidad):

        cliente_encontrado = None
        producto_encontrado = None

        for cliente in self.clientes:
            if cliente.id == id_cliente:
                cliente_encontrado = cliente

        for producto in self.productos:
            if producto.id == id_producto:
                producto_encontrado = producto

        if cliente_encontrado and producto_encontrado:
            cliente_encontrado.realizar_compra(producto_encontrado, cantidad)
        else:
            print("Cliente o producto no encontrado")

    def mostrar_productos(self):

        for producto in self.productos:
            producto.mostrar_informacion()

    def mostrar_clientes(self):

        for cliente in self.clientes:
            cliente.mostrar_informacion()

    def guardar_datos(self, archivo):

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
        arbol.write(archivo)

    def cargar_datos(self, archivo):

        arbol = ET.parse(archivo)
        raiz = arbol.getroot()

        for prod in raiz.find("productos"):
            nombre = prod.find("nombre").text
            id_producto = int(prod.find("id").text)
            precio = float(prod.find("precio").text)
            cantidad = int(prod.find("cantidad").text)

            nuevo_producto = Producto(nombre, id_producto, precio, cantidad)
            self.productos.append(nuevo_producto)

        for cli in raiz.find("clientes"):
            nombre = cli.find("nombre").text
            id_cliente = int(cli.find("id").text)
            saldo = float(cli.find("saldo").text)

            nuevo_cliente = Cliente(nombre, id_cliente, saldo)
            self.clientes.append(nuevo_cliente)
            
tienda = Tienda()

while True:

    print("\n----- MENU TIENDA -----")
    print("1. Agregar producto")
    print("2. Agregar cliente")
    print("3. Realizar venta")
    print("4. Mostrar productos")
    print("5. Mostrar clientes")
    print("6. Guardar datos")
    print("7. Cargar datos")
    print("8. Salir")

    opcion = input("Seleccione una opcion: ")

    if opcion == "1":

        nombre = input("Nombre del producto: ")
        id_producto = int(input("ID del producto: "))
        precio = float(input("Precio: "))
        cantidad = int(input("Cantidad en inventario: "))

        producto = Producto(nombre, id_producto, precio, cantidad)

        tienda.agregar_producto(producto)

        print("Producto agregado")

    elif opcion == "2":

        nombre = input("Nombre del cliente: ")
        id_cliente = int(input("ID del cliente: "))
        saldo = float(input("Saldo del cliente: "))

        cliente = Cliente(nombre, id_cliente, saldo)

        tienda.agregar_cliente(cliente)

        print("Cliente agregado")

    elif opcion == "3":

        id_cliente = int(input("ID del cliente: "))
        id_producto = int(input("ID del producto: "))
        cantidad = int(input("Cantidad a comprar: "))

        tienda.realizar_venta(id_cliente, id_producto, cantidad)

    elif opcion == "4":

        tienda.mostrar_productos()

    elif opcion == "5":

        tienda.mostrar_clientes()

    elif opcion == "6":

        archivo = input("Nombre del archivo XML: ")
        tienda.guardar_datos(archivo)

        print("Datos guardados")

    elif opcion == "7":

        archivo = input("Nombre del archivo XML: ")
        tienda.cargar_datos(archivo)

        print("Datos cargados")

    elif opcion == "8":

        print("Saliendo del sistema")
        break

    else:

        print("Opcion no valida")
        