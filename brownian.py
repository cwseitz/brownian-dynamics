from _lammps import Brownian
import json

with open('brownian.json', 'r') as f:
    config = json.load(f)
    
brown = Brownian(config)
brown.run()
