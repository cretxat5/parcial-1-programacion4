# ===============================================
# SISTEMA DE GESTIÓN DE EMPLEADOS
# ===============================================


def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número entero")


def leer_flotante(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número válido")

def leer_texto(mensaje):

    while True:

        valor = input(mensaje)

        if valor.replace(" ", "").isalpha():

            return valor.title()

        else:
            print("Error: solo se permiten letras")

# ----------------------------------------------
# CLASE EMPLEADO
# ----------------------------------------------

class Empleado:

    def __init__(self, nombre, id, salario_base, experiencia):

        self.nombre = nombre
        self.id = id
        self.salario_base = salario_base
        self.experiencia = experiencia


    def calcular_salario(self):

        if self.experiencia <= 2:
            bono = self.salario_base * 0.05

        elif self.experiencia <= 5:
            bono = self.salario_base * 0.10

        else:
            bono = self.salario_base * 0.15

        return self.salario_base + bono


    # REPRESENTACIÓN EN TEXTO
    def __str__(self):

        return f"Nombre: {self.nombre} | ID: {self.id} | Salario total: {self.calcular_salario():.2f}"


# ----------------------------------------------
# CLASE GESTOR
# ----------------------------------------------

class GestorEmpleados:

    def __init__(self):

        self.empleados = []


    def agregar_empleado(self, empleado):

        for emp in self.empleados:

            if emp.id == empleado.id:
                print("Error: ya existe un empleado con ese ID")
                return

        self.empleados.append(empleado)

        print("Empleado agregado correctamente")


    def eliminar_empleado(self, id):

        if not self.empleados:
            print("No hay empleados registrados.")
            return

        for empleado in self.empleados:

            if empleado.id == id:
                self.empleados.remove(empleado)
                print("Empleado eliminado")
                return

        print("Empleado no encontrado")


    def buscar_empleado(self, id):

        for empleado in self.empleados:

            if empleado.id == id:
                return empleado

        return None


    def editar_empleado(self, id):

        if not self.empleados:
            print("No hay empleados registrados para editar.")
            return

        empleado = self.buscar_empleado(id)

        if not empleado:
            print("Empleado no encontrado")
            return


        while True:

            print("\n--- EDITAR EMPLEADO ---")
            print("1. Cambiar nombre")
            print("2. Cambiar salario base")
            print("3. Cambiar experiencia")
            print("4. Salir")

            opcion = input("Seleccione: ")

            if opcion == "1":

                empleado.nombre = leer_texto("Nuevo nombre: ")
                print("Nombre actualizado")


            elif opcion == "2":

                empleado.salario_base = leer_flotante("Nuevo salario: ")
                print("Salario actualizado")


            elif opcion == "3":

                empleado.experiencia = leer_entero("Nueva experiencia (años): ")
                print("Experiencia actualizada")


            elif opcion == "4":
                break

            else:
                print("Opción inválida")


    def mostrar_empleados(self):

        if not self.empleados:
            print("No hay empleados registrados")
            return

        for empleado in self.empleados:
            print(empleado)


    # GUARDAR ARCHIVO
    def guardar_empleados(self, archivo):

        with open(archivo, "w") as f:

            for empleado in self.empleados:

                linea = f"{empleado.nombre},{empleado.id},{empleado.salario_base},{empleado.experiencia}\n"

                f.write(linea)

        print("Los datos fueron guardados correctamente.")


    # CARGAR ARCHIVO
    def cargar_empleados(self, archivo):

        try:

            self.empleados.clear()

            with open(archivo, "r") as f:

                for linea in f:

                    datos = linea.strip().split(",")

                    nombre = datos[0]
                    id = int(datos[1])
                    salario = float(datos[2])
                    experiencia = int(datos[3])

                    empleado = Empleado(nombre, id, salario, experiencia)

                    self.empleados.append(empleado)

            print("Empleados cargados correctamente.")

        except FileNotFoundError:

            print("No existe archivo previo.")
            
gestor = GestorEmpleados()

archivo = "empleados.txt"

gestor.cargar_empleados(archivo)

while True:

    print("\n====== MENU ======")
    print("1. Agregar empleado")
    print("2. Eliminar empleado")
    print("3. Buscar empleado")
    print("4. Editar empleado")
    print("5. Mostrar empleados")
    print("6. Guardar datos")
    print("7. Salir")

    opcion = input("Seleccione una opción: ")


    if opcion == "1":

        nombre = leer_texto("Nombre: ")
        id = leer_entero("ID: ")
        salario = leer_flotante("Salario base: ")
        experiencia = leer_entero("Experiencia (años): ")

        emp = Empleado(nombre, id, salario, experiencia)

        gestor.agregar_empleado(emp)

        gestor.guardar_empleados(archivo)


    elif opcion == "2":

        id = leer_entero("ID del empleado: ")

        gestor.eliminar_empleado(id)

        gestor.guardar_empleados(archivo)


    elif opcion == "3":

        id = leer_entero("ID del empleado: ")

        emp = gestor.buscar_empleado(id)

        if emp:
            print(emp)
        else:
            print("Empleado no encontrado")


    elif opcion == "4":

        id = leer_entero("ID del empleado a editar: ")

        gestor.editar_empleado(id)

        gestor.guardar_empleados(archivo)


    elif opcion == "5":

        gestor.mostrar_empleados()


    elif opcion == "6":

        gestor.guardar_empleados(archivo)


    elif opcion == "7":

        print("Saliendo del programa...")
        break


    else:

        print("Opción inválida")