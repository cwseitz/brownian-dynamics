from _lammps import Binders
import json

with open('binders.json', 'r') as f:
    config = json.load(f)
    
binders = Binders(config)
binders.run()
