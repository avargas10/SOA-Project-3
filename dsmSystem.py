import random
from node import Node

class DSMSystem:
    def __init__(self, total_pages, num_nodes, pages_per_node, replacement_algorithm, replication):
        self.total_pages = total_pages
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.pages_per_node = pages_per_node
        self.replacement_algorithm = replacement_algorithm
        self.replication = replication
        self.page_locations = self.initialize_pages()

    def initialize_pages(self):
        page_locations = {}
        for page in range(self.total_pages):
            owner_node = random.choice(self.nodes)
            owner_node.local_memory[page] = f"Data of page {page}"
            page_locations[page] = owner_node.id
        return page_locations

    def fetch_page(self, page, requester_id):
        owner_id = self.page_locations[page]
        owner_node = self.nodes[owner_id]
        page_data = owner_node.local_memory[page]
        
        if not self.replication or page not in owner_node.local_memory:
            return page_data
        
        # Handle replication
        if requester_id != owner_id:
            owner_node.invalidations += 1
            del owner_node.local_memory[page]
        
        return page_data
