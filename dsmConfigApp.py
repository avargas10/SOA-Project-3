import tkinter as tk
from tkinter import ttk, messagebox
from dsmSystem import DSMSystem

class DSMConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DSM Configuration")
        self.create_widgets()
    
    def create_widgets(self):
        # Number of pages
        ttk.Label(self.root, text="Total Number of Pages:").grid(row=0, column=0, sticky=tk.W)
        self.total_pages_var = tk.IntVar()
        ttk.Entry(self.root, textvariable=self.total_pages_var).grid(row=0, column=1)
        
        # Number of nodes
        ttk.Label(self.root, text="Number of Nodes:").grid(row=1, column=0, sticky=tk.W)
        self.num_nodes_var = tk.IntVar()
        ttk.Entry(self.root, textvariable=self.num_nodes_var).grid(row=1, column=1)
        
        # Pages per node
        ttk.Label(self.root, text="Pages per Node:").grid(row=2, column=0, sticky=tk.W)
        self.pages_per_node_var = tk.IntVar()
        ttk.Entry(self.root, textvariable=self.pages_per_node_var).grid(row=2, column=1)
        
        # Replacement algorithm
        ttk.Label(self.root, text="Page Replacement Algorithm:").grid(row=3, column=0, sticky=tk.W)
        self.replacement_algorithm_var = tk.StringVar()
        ttk.Combobox(self.root, textvariable=self.replacement_algorithm_var, values=["LRU", "Optimal", "FIFO"]).grid(row=3, column=1)
        
        # Replication option
        ttk.Label(self.root, text="Enable Replication:").grid(row=4, column=0, sticky=tk.W)
        self.replication_var = tk.BooleanVar()
        ttk.Checkbutton(self.root, variable=self.replication_var).grid(row=4, column=1)
        
        # List of references
        ttk.Label(self.root, text="Page References (format: node,page,mode):").grid(row=5, column=0, sticky=tk.W)
        self.references_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.references_var).grid(row=5, column=1)
        
        # Submit button
        ttk.Button(self.root, text="Submit", command=self.submit).grid(row=6, column=0, columnspan=2)
    
    def submit(self):
        try:
            total_pages = self.total_pages_var.get()
            num_nodes = self.num_nodes_var.get()
            pages_per_node = self.pages_per_node_var.get()
            replacement_algorithm = self.replacement_algorithm_var.get()
            replication = self.replication_var.get()
            references = self.references_var.get()
            
            if not (total_pages > 0 and num_nodes > 0 and pages_per_node > 0):
                raise ValueError("Number of pages, nodes, and pages per node must be greater than 0.")
            
            if replacement_algorithm not in ["LRU", "Optimal", "FIFO"]:
                raise ValueError("Invalid replacement algorithm selected.")
            
            references_list = [ref.split(",") for ref in references.split(";")]
            for ref in references_list:
                if len(ref) != 3:
                    raise ValueError("Each reference must have exactly three components: node,page,mode.")
                ref[0] = int(ref[0])  # node
                ref[1] = ref[1]  # page
                ref[2] = ref[2]  # mode
                if ref[2] not in ["r", "w"]:
                    raise ValueError("Mode must be 'r' (read) or 'w' (write).")
            
            config = {
                "total_pages": total_pages,
                "num_nodes": num_nodes,
                "pages_per_node": pages_per_node,
                "replacement_algorithm": replacement_algorithm,
                "replication": replication,
                "references": references_list
            }
            
            # self.simulate_dsm(config)
        
        except Exception as e:
            messagebox.showerror("Invalid Input", str(e))
    
    def simulate_dsm(self, config):
        dsm_system = DSMSystem(config['total_pages'], config['num_nodes'], config['pages_per_node'],
                               config['replacement_algorithm'], config['replication'])
        for ref in config['references']:
            node_id, page, mode = ref
            node = dsm_system.nodes[node_id]
            node.access_page(int(page), mode, dsm_system)
        
        self.show_statistics(dsm_system)
    
    def show_statistics(self, dsm_system):
        stats = "DSM Simulation Statistics\n"
        for node in dsm_system.nodes:
            stats += f"Node {node.id}: Page Faults: {node.page_faults}, Hits: {node.hits}, Invalidations: {node.invalidations}\n"
        print(stats)
        messagebox.showinfo("Simulation Statistics", stats)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = DSMConfigApp(root)
    root.mainloop()
