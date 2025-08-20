import arbol_b
import os
import msvcrt as mv
import time
import random

#Variables a utilizar
menu = True
contador = 10
arbol = arbol_b.BTree(16)

#Datos requeridos (10)
proveedores  = [(1,"Mario","Electricista",4,"50"),
                (2,"Juan","Plomero",3,"100"),
                (3,"Pedro","Carpintero",2,"150"),
                (4,"Luis","Albañil",1,"200"),
                (5,"Carlos","Herrero",5,"250"),
                (6,"Marco","Electricista",4,"300"),
                (7,"Juan","Plomero",3,"350"),
                (8,"Jose","Carpintero",2,"400"),
                (9,"Luis","Albañil",1,"450"),
                (10,"Carlos","Herrero",5,"500")]

for proveedor in proveedores:
    arbol.insert(arbol_b.Proveedor(proveedor[0], proveedor[1], proveedor[2], proveedor[3], proveedor[4]))

# Lista lineal para comparación
lista_lineal = [arbol_b.Proveedor(p[0], p[1], p[2], p[3], p[4]) for p in proveedores]

#Funciones
def agregar_datos_masivos():
    try:
        print("AGREGANDO DATOS MASIVOS")
        print("------------------------")
        print("Generando 1000 proveedores aleatorios...")
        
        nombres = ["Ana", "Carlos", "David", "Elena", "Fernando", "Gabriela", "Hector", "Isabel", 
                  "Jorge", "Karen", "Luis", "Maria", "Nicolas", "Olivia", "Pablo", "Rosa", 
                  "Santiago", "Teresa", "Uriel", "Valeria", "Walter", "Ximena", "Yolanda", "Zacarias"]
        
        servicios = ["Electricista", "Plomero", "Carpintero", "Albañil", "Herrero"]
        
        for i in range(1000):
            id_proveedor = generar_id()
            nombre = random.choice(nombres) + " " + str(random.randint(1, 999))
            servicio = random.choice(servicios)
            calificacion = random.randint(1, 5)
            ubicacion = str(random.randint(1, 1000))
            
            proveedor = arbol_b.Proveedor(id_proveedor, nombre, servicio, calificacion, ubicacion)
            arbol.insert(proveedor)
            lista_lineal.append(proveedor)
            
            if (i + 1) % 100 == 0:
                print(f"Progreso: {i + 1}/1000 proveedores agregados")
        
        print(f"\n¡Datos masivos agregados exitosamente!")
        print(f"Total de proveedores en el sistema: {len(lista_lineal)}")
        
    except Exception as e:
        print(f"Error al agregar datos masivos: {e}")
        print("Inténtelo de nuevo.")

def registrar_trabajador():
    try:
        print("REGISTRO")
        print("----------------------")
        print("Ingrese los siguientes datos:")
        
        id_proveedor = generar_id()

        while True:
            nombre = input("Nombre: ").strip()
            if nombre and len(nombre) > 0:
                break
            print("Error: El nombre no puede estar vacío. Inténtelo de nuevo.")
        
        servicio = definir_servicio()
        calificacion = definir_calificacion()
        
        while True:
            ubicacion = input("Ubicación (km): ").strip()
            if ubicacion and len(ubicacion) > 0:
                break
            print("Error: La ubicación no puede estar vacía. Inténtelo de nuevo.")
        
        proveedor = arbol_b.Proveedor(id_proveedor, nombre, servicio, calificacion, ubicacion)
        arbol.insert(proveedor)
        lista_lineal.append(proveedor)
        print("Proveedor agregado correctamente!")
        
    except Exception as e:
        print(f"Error al registrar proveedor: {e}")
        print("Inténtelo de nuevo.")

def busqueda_trabajador():
    try:
        servicio = definir_servicio()
        resultados = arbol.search_by_service(servicio)
        if len(resultados) == 0:
            print("No se encontraron resultados")
        else:
            print("Resultados encontrados:")
            for resultado in resultados:
                print(resultado)
    except Exception as e:
        print(f"Error en la búsqueda: {e}")
        print("Inténtelo de nuevo.")

def listado_proveedores():
    try:
        arbol.traverse_inorder()
    except Exception as e:
        print(f"Error al mostrar la lista: {e}")
        print("Inténtelo de nuevo.")

def comparacion_busquedas():
    try:
        print("COMPARACIÓN DE BÚSQUEDAS")
        print("-------------------------")
        
        servicio = definir_servicio()
        
        print(f"\nBuscando proveedores de servicio: {servicio}")
        print("=" * 50)
        
        # Búsqueda en árbol B
        print("BÚSQUEDA EN ÁRBOL B:")
        inicio = time.perf_counter()  
        resultados_arbol = arbol.search_by_service(servicio)
        tiempo_arbol = time.perf_counter() - inicio
        
        if len(resultados_arbol) > 0:
            print(f"Tiempo: {tiempo_arbol:.9f} segundos")
            print("Resultados ordenados por calificación:")
            for resultado in resultados_arbol:
                print(f"  - {resultado}")
        else:
            print("No se encontraron resultados")
        
        print("\n" + "=" * 50)
        
        # Búsqueda lineal
        print("BÚSQUEDA LINEAL:")
        inicio = time.perf_counter() 
        resultados_lineal = []
        for proveedor in lista_lineal:
            if proveedor.tipo_servicio.lower() == servicio.lower():
                resultados_lineal.append(proveedor)
        tiempo_lineal = time.perf_counter() - inicio
        
        if len(resultados_lineal) > 0:
            print(f"Tiempo: {tiempo_lineal:.9f} segundos")
            print("Resultados encontrados:")
            for resultado in resultados_lineal:
                print(f"  - {resultado}")
        else:
            print("No se encontraron resultados")
        
        print("\n" + "=" * 50)
        print("ANÁLISIS DE RENDIMIENTO:")
        
        if len(resultados_arbol) > 0 and len(resultados_lineal) > 0:
            if tiempo_arbol > 0 and tiempo_lineal > 0:
                if tiempo_arbol < tiempo_lineal:
                    ratio = tiempo_lineal / tiempo_arbol
                    print(f"El árbol B es {ratio:.2f} veces más rápido")
                else:
                    ratio = tiempo_arbol / tiempo_lineal
                    print(f"La búsqueda lineal es {ratio:.2f} veces más rápida")
            elif tiempo_arbol == 0 and tiempo_lineal > 0:
                print("El árbol B es instantáneo (tiempo < 0.000001 segundos)")
            elif tiempo_lineal == 0 and tiempo_arbol > 0:
                print("La búsqueda lineal es instantánea (tiempo < 0.000001 segundos)")
            else:
                print("Ambas búsquedas son instantáneas (tiempo < 0.000001 segundos)")
        else:
            print("No hay suficientes resultados para comparar rendimiento")
        
        print(f"Total de proveedores en el sistema: {len(lista_lineal)}")
        
    except Exception as e:
        print(f"Error en la comparación: {e}")
        print("Inténtelo de nuevo.")

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
        print("Escoja la calificación del proveedor")
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

try:
    while menu:
        os.system("cls")
        print("Menú")
        print("-------------------------")
        print("1. Registrar trabajador")
        print("2. Búsqueda de trabajador por tipo de servicio")
        print("3. Listar trabajadores")
        print("4. Comparación: Búsqueda Lineal vs Árbol B")
        print("5. Agregar datos masivos (1000 proveedores)")
        print("6. Salir")
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
                comparacion_busquedas()
            case "5":
                agregar_datos_masivos()
            case "6":
                menu = False
                print("Gracias por utilizar este sistema")
            case _:
                print("Valor no válido. Inténtelo de nuevo.")
        mv.getch()
        
except KeyboardInterrupt:
    print("\n\nPrograma interrumpido por el usuario.")
    print("Gracias por utilizar este sistema")
except Exception as e:
    print(f"\nError crítico del sistema: {e}")
    print("El programa se cerrará por seguridad.")
finally:
    print("Programa finalizado.")


    