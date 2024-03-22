import pandas as pd
import numpy as np
import trackpy as tp
import matplotlib.pyplot as plt
import json
from glob import glob
from utils import *

with open('plot_msd.json', 'r') as f:
    config = json.load(f)
    
imsd(config,types=[1,2])
plot_imsd(config,multiplier=1e12)



