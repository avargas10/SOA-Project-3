import random
from node import Node
from dsmSystem import DSMSystem
from logger import Logger
from constants import SIMULATOR_LOGGER

class Simulator:
    def __init__(self, config, instructions, output_path="logs/results.log"):
        self.config = config
        self.instructions = instructions
        
        self.logPath = SIMULATOR_LOGGER
        self.logger = Logger(self.logPath, clean=True) 
        self.logger.info(f"Configuring Simulator")
        self.dsmSystem = DSMSystem(config['total_pages'], config['num_nodes'], config['pages_per_node'],
                               config['replacement_algorithm'], config['replication'], self.instructions, output_path)
        self.runSimulation()
    
    def runSimulation(self):
        for instruction in self.instructions:
            node_id = instruction[0]
            page_id = instruction[1]
            mode = instruction[2]
            self.logger.info(f"Running simulation of {instruction}")
            self.dsmSystem.execute_instruction(node_id, page_id, mode)
        self.dsmSystem.print_detailed_info()

        