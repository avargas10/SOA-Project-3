import random
from datetime import datetime
from enum import Enum
from node import Node
from logger import Logger
from page import Page
from fifo import Fifo
from lru import Lru
from optimal import Optimal
from optimal_fixed import OptimalF
from constants import DSM_LOGGER
from painter import display_virtual_memory
import copy
from rich.console import Console
from rich.table import Table


class Modes(Enum):
    read = "r"  # Process ID
    write = "w"  # Period of the task

class Replacers(Enum):
    FIFO = "FIFO"  # Process ID
    OPTIMAL = "Optimal"  # Period of the task
    LRU = "LRU"


class DSMSystem:
    def __init__(self, total_pages, num_nodes, pages_per_node, replacement_algorithm, replication, instructions=[], output_path=""):
        self.total_pages = total_pages
        self.vmem = []
        self.nodes = [Node(i, pages_per_node) for i in range(num_nodes)]
        self.pages_per_node = pages_per_node
        self.replication = replication
        self.logPath = DSM_LOGGER
        self.logger = Logger(self.logPath)
        self.loggerResults = Logger(output_path, newName=True) 
        self.instructions = instructions
        self.assign_replacer(replacement_algorithm)
        self.create_pages()
        self.logger.info(f"Creating system with {self.total_pages} VMem Size, {num_nodes} Nodes and {pages_per_node} pages per Node")

    def get_node(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node  
            
    def assign_replacer(self, replacement_algorithm):
        if replacement_algorithm == Replacers.FIFO.value:
            self.replacer = Fifo()
        elif replacement_algorithm == Replacers.LRU.value:
            self.replacer = Lru()
        elif replacement_algorithm == Replacers.OPTIMAL.value:
            self.replacer = OptimalF(self.instructions)
        

    def create_pages(self):
        for page_id in range(self.total_pages):
            self.vmem.append(Page(page_id))
        self.print_vmem()
    
    def print_vmem(self):
        display_virtual_memory(self.vmem, self.logger, "Shared Virtual Memory")

    def update_page(self, new_page_id):
        updated_page = None
        for page in self.vmem:
            if page.id == new_page_id:
                now = datetime.now()
                time_str = now.strftime("%Y-%m-%d %H:%M:%S")
                page.content = "Update at: " + time_str
                page.change_invalid_status(False)
                updated_page = copy.deepcopy(page)
                break
        self.logger.info(f"Updating page {new_page_id}")
        self.print_vmem()
        return updated_page        
    
    def get_page_from_id(self, page_id):
        found_page = None
        for page in self.vmem:
            if page.id == page_id:
                found_page = copy.deepcopy(page)
                self.logger.info(f"Page {page_id} found")
                break
        return found_page

    def update_node(self, new_node):
        for idx, node in enumerate(self.nodes):
            if node.id == new_node.id:
                self.nodes[idx] = new_node
                new_node.print_status()

    def exec_read(self, node , new_page_id, index):
        page = self.get_page_from_id(new_page_id)
        exist, content = node.read_page(new_page_id)
        content = page.content
        node = self.replacer.replace_page(page, node, index)
        self.update_node(node)
        return content

    
    def invalid_page(self, page_id, exempt_node_id):
        for node in self.nodes:
            if node.id != exempt_node_id:
                self.logger.info(f"Invalidating {page_id} for {node.id}")
                node.invalid_page(page_id)
    
    def remove_page(self, page_id, exempt_node_id):
        for node in self.nodes:
            if node.id != exempt_node_id:
                self.logger.info(f"Removing {page_id} for {node.id}")
                node.remove_page(page_id)

    def exec_write(self, node , new_page_id, index):
        new_page = self.update_page(new_page_id)
        exist = node.write_page(new_page)
        node = self.replacer.replace_page(new_page, node, index)
        if self.replication:
            self.invalid_page(new_page.id, node.id)
        self.update_node(node)
        self.print_vmem()
        return

    def execute_instruction(self, node_id, new_page_id, mode, index):
        new_page_id = int(new_page_id)
        node = self.get_node(node_id)
        exist = False
        content = None
        if mode == Modes.read.value:
            self.exec_read(node, new_page_id, index)
        elif mode == Modes.write.value:
            self.exec_write(node, new_page_id, index)
        self.logger.info(f"Replication {self.replication}")
        if not self.replication:
            self.remove_page(new_page_id, node_id)
        self.logger.info(f"Node {node_id} page status {exist} with content {content}")
        

    def analyze_statistics(self, customLogger=None):
        """
        Analyzes an array of Statistics objects and prints a general analysis of hits,
        page faults, and invalidations with their respective percentages.

        Parameters
        ----------
        stats_list : list of Statistics
            A list of Statistics objects to analyze.
        """
        total_hits = 0
        total_page_faults = 0
        total_invalidations = 0
        stats_list = [node.nodeStatistics for node in self.nodes]
        # Sum up all the statistics
        for stats in stats_list:
            total_hits += stats.hits
            total_page_faults += stats.page_faults
            total_invalidations += stats.invalidations

        total_events = total_hits + total_page_faults
        hits_percentage = (total_hits / total_events * 100) if total_events > 0 else 0
        page_faults_percentage = (total_page_faults / total_events * 100) if total_events > 0 else 0
        invalidations_percentage = (total_invalidations / total_events * 100) if total_events > 0 else 0

        table = Table(title="General Statistics Analysis")

        table.add_column("Statistic", justify="center")
        table.add_column("Total Count", justify="center")
        table.add_column("Percentage", justify="center")

        table.add_row("Hits", str(total_hits), f"{hits_percentage:.2f}%")
        table.add_row("Page Faults", str(total_page_faults), f"{page_faults_percentage:.2f}%")
        table.add_row("Invalidations", str(total_invalidations), f"{invalidations_percentage:.2f}%")

        logger = self.logger
        if customLogger:
            logger = customLogger

        console = Console(record=True)
        console.print(table)
        logger.info(console.export_text())
        return console.export_text()
    
    def print_detailed_info(self):
        for node in self.nodes:
            node.print_status_custom_location(self.loggerResults)
        self.analyze_statistics(self.loggerResults)