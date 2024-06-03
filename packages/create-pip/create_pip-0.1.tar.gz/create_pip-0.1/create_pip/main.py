import numpy as np
import cv2 as cv
import os
import time

def make_folder(src_directory,idx):
    print("idx",idx)
    if not os.path.exists(src_directory):
        os.makedirs(src_directory)
        return idx
    return 1
    
