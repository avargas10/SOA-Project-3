class Page:
    def __init__(self, page_id, priority=None, content=None):
        self.id = page_id
        self.priority = priority
        self.invalid = False
        self.content = content
        if not self.content:
            self.content = str(page_id) 
        
    
    def change_invalid_status(self, status):
        self.invalid = status