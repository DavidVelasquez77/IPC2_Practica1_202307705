from prettytable import PrettyTable, ALL
from colorama import init
import pyfiglet
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import time

# Inicializar colorama
init(autoreset=True)

# Inicializar Rich Console
console = Console()

# Listas para almacenar los autos, clientes y compras registradas
autos_registrados = []
clientes_registrados = []
compras_registradas = []

class Auto:
    def __init__(self, placa, marca, modelo, descripcion, precio_unitario):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario

class Cliente:
    def __init__(self, nombre, correo_electronico, nit):
        self.nombre = nombre
        self.correo_electronico = correo_electronico
        self.nit = nit

class Compra:
    def __init__(self, cliente, autos):
        self.cliente = cliente
        self.autos = autos

def mostrar_titulo():
    # Crear un título con pyfiglet
    ascii_titulo = pyfiglet.figlet_format("SUPER\nAUTOS GT", font="starwars")
    
    # Crear un panel con Rich
    panel = Panel(
        renderable=f"[magenta bold]{ascii_titulo}[/magenta bold]",  # El contenido del panel
        title="✨ Menú Principal ✨", 
        title_align="center",
        border_style="cyan",
        padding=(0, 1),
        expand=False
    )
    console.print(panel)
    time.sleep(1)

def mostrar_menu():
    # Crear tabla con Rich
    table = Table(title="🎯 SELECCIONA UNA OPCIÓN 🎯", title_justify="center", border_style="cyan")
    
    table.add_column("📌 Opción", style="yellow", justify="center")
    table.add_column("Descripción", style="yellow", justify="left")
    
    table.add_row("[cyan]1[/cyan]", "[lightwhite]🌟 Opción 1: Registrar Auto[/lightwhite]")
    table.add_row("[cyan]2[/cyan]", "[lightwhite]🌟 Opción 2: Registrar Cliente[/lightwhite]")
    table.add_row("[cyan]3[/cyan]", "[lightwhite]🌟 Opción 3: Realizar Compra[/lightwhite]")
    table.add_row("[cyan]4[/cyan]", "[lightwhite]🌟 Opción 4: Reporte de Compras[/lightwhite]")
    table.add_row("[cyan]5[/cyan]", "[lightwhite]🌟 Opción 5: Datos del Estudiante[/lightwhite]")
    table.add_row("[red]6[/red]", "[lightwhite]❌ Salir del programa[/lightwhite]")

    console.print(table)

def registrar_auto():
    console.print("[cyan]Registrar Auto[/cyan]")
    placa = input("Ingrese la placa del auto: ")
    marca = input("Ingrese la marca del auto: ")
    modelo = input("Ingrese el modelo del auto: ")
    descripcion = input("Ingrese la descripción del auto: ")
    precio_unitario = float(input("Ingrese el precio unitario del auto: "))
    
    auto = Auto(placa, marca, modelo, descripcion, precio_unitario)
    autos_registrados.append(auto)
    console.print("[green]Auto registrado exitosamente![/green]")

def registrar_cliente():
    console.print("[cyan]Registrar Cliente[/cyan]")
    nombre = input("Ingrese el nombre del cliente: ")
    correo_electronico = input("Ingrese el correo electrónico del cliente: ")
    nit = input("Ingrese el NIT del cliente: ")
    
    # Verificar que el NIT tenga exactamente 9 dígitos
    if len(nit) != 9 or not nit.isdigit():
        console.print("[red]⚠️ El NIT debe tener exactamente 9 dígitos.[/red]")
        return
    
    # Verificar si el NIT ya existe
    for cliente in clientes_registrados:
        if cliente.nit == nit:
            console.print("[red]⚠️ Ya existe un cliente con este NIT.[/red]")
            return
    
    cliente = Cliente(nombre, correo_electronico, nit)
    clientes_registrados.append(cliente)
    console.print("[green]Cliente registrado exitosamente![/green]")

def realizar_compra():
    console.print("[cyan]Realizar Compra[/cyan]")
    nit = input("Ingrese el NIT del cliente: ")
    
    # Buscar el cliente por NIT
    cliente = next((c for c in clientes_registrados if c.nit == nit), None)
    if not cliente:
        console.print("[red]⚠️ No se encontró un cliente con este NIT.[/red]")
        return
    
    autos_seleccionados = []
    while True:
        # Crear submenú con Rich
        table = Table(title="🚗 Submenú de Compra 🚗", title_justify="center", border_style="cyan")
        table.add_column("📌 Opción", style="yellow", justify="center")
        table.add_column("Descripción", style="yellow", justify="left")
        
        table.add_row("[cyan]1[/cyan]", "[lightwhite]Agregar Auto[/lightwhite]")
        table.add_row("[cyan]2[/cyan]", "[lightwhite]Terminar Compra y Generar Factura[/lightwhite]")
        
        console.print(table)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            placa = input("Ingrese la placa del auto a comprar: ")
            auto = next((a for a in autos_registrados if a.placa == placa), None)
            if not auto:
                console.print("[red]⚠️ No se encontró un auto con esta placa.[/red]")
            else:
                autos_seleccionados.append(auto)
                console.print("[green]Auto agregado a la compra![/green]")
        elif opcion == '2':
            if not autos_seleccionados:
                console.print("[red]⚠️ No se seleccionaron autos para la compra.[/red]")
                continue
            
            seguro = input("¿Desea agregar seguro a los autos comprados? (SI/NO): ").strip().lower()
            total = sum(auto.precio_unitario for auto in autos_seleccionados)
            if seguro == 'si':
                total += total * 0.15
            
            compra = Compra(cliente, autos_seleccionados)
            compras_registradas.append(compra)
            console.print(f"[green]Compra registrada exitosamente! Total: Q{total:.2f}[/green]")
            break
        else:
            console.print("[red]⚠️ Opción no válida. Por favor, seleccione una opción del submenú.[/red]")

def generar_reporte_compras():
    total_general = 0
    for compra in compras_registradas:
        cliente = compra.cliente
        autos = compra.autos
        total_compra = sum(auto.precio_unitario for auto in autos)

        # Crear tabla para cada compra
        table = Table(title=f"Compra de {cliente.nombre}", title_justify="center", border_style="cyan")
        table.add_column("Detalle", style="yellow", justify="left")
        table.add_column("Valor", style="yellow", justify="right")
        
        table.add_row("Nombre", cliente.nombre)
        table.add_row("Correo electrónico", cliente.correo_electronico)
        table.add_row("NIT", cliente.nit)
        table.add_row("Autos Adquiridos", "")
        
        for auto in autos:
            table.add_row(f"{auto.marca} {auto.modelo} ({auto.placa})", f"Q{auto.precio_unitario:.2f}")
        
        table.add_row("Total Compra", f"Q{total_compra:.2f}")
        total_general += total_compra
        
        console.print(table)
    
    # Crear panel para el total general
    panel = Panel(
        renderable=f"[bold]Total General: Q{total_general:.2f}[/bold]",
        title="Resumen de Compras",
        title_align="center",
        border_style="green"
    )
    console.print(panel)

def mostrar_datos_estudiante():
    datos_estudiante = """
    [bold]Nombre:[/bold] Josué David Velásquez Ixchop
    [bold]Carnet:[/bold] 202307705
    [bold]Carrera:[/bold] Ingeniería en Ciencias y Sistemas
    [bold]Curso:[/bold] Introducción a la Programación de Computadoras 2
    [bold]Sección:[/bold] A
    """
    panel = Panel(
        renderable=datos_estudiante,
        title="Datos del Estudiante",
        title_align="center",
        border_style="cyan"
    )
    console.print(panel)

def ejecutar_opcion(opcion):
    opciones = {
        1: registrar_auto,
        2: registrar_cliente,
        3: realizar_compra,
        4: generar_reporte_compras,
        5: mostrar_datos_estudiante,
        6: "[red]❌ Saliendo del programa... ¡Hasta luego![/red]"
    }
    if opcion in opciones:
        if callable(opciones[opcion]):
            opciones[opcion]()
        else:
            console.print(opciones[opcion])
    else:
        console.print("[green]⚠️ Opción no válida. Por favor, selecciona una opción del 1 al 6.[/green]")

def main():
    mostrar_titulo()
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Selecciona una opción: "))
            ejecutar_opcion(opcion)
            if opcion == 6:
                break
        except ValueError:
            console.print("[red]⚠️ Entrada no válida. Por favor, introduce un número.[/red]")

if __name__ == "__main__":
    main()