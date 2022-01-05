import os
import shutil
import zipfile
import tifffile
import imageio
import json
import numpy as np
import pickle
from pdf2image import convert_from_path

def check_dir(path):
    flag_created = True
    try:
        sep = '\\'
        try:
            list_ = path.split('\\')
        except:
            list_ = path.split('/')
            sep = '/'
        for l in range(len(list_)):
            p = sep.join(list_[:l + 1])
            if not os.path.exists(path=p):
                os.mkdir(p)
    except Exception as e:
        flag_created = False
        print(e)
    return flag_created


def write_arr_images(img, dst):
    dir = "\\".join(dst.split('\\')[:-1])
    dst_extenstion = dst.split('\\')[-1].split('.')[-1]
    if check_dir(path=dir):
        if dst_extenstion == 'tif':
            tifffile.imwrite(dst, img)
        else:
            imageio.imwrite(uri=dst, im=img)


def move_file(src, dst):
    flag_move = True
    try:
        if check_dir(dst):
            shutil.move(src=src, dst=dst)
    except Exception as e:
        flag_move = False
        print(e)
    return flag_move


def copy_file(src, dst):
    flag_move = True
    try:
        if check_dir(dst):
            shutil.copy(src=src, dst=dst)
    except Exception as e:
        flag_move = False
        print(e)
    return flag_move


def export_dict_as_json(target_dict, dst):
    with open(dst, 'w') as json_file:
        json.dump(target_dict, json_file)


def load_json_as_dict(src):
    # Opening JSON file
    with open(src) as json_file:
        dict_data = json.load(json_file)
    return dict_data


def dump_data_as_pickle(object_file, dst):
    try:
        with open(f"{dst}.pickle", "wb") as f_out:
            pickle.dump(object_file, f_out)
    except Exception as e:
        print(e)
        return False
    return True


def load_pickle_file(path):
    try:
        with open(path, 'rb') as f_in:
            object_file = pickle.load(f_in)
    except Exception as e:
        print(e)
        return None
    return object_file


def unzip_file(src, dst):
    try:
        check_dir(dst)
        with zipfile.ZipFile(src, 'r') as zip_ref:
            zip_ref.extractall(dst)
        return dst
    except Exception as e:
        print(e)
        return None


def empty_image(arr_image):
    return np.max(arr_image) == 0.0 and np.min(arr_image) == 0.0


def convert_pdf_2_images(pdf_path):
    images = convert_from_path(pdf_path, 500, poppler_path=r'C:\\Program Files\\poppler-0.67.0\\bin')

    # for i in range(len(images)):
    #     # Save pages as images in the pdf
    #     images[i].save('page' + str(i) + '.jpg', 'JPEG')

    return [np.array(image) for image in images]

