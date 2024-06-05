import argparse
import json
from dsmSystem import DSMSystem

class ConsoleDSMConfigApp:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="DSM Configuration and Simulation")
        self.setup_arguments()
    
    def setup_arguments(self):
        self.parser.add_argument("-c", "--config", required=True, help="Path to configuration file")
        self.parser.add_argument("-r", "--references", required=True, help="Path to references file")
        self.parser.add_argument("-o", "--output", required=True, help="Path to output file")
        self.parser.add_argument("-a", "--algorithm", required=True, choices=["LRU", "Optimal", "FIFO"], help="Page replacement algorithm")
        self.parser.add_argument("-d", "--replication", required=True, type=bool, help="Enable replication (True/False)")
    
    def parse_arguments(self):
        return self.parser.parse_args()
    
    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            return json.load(file)
    
    def load_references(self, references_path):
        with open(references_path, 'r') as file:
            references = []
            for line in file:
                node, page, mode = line.strip().split(',')
                references.append((int(node), page, mode))
            return references
    
    def save_output(self, output_path, stats):
        with open(output_path, 'w') as file:
            file.write(stats)
    
    def simulate_dsm(self, config, references):
        dsm_system = DSMSystem(config['total_pages'], config['num_nodes'], config['pages_per_node'],
                               config['replacement_algorithm'], config['replication'])
        for ref in references:
            node_id, page, mode = ref
            node = dsm_system.nodes[node_id]
            node.access_page(int(page), mode, dsm_system)
        
        return self.collect_statistics(dsm_system)
    
    def collect_statistics(self, dsm_system):
        stats = "DSM Simulation Statistics\n"
        for node in dsm_system.nodes:
            stats += f"Node {node.id}: Page Faults: {node.page_faults}, Hits: {node.hits}, Invalidations: {node.invalidations}\n"
        return stats
    
    def run(self):
        args = self.parse_arguments()
        
        config = self.load_config(args.config)
        config['replacement_algorithm'] = args.algorithm
        config['replication'] = args.replication
        
        references = self.load_references(args.references)
        config['references'] = references
        
        stats = self.simulate_dsm(config, references)
        self.save_output(args.output, stats)
        print("Simulation completed successfully. Check the output file for statistics.")

if __name__ == "__main__":
    app = ConsoleDSMConfigApp()
    app.run()
