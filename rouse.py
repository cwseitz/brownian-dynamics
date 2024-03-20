from _lammps import Rouse
import json

with open('rouse.json', 'r') as f:
    config = json.load(f)
    
rouse = Rouse(config)
rouse.run()
