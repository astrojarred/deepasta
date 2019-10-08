# imports
import numpy as np
import subprocess as sp
from os import path
import getch

# Test image
test_image_path = '/Users/jarredgreen/Downloads/instalooter/carbonara/2081350632616431848.jpg'
image_name = path.basename(test_image_path)

# try with getch
with sp.Popen(["qlmanage", "-p", test_image_path], stdout=sp.DEVNULL, stderr=sp.STDOUT) as pp:
    x = getch.getch()
    if x == "\n":
        print("YES: the image %s is accepted" % image_name)
    else:
        print("NO : the image %s is rejected" % image_name)
    # then close the image with:    
    pp.terminate()

print("done!")