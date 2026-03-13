# ===============================================
# SISTEMA DE CIFRADO Y DESCIFRADO CÉSAR
# Implementado con POO, Archivos y Listas
# ===============================================

import os
from datetime import datetime


class CifroCesar:
    """
    Clase que implementa el algoritmo de cifrado César.
    
    El cifrado César desplaza cada letra un número fijo de posiciones
    en el alfabeto. Por ejemplo, con desplazamiento 3:
    A → D, B → E, C → F, etc.
    """

    def __init__(self, desplazamiento=3):
        """
        Inicializa el cifrador César.
        
        Args:
            desplazamiento (int): Número de posiciones a desplazar (1-25)
        """
        if not (1 <= desplazamiento <= 25):
            raise ValueError("El desplazamiento debe estar entre 1 y 25")
        
        self.desplazamiento = desplazamiento
        self.alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.historial = []

    def cifrar(self, texto):
        """
        Cifra un texto usando el algoritmo César.
        
        Proceso:
        1. Convierte a mayúsculas
        2. Para cada carácter:
           - Si es letra: encuentra posición y suma desplazamiento
           - Si no es letra: mantiene igual
        3. Usa módulo 26 para "dar la vuelta" al alfabeto
        
        Args:
            texto (str): Texto a cifrar
            
        Returns:
            str: Texto cifrado
            
        Ejemplo:
            >>> cifrador = CifroCesar(3)
            >>> cifrador.cifrar("hola")
            'KROH'
        """
        texto_mayuscula = texto.upper()
        texto_cifrado = ""

        for caracter in texto_mayuscula:
            if caracter in self.alfabeto:
                # Encuentra la posición actual de la letra (0-25)
                posicion_actual = self.alfabeto.index(caracter)
                
                # Suma el desplazamiento y usa módulo 26
                nueva_posicion = (posicion_actual + self.desplazamiento) % 26
                
                # Obtiene la letra cifrada
                texto_cifrado += self.alfabeto[nueva_posicion]
            else:
                # Mantiene espacios, números y caracteres especiales
                texto_cifrado += caracter

        # Registra en historial
        self.historial.append({
            'tipo': 'Cifrado',
            'original': texto,
            'resultado': texto_cifrado,
            'desplazamiento': self.desplazamiento,
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return texto_cifrado

    def descifrar(self, texto_cifrado):
        """
        Descifra un texto que fue encriptado con César.
        
        Proceso:
        1. Invierte el desplazamiento (resta en lugar de sumar)
        2. Usa módulo 26 para manejar números negativos
        3. Recupera el texto original
        
        Args:
            texto_cifrado (str): Texto cifrado
            
        Returns:
            str: Texto descifrado
            
        Ejemplo:
            >>> cifrador = CifroCesar(3)
            >>> cifrador.descifrar("KROH")
            'HOLA'
        """
        texto_mayuscula = texto_cifrado.upper()
        texto_descifrado = ""

        for caracter in texto_mayuscula:
            if caracter in self.alfabeto:
                # Encuentra la posición actual
                posicion_actual = self.alfabeto.index(caracter)
                
                # RESTA el desplazamiento (inverso del cifrado)
                # El módulo 26 maneja correctamente los números negativos
                nueva_posicion = (posicion_actual - self.desplazamiento) % 26
                
                # Obtiene la letra descifrada
                texto_descifrado += self.alfabeto[nueva_posicion]
            else:
                # Mantiene espacios, números y caracteres especiales
                texto_descifrado += caracter

        # Registra en historial
        self.historial.append({
            'tipo': 'Descifrado',
            'original': texto_cifrado,
            'resultado': texto_descifrado,
            'desplazamiento': self.desplazamiento,
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return texto_descifrado

    def obtener_historial(self):
        """Retorna la lista de operaciones realizadas."""
        return self.historial

    def mostrar_historial(self):
        """Muestra el historial en formato legible."""
        if not self.historial:
            print("No hay operaciones en el historial.")
            return

        print("\n" + "="*70)
        print("HISTORIAL DE OPERACIONES")
        print("="*70)
        
        for i, operacion in enumerate(self.historial, 1):
            print(f"\n{i}. {operacion['tipo']}")
            print(f"   Original:       {operacion['original']}")
            print(f"   Resultado:      {operacion['resultado']}")
            print(f"   Desplazamiento: {operacion['desplazamiento']}")
            print(f"   Fecha:          {operacion['fecha']}")

    def limpiar_historial(self):
        """Limpia el historial de operaciones."""
        self.historial.clear()
        print("Historial limpiado.")

    def cambiar_desplazamiento(self, nuevo_desplazamiento):
        """Cambia el desplazamiento actual."""
        if not (1 <= nuevo_desplazamiento <= 25):
            raise ValueError("El desplazamiento debe estar entre 1 y 25")
        self.desplazamiento = nuevo_desplazamiento
        print(f"Desplazamiento cambiadoa {nuevo_desplazamiento}")


class GestorArchivos:
    """
    Clase que gestiona la lectura y escritura de archivos
    para el cifrado César.
    """

    @staticmethod
    def leer_archivo(ruta):
        """
        Lee el contenido de un archivo.
        
        Args:
            ruta (str): Ruta del archivo
            
        Returns:
            str: Contenido del archivo
        """
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
            print(f"✓ Archivo '{ruta}' leído correctamente.")
            return contenido
        except FileNotFoundError:
            print(f"Error: Archivo '{ruta}' no encontrado.")
            return None
        except Exception as e:
            print(f"Error al leer archivo: {e}")
            return None

    @staticmethod
    def guardar_archivo(ruta, contenido):
        """
        Guarda contenido en un archivo.
        
        Args:
            ruta (str): Ruta del archivo
            contenido (str): Contenido a guardar
        """
        try:
            with open(ruta, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido)
            print(f"✓ Archivo '{ruta}' guardado correctamente.")
        except Exception as e:
            print(f"Error al guardar archivo: {e}")

    @staticmethod
    def guardar_historial(ruta, historial):
        """
        Guarda el historial en un archivo de texto.
        
        Args:
            ruta (str): Ruta del archivo
            historial (list): Lista de operaciones
        """
        try:
            with open(ruta, 'w', encoding='utf-8') as archivo:
                archivo.write("HISTORIAL DE CIFRADO CÉSAR\n")
                archivo.write("=" * 70 + "\n\n")
                
                for i, operacion in enumerate(historial, 1):
                    archivo.write(f"{i}. {operacion['tipo']}\n")
                    archivo.write(f"   Original:       {operacion['original']}\n")
                    archivo.write(f"   Resultado:      {operacion['resultado']}\n")
                    archivo.write(f"   Desplazamiento: {operacion['desplazamiento']}\n")
                    archivo.write(f"   Fecha:          {operacion['fecha']}\n\n")
            
            print(f"✓ Historial guardado en '{ruta}'.")
        except Exception as e:
            print(f"Error al guardar historial: {e}")


class MenuSistema:
    """
    Clase que gestiona la interfaz del menú interactivo.
    """

    def __init__(self):
        """Inicializa el sistema con un cifrador César."""
        self.cifrador = CifroCesar(3)
        self.gestor = GestorArchivos()

    def mostrar_menu_principal(self):
        """Muestra el menú principal."""
        print("\n" + "="*70)
        print("SISTEMA DE CIFRADO Y DESCIFRADO CÉSAR")
        print("="*70)
        print("1. Cifrar texto directo")
        print("2. Descifrar texto directo")
        print("3. Cifrar archivo")
        print("4. Descifrar archivo")
        print("5. Ver historial")
        print("6. Guardar historial")
        print("7. Cambiar desplazamiento")
        print("8. Limpiar historial")
        print("9. Ver información")
        print("10. Salir")
        print("="*70)

    def opcion_cifrar_directo(self):
        """Opción para cifrar texto directo."""
        texto = input("Ingrese el texto a cifrar: ")
        resultado = self.cifrador.cifrar(texto)
        print(f"\n✓ Texto cifrado: {resultado}\n")

    def opcion_descifrar_directo(self):
        """Opción para descifrar texto directo."""
        texto = input("Ingrese el texto a descifrar: ")
        resultado = self.cifrador.descifrar(texto)
        print(f"\n✓ Texto descifrado: {resultado}\n")

    def opcion_cifrar_archivo(self):
        """Opción para cifrar un archivo."""
        ruta_entrada = input("Ingrese la ruta del archivo a cifrar: ")
        contenido = self.gestor.leer_archivo(ruta_entrada)
        
        if contenido:
            contenido_cifrado = self.cifrador.cifrar(contenido)
            ruta_salida = input("Ingrese la ruta para guardar el archivo cifrado: ")
            self.gestor.guardar_archivo(ruta_salida, contenido_cifrado)

    def opcion_descifrar_archivo(self):
        """Opción para descifrar un archivo."""
        ruta_entrada = input("Ingrese la ruta del archivo a descifrar: ")
        contenido = self.gestor.leer_archivo(ruta_entrada)
        
        if contenido:
            contenido_descifrado = self.cifrador.descifrar(contenido)
            ruta_salida = input("Ingrese la ruta para guardar el archivo descifrado: ")
            self.gestor.guardar_archivo(ruta_salida, contenido_descifrado)

    def opcion_ver_historial(self):
        """Opción para ver el historial."""
        self.cifrador.mostrar_historial()

    def opcion_guardar_historial(self):
        """Opción para guardar el historial."""
        ruta = input("Ingrese la ruta para guardar el historial: ")
        self.gestor.guardar_historial(ruta, self.cifrador.obtener_historial())

    def opcion_cambiar_desplazamiento(self):
        """Opción para cambiar el desplazamiento."""
        try:
            nuevo_desp = int(input("Ingrese nuevo desplazamiento (1-25): "))
            self.cifrador.cambiar_desplazamiento(nuevo_desp)
        except ValueError:
            print("Error: Ingrese un número válido entre 1 y 25.")

    def opcion_limpiar_historial(self):
        """Opción para limpiar el historial."""
        confirmacion = input("¿Está seguro? (S/N): ").upper()
        if confirmacion == 'S':
            self.cifrador.limpiar_historial()



    def ejecutar(self):
        """Ejecuta el menú principal."""
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.opcion_cifrar_directo()
            elif opcion == "2":
                self.opcion_descifrar_directo()
            elif opcion == "3":
                self.opcion_cifrar_archivo()
            elif opcion == "4":
                self.opcion_descifrar_archivo()
            elif opcion == "5":
                self.opcion_ver_historial()
            elif opcion == "6":
                self.opcion_guardar_historial()
            elif opcion == "7":
                self.opcion_cambiar_desplazamiento()
            elif opcion == "8":
                self.opcion_limpiar_historial()
            
            elif opcion == "10":
                
                break
            else:
                print("Opción no válida. Intente de nuevo.")


# ===============================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ===============================================

if __name__ == "__main__":
    sistema = MenuSistema()
    sistema.ejecutar()
