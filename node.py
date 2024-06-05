class Node:
    def __init__(self, id):
        self.id = id
        self.local_memory = {}
        self.page_faults = 0
        self.hits = 0
        self.invalidations = 0

    def __repr__(self):
        return f"Node({self.id}, {self.local_memory})"

    def access_page(self, page, mode, dsm_system):
        if page in self.local_memory:
            self.hits += 1
            return self.local_memory[page]
        
        self.page_faults += 1
        page_data = dsm_system.fetch_page(page, self.id)
        self.local_memory[page] = page_data
        return page_data
