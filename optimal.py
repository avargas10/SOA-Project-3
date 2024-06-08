from replacer import Replacer
from constants import SCHEDULER_LOGGER
from logger import Logger
import copy

class Optimal(Replacer):
    def __init__(self, instructions=[]):
        self.instructions = instructions
        self.logPath = SCHEDULER_LOGGER + "-OPTIMAL"
        self.logger = Logger(self.logPath) 


    def get_page_tracking(self, node):
        # Filtrar las instrucciones para el nodo especificado
        filtered_instructions = [instr for instr in self.instructions if instr[0] == node.id]
        
        # Contar las ocurrencias de cada página
        page_counts = {}
        for instr in filtered_instructions:
            page = instr[1]
            if page in page_counts:
                page_counts[page] += 1
            else:
                page_counts[page] = 1
        
        # Crear una lista de diccionarios con el formato {page: <page>, count: <count>}
        page_tracking = [{'page': int(page), 'count': count} for page, count in page_counts.items()]
        
        # Ordenar la lista de menor a mayor por el conteo
        page_tracking_sorted = sorted(page_tracking, key=lambda x: x['count'])
        node.assign_page_tracker(page_tracking_sorted)
        return page_tracking_sorted
    
    def check_existing(self, new_page, node):
        exist = False
        for idx, page in enumerate(node.local_memory):
            if page.id == new_page.id:
                new_page.change_invalid_status(False)
                node.local_memory[idx] = copy.deepcopy(new_page)
                node.operate_page(new_page.id)
                exist = True
                self.logger.info(f"Node {node.id} -- Page {new_page.id} added to local memory at position {idx}")
        return exist, node

            
    def replace_page(self, new_page, node, index):
        # Check if the new page is already in the local memory
        if not node.page_tracker:
            self.get_page_tracking(node)
        exist, node = self.check_existing(new_page, node) 
        if exist:
            return node
        # Check if there's space in the local memory
        if len(node.local_memory) < node.local_mem_size:
            node.local_memory.insert(0, copy.deepcopy(new_page))
            self.logger.info(f"Node {node.id} -- Page {new_page.id} added to local memory at position {len(node.local_memory) - 1}")
        else:      
            # Replace the least used in the future (Optimal)
            page_to_replace = node.local_memory.pop(0)
            node.local_memory.insert(0, copy.deepcopy(new_page))
            self.logger.info(f"Node {node.id} -- Page {page_to_replace.id} replaced with page {new_page.id}.")
        node.operate_page(new_page.id)
        return node