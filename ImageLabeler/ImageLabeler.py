# imports
import numpy as np
import subprocess as sp
from os import path
import getch
import time
import sys
import glob

# for cropping images
import imageio
import skimage
import math
import warnings


# defs
def move_image(file, image_name, destination_folder):
    '''Make thumbnail and move image to a special folder'''
    sp.call(['mv', str(file), '%s/%s' % (destination_folder, image_name)])


def crop_center(im, quiet=True):
    '''Crops an image to square about the center using skimage
       needs: imageio, skimage, math'''
    
    if not quiet: print('cropping to a square')
    if not quiet: print('old shape: %s' % str(im.shape))
    photo_dim = np.array(im.shape)[:2]
    bigger_dim, smaller_dim = np.amax(photo_dim), np.amin(photo_dim)
    height, width = photo_dim[0], photo_dim[1]

    diff1 = math.ceil((bigger_dim - smaller_dim ) / 2)
    diff2 = math.floor((bigger_dim - smaller_dim ) / 2)

    if width == height:
        if not quiet: print('already square!')
    elif width > height:
        im = skimage.util.crop(im, ((0,0),(diff1,diff2),(0,0)))
        if not quiet: print('new shape: %s' % str(im.shape))
    else:
        im = skimage.util.crop(im, ((diff1,diff2),(0,0),(0,0)))
        if not quiet: print('new shape: %s' % str(im.shape))
    
    return im


def resize_image(im, dim, quiet=True):
    '''resizes image im to square with dimensions dim'''
    
    if not quiet: print('rescaling to %s x %s' % (dim, dim))
    return skimage.transform.resize(im, [dim, dim])


def write_image(image, path, filename, quiet=True):
    '''writes the new image!'''
    imageio.imwrite('%s/%s' % (path, filename), skimage.img_as_ubyte(image))
    if not quiet: print('image saved to %s/%s' % (path, filename))


def process_image(path, image_name, destination_folder, size, quiet=True):
    #open_image
    im = imageio.imread(path)
    im = crop_center(im, quiet=quiet)
    im = resize_image(im, size, quiet=quiet)

    write_image(im, destination_folder, image_name, quiet=quiet)



# Test image
category = sys.argv[1]
image_folder = sys.argv[2]

print("looking for .jpg %s images in %s" % (category, image_folder))

# get list of *.jpg files inside the image_folder
files_list = glob.glob("%s/*.jpg" % image_folder)

# create an accepted and rejected folder
print("creating folders")
accepted_folder = '%s/accepted' % image_folder
rejected_folder = '%s/rejected' % image_folder
sp.call(['mkdir', '-p', '%s' % accepted_folder])
sp.call(['mkdir', '-p', '%s' % rejected_folder])
        

# one image for testing
# test_image_path = '/Users/jarredgreen/Downloads/instalooter/carbonara/2081350632616431848.jpg'
# image_name = path.basename(test_image_path)


# loop over all images in files_list
for file in files_list:
    with sp.Popen(["qlmanage", "-t", file], stdout=sp.DEVNULL, stderr=sp.STDOUT) as pp:
        # set image name
        image_name = path.basename(file)

        # switch app to hyper
        # wait 1/10 sec for image to open
        time.sleep(0.25)
        sp.Popen(["open", "-a", "Hyper"])

        # get a 1 character input from getch
        x = getch.getch()

        # return yields a yes, any other key a no
        if x == "\n":
            print("YES: the image %s is accepted" % image_name)
            move_image(file, image_name, accepted_folder)
            # process and move the image, surpressing the coversion warning
            '''
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                process_image(file, image_name, accepted_folder, 64, quiet=True)
            '''

        else:
            print("NO : the image %s is rejected" % image_name)
            move_image(file, image_name, rejected_folder)
        # then close the image with:    
        pp.terminate()


print("done!")