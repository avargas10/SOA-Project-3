from abc import ABC, abstractmethod
import copy

class Replacer(ABC):
    @abstractmethod
    def replace_page(self, new_page, node):
        pass

    def check_existing(self, new_page, node, index):
        exist = False
        for idx, page in enumerate(node.local_memory):
            if page.id == new_page.id:
                new_page.change_invalid_status(False)
                node.local_memory[idx] = copy.deepcopy(new_page)
                exist = True
                self.logger.info(f"Node {node.id} -- Page {new_page.id} added to local memory at position {idx}")
        return exist, node