# Optimal Execution
python3 consoleDsmConfigApp.py -c /Users/andresvargasrivera/repos/SOA-Project-3/config/config1.json -r /Users/andresvargasrivera/repos/SOA-Project-3/instructions/instructions-optimal.txt -o logs/salida-optimal.txt -a Optimal

# LRU Execution
python3 consoleDsmConfigApp.py -c /Users/andresvargasrivera/repos/SOA-Project-3/config/config1.json -r /Users/andresvargasrivera/repos/SOA-Project-3/instructions/instructions-lru.txt -o logs/salida-lru.txt -a LRU

# FIFO Execution
python3 consoleDsmConfigApp.py -c /Users/andresvargasrivera/repos/SOA-Project-3/config/config1.json -r /Users/andresvargasrivera/repos/SOA-Project-3/instructions/instructions-fifo.txt -o logs/salida-fifo.txt -a FIFO -d

# Replication Execution
python3 consoleDsmConfigApp.py -c /Users/andresvargasrivera/repos/SOA-Project-3/config/config1.json -r /Users/andresvargasrivera/repos/SOA-Project-3/instructions/instructions-replication.txt -o logs/salida-replication.txt -a FIFO -d

# NO Replication Execution
python3 consoleDsmConfigApp.py -c /Users/andresvargasrivera/repos/SOA-Project-3/config/config1.json -r /Users/andresvargasrivera/repos/SOA-Project-3/instructions/instructions-replication.txt -o logs/salida-replication.txt -a FIFO

# UI Execution
python3 dsmConfigApp.py