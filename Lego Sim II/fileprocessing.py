from os import listdir, mkdir, rename
from os.path import isfile
import glob
import shutil



root_path = '/Users/ckruse/Documents/Unity/Lego Sim II/screenshots/'
root_folder = listdir(root_path)

type_array = [];
#Load images into image_array by iterating through all the folders in the root directory


for files in range(1,len(root_folder)):
    name = ''
    for char in root_folder[files]:

        if char == ' ':
            break
        name += char

    if name not in type_array:
        type_array.append(name)

for element in type_array:
    folder_name = '/Users/ckruse/Documents/Unity/Lego Sim II/screenshots/' + element
    cat_name = '/Users/ckruse/Documents/Unity/Lego Sim II/screenshots/' + element +'*.png'
    mkdir(folder_name)
    for img in glob.glob(cat_name):
        shutil.move(img, folder_name)
