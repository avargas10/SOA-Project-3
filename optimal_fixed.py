from replacer import Replacer
from constants import SCHEDULER_LOGGER
from logger import Logger
import copy

class OptimalF(Replacer):
    def __init__(self, instructions=[]):
        self.instructions = instructions
        self.logPath = SCHEDULER_LOGGER + "-OPTIMALF"
        self.logger = Logger(self.logPath) 


    def exist_in_instructions(self, node, index):
        filtered_instructions = [instr for instr in self.instructions if instr[0] == node.id]
        page_list = copy.deepcopy(node.local_memory)
        for instruction in filtered_instructions:
            if instruction[3] > index:
                for page in page_list:
                    if page.id == int(instruction[1]):
                        page_list.remove(page)
                        continue
        return page_list

    def get_replaced_page(self, node, index):
        options_list = self.exist_in_instructions(node, index)
        self.logger.info(f"Node {node.id} -- options_list: {[option.id for option in options_list]}")
        replaced_page = None
        if len(options_list) > 0:
            replaced_page = options_list[0]
        else:
            # Filtrar las instrucciones para el nodo especificado
            filtered_instructions = [instr for instr in self.instructions if instr[0] == node.id]
            page_list = copy.deepcopy(node.local_memory)
            for instruction in filtered_instructions:
                if instruction[3] > index:
                    for page in page_list:
                        if page.id == int(instruction[1]) and page != replaced_page:
                            replaced_page = copy.deepcopy(page)
                            page_list.remove(page)
        self.logger.info(f"Node {node.id} -- replaced_page: {replaced_page.id}")
        return replaced_page

    def check_existing(self, new_page, node):
        exist = False
        for idx, page in enumerate(node.local_memory):
            if page.id == new_page.id:
                new_page.change_invalid_status(False)
                node.local_memory[idx] = copy.deepcopy(new_page)
                exist = True
                self.logger.info(f"Node {node.id} -- Page {new_page.id} added to local memory at position {idx}")
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
            # Replace the furthest used in the future (Optimal)
            page_to_replace = self.get_replaced_page(node, index)
            node.replace_page(page_to_replace, new_page)
            self.logger.info(f"Node {node.id} -- Page {page_to_replace.id} replaced with page {new_page.id}.")
        return node