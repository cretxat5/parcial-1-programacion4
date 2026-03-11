# ===============================================
# SISTEMA DE GESTIÓN DE EMPLEADOS
# ===============================================


def leer_entero(mensaje):
    """Lee un número entero con validación."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número entero")


def leer_flotante(mensaje):
    """Lee un número flotante con validación."""
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
# CLASE EMPLEADO
# ----------------------------------------------

class Empleado:
    """Clase que representa un empleado con sus datos básicos."""

    def __init__(self, nombre, id_empleado, salario_base, experiencia):
        """
        Inicializa un empleado.
        
        Args:
            nombre: Nombre del empleado
            id_empleado: ID único del empleado
            salario_base: Salario base en pesos
            experiencia: Años de experiencia
        """
        if salario_base < 0 or experiencia < 0:
            raise ValueError("Salario y experiencia no pueden ser negativos")
        
        self.nombre = nombre
        self.id_empleado = id_empleado
        self.salario_base = salario_base
        self.experiencia = experiencia

    def calcular_salario(self):
        """Calcula el salario total con bono según experiencia."""
        if self.experiencia <= 2:
            bono = self.salario_base * 0.05
        elif self.experiencia <= 5:
            bono = self.salario_base * 0.10
        else:
            bono = self.salario_base * 0.15

        return self.salario_base + bono

    def __str__(self):
        """Representación en texto del empleado."""
        return (f"Nombre: {self.nombre} | ID: {self.id_empleado} | "
                f"Salario total: {self.calcular_salario():.2f}")


# ----------------------------------------------
# CLASE GESTOR
# ----------------------------------------------

class GestorEmpleados:
    """Clase que gestiona la colección de empleados."""

    def __init__(self):
        """Inicializa el gestor con una lista vacía de empleados."""
        self.empleados = []

    def agregar_empleado(self, empleado):
        """Agrega un nuevo empleado si no existe uno con el mismo ID."""
        if any(emp.id_empleado == empleado.id_empleado for emp in self.empleados):
            print("Error: ya existe un empleado con ese ID")
            return

        self.empleados.append(empleado)
        print("Empleado agregado correctamente")

    def eliminar_empleado(self, id_empleado):
        """Elimina un empleado por su ID."""
        if not self.empleados:
            print("No hay empleados registrados.")
            return

        empleado = self.buscar_empleado(id_empleado)
        
        if empleado:
            self.empleados.remove(empleado)
            print("Empleado eliminado")
        else:
            print("Empleado no encontrado")

    def buscar_empleado(self, id_empleado):
        """Busca un empleado por su ID."""
        for empleado in self.empleados:
            if empleado.id_empleado == id_empleado:
                return empleado
        return None

    def editar_empleado(self, id_empleado):
        """Permite editar los datos de un empleado existente."""
        if not self.empleados:
            print("No hay empleados registrados para editar.")
            return

        empleado = self.buscar_empleado(id_empleado)

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
        """Muestra todos los empleados registrados."""
        if not self.empleados:
            print("No hay empleados registrados")
            return

        for empleado in self.empleados:
            print(empleado)

    def guardar_empleados(self, archivo):
        """Guarda los empleados en un archivo CSV."""
        try:
            with open(archivo, "w") as f:
                for empleado in self.empleados:
                    linea = (f"{empleado.nombre},{empleado.id_empleado},"
                             f"{empleado.salario_base},{empleado.experiencia}\n")
                    f.write(linea)
            print("Los datos fueron guardados correctamente.")
        except IOError as e:
            print(f"Error al guardar el archivo: {e}")

    def cargar_empleados(self, archivo):
        """Carga empleados desde un archivo CSV."""
        try:
            self.empleados.clear()

            with open(archivo, "r") as f:
                for linea in f:
                    datos = linea.strip().split(",")
                    
                    if len(datos) != 4:
                        print(f"Advertencia: línea mal formada ignorada: {linea}")
                        continue

                    try:
                        nombre = datos[0]
                        id_empleado = int(datos[1])
                        salario = float(datos[2])
                        experiencia = int(datos[3])

                        empleado = Empleado(nombre, id_empleado, salario, experiencia)
                        self.empleados.append(empleado)
                    except (ValueError, IndexError) as e:
                        print(f"Advertencia: error en línea {linea.strip()}: {e}")
                        continue

            print("Empleados cargados correctamente.")

        except FileNotFoundError:
            print("No existe archivo previo.")


# ===============================================
# PROGRAMA PRINCIPAL
# ===============================================

def main():
    """Función principal que ejecuta el menú del sistema."""
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
            id_empleado = leer_entero("ID: ")
            salario = leer_flotante("Salario base: ")
            experiencia = leer_entero("Experiencia (años): ")

            try:
                emp = Empleado(nombre, id_empleado, salario, experiencia)
                gestor.agregar_empleado(emp)
                gestor.guardar_empleados(archivo)
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "2":
            id_empleado = leer_entero("ID del empleado: ")
            gestor.eliminar_empleado(id_empleado)
            gestor.guardar_empleados(archivo)

        elif opcion == "3":
            id_empleado = leer_entero("ID del empleado: ")
            emp = gestor.buscar_empleado(id_empleado)

            if emp:
                print(emp)
            else:
                print("Empleado no encontrado")

        elif opcion == "4":
            id_empleado = leer_entero("ID del empleado a editar: ")
            gestor.editar_empleado(id_empleado)
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


if __name__ == "__main__":
    main()
    