from replacer import Replacer
from constants import SCHEDULER_LOGGER
from logger import Logger
import copy

class Fifo(Replacer):
    def __init__(self):
        self.logPath = SCHEDULER_LOGGER + "-FIFO"
        self.logger = Logger(self.logPath) 

    def replace_page(self, new_page, node):
        # Check if the new page is already in the local memory
        exist, node = self.check_existing(new_page, node) 
        if exist:
            return node
        # Check if there's space in the local memory
        if len(node.local_memory) < node.local_mem_size:
            node.local_memory.append(copy.deepcopy(new_page))
            self.logger.info(f"Node {node.id} -- Page {new_page.id} added to local memory at position {len(node.local_memory) - 1}")
        else:
            # Replace the oldest page (FIFO)
            page_to_replace = node.local_memory.pop(0)
            node.local_memory.append(copy.deepcopy(new_page))
            self.logger.info(f"Node {node.id} -- Page {page_to_replace.id} replaced with page {new_page.id}.")

        return node