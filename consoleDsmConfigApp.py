import argparse
import json
from dsmSystem import DSMSystem
from simulator import Simulator
class ConsoleDSMConfigApp:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="DSM Configuration and Simulation")
        self.setup_arguments()
        self.simulator = None
    
    def setup_arguments(self):
        self.parser.add_argument("-c", "--config", required=True, help="Path to configuration file")
        self.parser.add_argument("-r", "--references", required=True, help="Path to references file")
        self.parser.add_argument("-o", "--output", required=True, help="Path to output file")
        self.parser.add_argument("-a", "--algorithm", required=True, choices=["LRU", "Optimal", "FIFO"], help="Page replacement algorithm")
        self.parser.add_argument("-d", "--replication", action='store_true', help="Enable replication")
    
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
    
    
    def run(self):
        args = self.parse_arguments()
        
        config = self.load_config(args.config)
        config['replacement_algorithm'] = args.algorithm
        print(f"Replication in console: {args.replication}")
        config['replication'] = args.replication
        output_path = args.output
        
        references = self.load_references(args.references)
        config['references'] = references
        self.simulator = Simulator(config=config, instructions=references, output_path=output_path)
        print("Simulation completed successfully. Check the output file for statistics.")

if __name__ == "__main__":
    app = ConsoleDSMConfigApp()
    app.run()
