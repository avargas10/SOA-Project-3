from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout

def display_processor(node_id, pages, logger):

    # Crear la tabla de posiciones de memoria
    table = Table(title="Posiciones de Memoria")
    table.add_column("Page ID", justify="center")
    table.add_column("Content", justify="center")

    for page in pages:
        table.add_row(str(page.id), str(page.content))

    # Crear el panel del procesador
    processor_panel = Panel(
        f"[bold magenta]{node_id}[/bold magenta]",
        title="[bold green]Processor[/bold green]",
        border_style="green"
    )

    # Disposición del layout
    layout = Layout()
    layout.split_column(
        Layout(processor_panel, name="processor"),
        Layout(table, name="memory")
    )

    console = Console(record=True)
    console.print(layout)
    logger.info("\n"+console.export_text())
    return console.export_text()


def display_virtual_memory(vmem, logger, table_title):

    # Crear la tabla de memoria virtual
    table = Table(title=table_title)
    table.add_column("Page ID", justify="center")
    table.add_column("Content", justify="center")
    table.add_column("Invalid", justify="center")

    for page in vmem:
        table.add_row(str(page.id), str(page.content), str(page.invalid))

    console = Console(record=True)
    console.print(table)
    logger.info(console.export_text())
    return console.export_text()