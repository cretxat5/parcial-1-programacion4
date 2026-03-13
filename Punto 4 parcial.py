while True:
    try:
        numero = int(input("Ingrese un numero entero de 4 cifras: "))

        if numero >= 1000 and numero <= 9999:

            # Descomponer el número
            primer = numero // 1000
            segundo = (numero // 100) % 10
            tercero = (numero // 10) % 10
            cuarto = numero % 10

            # Suma del segundo y tercer número
            suma = segundo + tercero

            # Verificar si el primero es múltiplo del cuarto
            if cuarto != 0 and primer % cuarto == 0:
                print("El primer numero es multiplo del cuarto numero")
            else:
                print("El primer numero NO es multiplo del cuarto numero")

            print("La suma del segundo y tercer numero es:", suma)

            # Preguntar si desea continuar
            continuar = input("¿Desea ingresar otro numero? (Si/No): ")

            if continuar.lower() != "si":
                print("Programa finalizado.")
                break

        else:
            print("El numero debe tener exactamente 4 cifras. Intente nuevamente.\n")

    except ValueError:
        print("Debe ingresar un numero entero. Intente nuevamente.\n")
