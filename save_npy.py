import os
import json
import numpy as np

json_list = os.listdir('swig-master/regionfiles')
img_list = [name.split('.')[0] for name in json_list]

img_list =