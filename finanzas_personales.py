import csv
import matplotlib.pyplot as plt
from datetime import datetime
from unidecode import unidecode
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# Variable que almacena la versión del programa
version = "1.2"

# Lista de categorías permitidas
categorias_permitidas = ["Sueldo", "Alimentacion", "Impuestos", "Alquiler", "Otros"]

# Inicializa una lista para almacenar los datos financieros (ingresos y gastos)
registros_financieros = []

def cargar_datos():
    try:
        with open("registros_financieros.csv", newline="", mode="r") as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)
            for row in lector_csv:
                registros_financieros.append(row)
        print("Datos cargados con éxito.")
    except FileNotFoundError:
        print("No se encontró un archivo de datos existente. Se creará uno nuevo.")

def guardar_datos():
    with open("registros_financieros.csv", newline="", mode="w") as archivo_csv:
        campos = ["Fecha", "Tipo", "Descripción", "Categoría", "Monto"]
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)

        escritor_csv.writeheader()
        escritor_csv.writerows(registros_financieros)

def agregar_registro():
    # Solicita al usuario ingresar detalles sobre un ingreso o gasto
    fecha = input("Fecha (AAAA-MM-DD): ")
    tipo = input("Tipo (ingreso/gasto): ")
    descripcion = input("Descripción: ")
    
    # Solicita la categoría y verifica si es válida
    while True:
        categoria = input("Categoría (Sueldo/Alimentación/Impuestos/Alquiler/Otros): ")
        categoria = unidecode(categoria).capitalize()  # Normalizar y capitalizar la categoría
        if categoria in categorias_permitidas:
            break
        else:
            print("Categoría no válida. Las categorías permitidas son: Sueldo, Alimentación, Impuestos, Alquiler, Otros.")

    monto = float(input("Monto: "))

    # Crea un diccionario para representar el registro financiero
    registro = {
        "Fecha": fecha,
        "Tipo": tipo,
        "Descripción": descripcion,
        "Categoría": categoria,
        "Monto": monto
    }

    # Agrega el registro a la lista de registros financieros
    registros_financieros.append(registro)
    print("Registro agregado con éxito.")
    guardar_datos()

def calcular_totales():
    total_ingresos = sum(float(registro["Monto"]) for registro in registros_financieros if registro["Tipo"] == "ingreso")
    total_gastos = sum(float(registro["Monto"]) for registro in registros_financieros if registro["Tipo"] == "gasto")
    saldo_actual = total_ingresos - total_gastos

    print(f"Total de Ingresos: {total_ingresos}")
    print(f"Total de Gastos: {total_gastos}")
    print(f"Saldo Actual: {saldo_actual}")

    if saldo_actual >= 0:
        print("Estás en saldo positivo.")
    else:
        print("Estás en saldo negativo.")

def generar_grafico_torta():
    total_gastos = sum(float(registro["Monto"]) for registro in registros_financieros if registro["Tipo"] == "gasto")
    saldo_actual = sum(float(registro["Monto"]) for registro in registros_financieros if registro["Tipo"] == "ingreso") - total_gastos

    # Crear una lista con los datos para el gráfico de torta
    datos = [total_gastos, saldo_actual]
    categorias = ["Gastos", "Saldo Actual"]

    # Crear el gráfico de torta
    plt.figure(figsize=(8, 8))
    plt.pie(datos, labels=categorias, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Aspecto igual para asegurar que el gráfico sea circular.

    plt.title('Distribución de Gastos y Saldo Actual')

    plt.show()

def generar_grafico_torta_gastos():
    gastos = [registro for registro in registros_financieros if registro["Tipo"] == "gasto"]
    if not gastos:
        print("No hay gastos para mostrar en el gráfico de torta.")
        return

    categorias_gastos = {}
    for registro in gastos:
        categoria = registro["Categoría"]
        if categoria in categorias_gastos:
            categorias_gastos[categoria] += float(registro["Monto"])
        else:
            categorias_gastos[categoria] = float(registro["Monto"])

    # Preparar los datos para el gráfico de torta
    montos = list(categorias_gastos.values())
    categorias = list(categorias_gastos.keys())

    # Crear el gráfico de torta
    plt.figure(figsize=(8, 8))
    plt.pie(montos, labels=categorias, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Aspecto igual para asegurar que el gráfico sea circular.

    plt.title('Distribución de Gastos por Categoría')

    plt.show()

def generar_resumen_mensual():
    # Crear un diccionario para almacenar totales mensuales
    totales_mensuales = {}
    
    for registro in registros_financieros:
        fecha = datetime.strptime(registro["Fecha"], "%Y-%m-%d")
        mes_anio = fecha.strftime("%Y-%m")

        if mes_anio in totales_mensuales:
            if registro["Tipo"] == "ingreso":
                totales_mensuales[mes_anio]["Ingresos"] += float(registro["Monto"])
            elif registro["Tipo"] == "gasto":
                totales_mensuales[mes_anio]["Gastos"] += float(registro["Monto"])
        else:
            totales_mensuales[mes_anio] = {
                "Ingresos": float(registro["Monto"]) if registro["Tipo"] == "ingreso" else 0,
                "Gastos": float(registro["Monto"]) if registro["Tipo"] == "gasto" else 0
            }
    
    print("Resumen Mensual:")
    for mes_anio, totales in totales_mensuales.items():
        saldo_mensual = totales["Ingresos"] - totales["Gastos"]
        print(f"Mes: {mes_anio}, Ingresos: {totales['Ingresos']}, Gastos: {totales['Gastos']}, Saldo Mensual: {saldo_mensual}")

def limpiar_datos_hasta_fecha():
    fecha_limite = input("Ingrese la fecha hasta la cual desea limpiar los datos (AAAA-MM-DD): ")

    # Filtrar los registros financieros y conservar solo los posteriores a la fecha límite
    registros_nuevos = [registro for registro in registros_financieros if registro["Fecha"] > fecha_limite]

    # Actualizar la lista de registros financieros con los registros posteriores a la fecha límite
    registros_financieros.clear()
    registros_financieros.extend(registros_nuevos)

    # Guardar los datos actualizados
    guardar_datos()

    print("Datos limpiados hasta la fecha especificada.")

def respaldo_automatico():
    nombre_archivo_respaldo = "respaldo.csv"

    with open(nombre_archivo_respaldo, newline="", mode="w") as archivo_csv:
        campos = ["Fecha", "Tipo", "Descripción", "Categoría", "Monto"]
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)

        escritor_csv.writeheader()
        escritor_csv.writerows(registros_financieros)

    print(f"Copia de seguridad actualizada en {nombre_archivo_respaldo}")

def exportar_pdf():
    # Crear un documento PDF
    doc = SimpleDocTemplate("resumen_financiero.pdf", pagesize=letter)
    story = []

    # Crear una tabla para el resumen financiero
    data = [["Fecha", "Tipo", "Descripción", "Categoría", "Monto"]]
    for registro in registros_financieros:
        data.append([registro["Fecha"], registro["Tipo"], registro["Descripción"], registro["Categoría"], registro["Monto"]])

    t = Table(data)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    story.append(t)
    doc.build(story)
    print("Resumen financiero exportado como 'resumen_financiero.pdf'.")

def mostrar_menu():
    print("\nOpciones:")
    print("1. Agregar registro financiero")
    print("2. Calcular totales")
    print("3. Generar gráfico de torta (Gastos e Ingresos)")
    print("4. Generar gráfico de torta de gastos por categoría")
    print("5. Generar resumen mensual")
    print("6. Limpiar datos hasta una fecha")
    print("7. Exportar resumen financiero a PDF")
    print("8. Mostrar versión del programa")
    print("9. Salir")

if __name__ == "__main__":
    cargar_datos()
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_registro()
        elif opcion == "2":
            calcular_totales()
        elif opcion == "3":
            generar_grafico_torta()
        elif opcion == "4":
            generar_grafico_torta_gastos()
        elif opcion == "5":
            generar_resumen_mensual()
        elif opcion == "6":
            limpiar_datos_hasta_fecha()
        elif opcion == "7":
            exportar_pdf()
        elif opcion == "8":
            print(f"Versión del programa: {version}")
        elif opcion == "9":
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")
