from replacer import Replacer
from constants import SCHEDULER_LOGGER
from logger import Logger
import copy

class Lru(Replacer):
    def __init__(self):
        self.logPath = SCHEDULER_LOGGER + "-LRU"
        self.logger = Logger(self.logPath) 


    def check_existing(self, new_page, node):
        exist = False
        for i, page in enumerate(node.local_memory):
            if page.id == new_page.id:
                exist = True
                # Remove the page from its current position
                node.local_memory.pop(i)
                # Insert the page at the beginning of the list
                node.local_memory.insert(0, copy.deepcopy(new_page))
                self.logger.info(f"Node {node.id} -- Page {new_page.id} added to local memory at position {0}")
                break
        return exist, node

            
    def replace_page(self, new_page, node, index):
        # Check if the new page is already in the local memory
        exist, node = self.check_existing(new_page, node) 
        if exist:
            return node
        # Check if there's space in the local memory
        if len(node.local_memory) < node.local_mem_size:
            node.local_memory.insert(0, copy.deepcopy(new_page))
            self.logger.info(f"Node {node.id} -- Page {new_page.id} added to local memory at position {len(node.local_memory) - 1}")
        else:      
            # Replace the least used page (LRU)
            page_to_replace = node.local_memory.pop()
            node.local_memory.insert(0, copy.deepcopy(new_page))
            self.logger.info(f"Node {node.id} -- Page {page_to_replace.id} replaced with page {new_page.id}.")
        return node