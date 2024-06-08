from rich.console import Console
from rich.table import Table

class NodeStatistics:
    """
    A class to manage statistics for hits, page faults, and page invalidations.

    Attributes
    ----------
    hits : int
        Counter for the number of hits.
    page_faults : int
        Counter for the number of page faults.
    invalidations : int
        Counter for the number of page invalidations.

    Methods
    -------
    increment_hits():
        Increments the hit counter by one.
    increment_page_faults():
        Increments the page fault counter by one.
    increment_invalidations():
        Increments the page invalidation counter by one.
    generate_table():
        Generates and prints a table with statistics and their percentages using rich.
    """

    def __init__(self):
        """Initializes the counters for hits, page faults, and page invalidations to zero."""
        self.hits = 0
        self.page_faults = 0
        self.invalidations = 0

    def increment_hits(self):
        """Increments the hit counter by one."""
        self.hits += 1

    def increment_page_faults(self):
        """Increments the page fault counter by one."""
        self.page_faults += 1

    def increment_invalidations(self):
        """Increments the page invalidation counter by one."""
        self.invalidations += 1

    def generate_table(self, logger):
        """
        Generates and prints a table with statistics and their percentages using rich.
        """
        total = self.hits + self.page_faults
        hits_percentage = (self.hits / total * 100) if total > 0 else 0
        page_faults_percentage = (self.page_faults / total * 100) if total > 0 else 0
        invalidations_percentage = (self.invalidations / total * 100) if total > 0 else 0

        table = Table(title="Statistics")

        table.add_column("Statistic", justify="center")
        table.add_column("Count", justify="center")
        table.add_column("Percentage", justify="center")

        table.add_row("Hits", str(self.hits), f"{hits_percentage:.2f}%")
        table.add_row("Page Faults", str(self.page_faults), f"{page_faults_percentage:.2f}%")
        table.add_row("Invalidations", str(self.invalidations), f"{invalidations_percentage:.2f}%")

        console = Console(record=True)
        console.print(table)
        logger.info(console.export_text())
        return console.export_text()