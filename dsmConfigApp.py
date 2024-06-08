import tkinter as tk
from tkinter import ttk, messagebox
from dsmSystem import DSMSystem
from simulator import Simulator

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
        ttk.Label(self.root, text="Page References (example: instructions.txt):").grid(row=5, column=0, sticky=tk.W)
        self.references_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.references_var).grid(row=5, column=1)
        
        # Submit button
        ttk.Button(self.root, text="Submit", command=self.submit).grid(row=6, column=0, columnspan=2)

        # Help button
        ttk.Button(self.root, text="Help", command=self.help).grid(row=7, column=0, columnspan=2)
    
    def help(self):
        help_text = (
            "Esta interfaz permite configurar un sistema DSM (Distributed Shared Memory).\n\n"
            "1. Total Number of Pages: Número total de páginas en la memoria compartida.\n"
            "2. Number of Nodes: Número de nodos en el sistema DSM.\n"
            "3. Pages per Node: Número de páginas asignadas a cada nodo.\n"
            "4. Page Replacement Algorithm: Algoritmo de reemplazo de páginas a utilizar. Opciones: LRU (Least Recently Used), Optimal, FIFO (First In First Out).\n"
            "5. Enable Replication: Opción para habilitar la replicación de páginas entre nodos.\n"
            "6. Page References: Lista de referencias de páginas en el formato 'node,page,mode', donde 'node' es el identificador del nodo, 'page' es la página y 'mode' es el modo de acceso ('read' o 'write').\n\n"
            "Los logs de estadisticas del sistema se guardaran en el archivo logs/results.txt.\n"
            "Una vez configurados los parámetros, presione 'Submit' para iniciar la simulación.\n"
            
        )
        messagebox.showinfo("Ayuda", help_text)

    def submit(self):
        try:
            total_pages = self.total_pages_var.get()
            num_nodes = self.num_nodes_var.get()
            pages_per_node = self.pages_per_node_var.get()
            replacement_algorithm = self.replacement_algorithm_var.get()
            replication = self.replication_var.get()
            references_path = self.references_var.get()
            
            if not (total_pages > 0 and num_nodes > 0 and pages_per_node > 0):
                raise ValueError("Number of pages, nodes, and pages per node must be greater than 0.")
            
            if replacement_algorithm not in ["LRU", "Optimal", "FIFO"]:
                raise ValueError("Invalid replacement algorithm selected.")
            
            references_list = self.load_references(references_path)
            
            config = {
                "total_pages": total_pages,
                "num_nodes": num_nodes,
                "pages_per_node": pages_per_node,
                "replacement_algorithm": replacement_algorithm,
                "replication": replication,
                "references": references_list
            }
            
            self.simulate_dsm(config, references_list)
        
        except Exception as e:
            messagebox.showerror("Invalid Input", str(e))
    
    def load_references(self, references_path):
        with open(references_path, 'r') as file:
            references = []
            index = 0
            for line in file:
                node, page, mode = line.strip().split(',')
                references.append((int(node), page, mode, index))
                index += 1
            return references

    def simulate_dsm(self, config, references):
        self.simulator = Simulator(config=config, instructions=references)
        print("Simulation completed successfully. Check the output file for statistics.")
    
    def show_statistics(self, dsm_system):
        stats = "DSM Simulation Statistics\n"
        for node in dsm_system.nodes:
            stats += f"Node {node.id}: Page Faults: {node.page_faults}, Hits: {node.hits}, Invalidations: {node.invalidations}\n"
        messagebox.showinfo("Simulation Statistics", stats)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = DSMConfigApp(root)
    root.mainloop()
