from page import Page
from painter import display_virtual_memory
from constants import NODE_LOGGER
from logger import Logger
from datetime import datetime
from nodeStatistics import NodeStatistics
import copy

class Node:
    def __init__(self, id, lmem_size):
        self.id = id
        self.local_mem_size = lmem_size
        self.local_memory = []
        self.page_faults = 0
        self.hits = 0
        self.page_tracker = []
        self.invalidations = 0
        self.logPath = NODE_LOGGER + "-" + str(self.id)
        self.logger = Logger(self.logPath) 
        self.logPathStats = NODE_LOGGER + "-stats-" + str(self.id)
        self.loggerStats = Logger(self.logPathStats) 
        self.nodeStatistics = NodeStatistics()
        self.print_status()

    def __repr__(self):
        return f"Node({self.id}, {self.local_memory})"
    
    def print_status(self):
        vmem = display_virtual_memory(self.local_memory, self.loggerStats, "Node " + str(self.id) + " Local Memory")
        stats =  self.nodeStatistics.generate_table(self.loggerStats)
        return vmem + '\n' + stats
    
    def print_status_custom_location(self, logger_custom):
        display_virtual_memory(self.local_memory, logger_custom, "Node " + str(self.id) + " Local Memory")
        self.nodeStatistics.generate_table(logger_custom)
    
    def read_page(self, page_id):
        self.logger.info(f"Reading page {page_id}")
        page_content = None
        exist = False
        invalid = False
        for page in self.local_memory:
            if page.id == page_id:
                exist = True
                self.nodeStatistics.increment_hits()
                page_content = page.content
                invalid = page.invalid
        self.check_page_fault(exist and not invalid)
        return exist and not invalid, page_content

    def write_page(self, new_page):
        self.logger.info(f"Writting page {new_page.id}")
        exist = False
        for idx, page in enumerate(self.local_memory):
            if page.id == new_page.id:
                exist = True
                self.nodeStatistics.increment_hits()
                self.local_memory[idx] = copy.deepcopy(new_page)
        self.check_page_fault(exist)
        return exist

    def invalid_page(self, page_id):
        for page in self.local_memory:
            if page.id == page_id:
                self.logger.info(f"Invalidating page {page_id}")
                page.change_invalid_status(True)
                self.nodeStatistics.increment_invalidations()
                break
        self.print_status()

    def remove_page(self, page_id):
        for idx,page in enumerate(self.local_memory):
            if page.id == page_id:
                self.logger.info(f"Removing page {page_id}")
                self.local_memory.pop(idx)
                break
        self.print_status()

    def replace_page(self, old_page, new_page):
        for idx,page in enumerate(self.local_memory):
            if page.id == old_page.id:
                self.logger.info(f"Removing page {old_page.id} inserting {new_page.id}")
                self.local_memory.pop(idx)
                self.local_memory.insert(idx, copy.deepcopy(new_page))
                break
        self.print_status()

    def check_page_fault(self, exist):
        if not exist:
            self.nodeStatistics.increment_page_faults()
    
    def assign_page_tracker(self, page_tracker):
        self.page_tracker = page_tracker

    def operate_page(self, page_id):
        # Encontrar el índice de la página en el arreglo
        for item in self.page_tracker:
            if item['page'] == page_id:
                item['count'] -= 1
                break
        
        # Volver a ordenar el arreglo por el conteo de menor a mayor
        self.page_tracker = sorted(self.page_tracker, key=lambda x: x['count'])
        self.order_local_memory()
        self.logger.info(f"Page Tracker\n{self.page_tracker}")

    def order_local_memory(self):
        """
        Orders the self.local_memory list based on the order of page IDs in self.page_tracker.
        Only includes pages that are present in both self.page_tracker and self.local_memory.
        """
        # Create a dictionary for quick lookup of local_memory pages by their id
        local_memory_dict = {page.id: page for page in self.local_memory}
        self.logger.info(local_memory_dict)
        # Create a new ordered list based on the page_tracker
        ordered_local_memory = []
        for entry in self.page_tracker:
            page_id = entry['page']
            if page_id in local_memory_dict:
                ordered_local_memory.append(local_memory_dict[page_id])

        # Update self.local_memory to be the ordered list
        self.local_memory = ordered_local_memory
