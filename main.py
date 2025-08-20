import arbol_b
import os
import msvcrt as mv

#Variables a utilizar
menu = True
contador = 0
arbol = arbol_b.BTree(4)

#Funciones
def registrar_trabajador():
    print("REGISTRO")
    print("----------------------")
    print("Ingrese los siguientes datos:")
    id_proveedor = generar_id()
    nombre = input("Nombre: ")
    servicio = definir_servicio()
    calificacion = definir_calificacion()
    ubicacion = input("Ubicación: ")
    proveedor = arbol_b.Proveedor(id_proveedor, nombre, servicio, calificacion, ubicacion)
    arbol.insert(proveedor)
    print("Proveedor agregado correctamente!")

def busqueda_trabajador():
    servicio = definir_servicio()
    resultados = arbol.search_by_service(servicio)
    if len(resultados) == 0:
        print("No se encontraron resultados")
    else:
        print(resultados)

def listado_proveedores():
    arbol.traverse_inorder()

def definir_servicio():
    while True:
        os.system("cls")
        print("A cuál de los siguientes servicios pertenece?")
        print("1. Electricista")
        print("2. Plomero")
        print("3. Carpintero")
        print("4. Albañil")
        print("5. Herrero")
        respuesta_usuario = input("Ingrese el número de la opción: ")

        match respuesta_usuario:
            case "1":
                return "Electricista"
            case "2":
                return "Plomero"
            case "3":
                return "Carpintero"
            case "4":
                return "Albañil"
            case "5":
                return "Herrero"
            case _:
                print("Opción no reconocida, inténtelo de nuevo.")
        mv.getch()
        os.system("cls")

            
def definir_calificacion():
    while True:
        os.system("cls")
        print("Escoja la reputación del proveedor")
        print("1. Muy baja")
        print("2. Baja")
        print("3. Normal")
        print("4. Buena")
        print("5. Excelente")
        respuesta_usuario = input("Ingrese el número de la opción: ")

        match respuesta_usuario:
            case "1":
                return 1
            case "2":
                return 2
            case "3":
                return 3
            case "4":
                return 4
            case "5":
                return 5
            case _:
                print("Opción no reconocida, inténtelo de nuevo.")
        mv.getch()
        os.system("cls")
        
        
def generar_id():
    global contador
    contador += 1
    return contador


#Programa principal

while menu:
    os.system("cls")
    print("Menú")
    print("-------------------------")
    print("1. Registrar trabajador")
    print("2. Búsqueda de trabajador por tipo de servicio")
    print("3. Listar trabajadores")
    print("4. Salir")
    input_usuario = input("Escriba su opción: ")
    os.system("cls")

    match input_usuario:
        case "1":
            registrar_trabajador()
        case "2":
            busqueda_trabajador()           
        case "3":
            listado_proveedores()
        case "4":
            menu = False
            print("Gracias por utilizar este sistema")
        case _:
            print("Valor no válido. Inténtelo de nuevo.")
    mv.getch()


    