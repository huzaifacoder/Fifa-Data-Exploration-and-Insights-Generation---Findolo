import tkinter as tk
import time
import os
import pandas as pd
from scipy.stats import skew
import numpy as np
import threading
# read csv
pathjoin1 = (os.getcwd())
#print(pathjoin1)
#path = pathjoin1.join(pathjoin1, "DATABASE\\Career Mode player datasets - FIFA 15-22.csv")
#print(path.head())
print(os.path.relpath('Career Mode player datasets - FIFA 15-22.csv'))