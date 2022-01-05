import numpy as np
from PIL import Image
import utils_ocr
import easyocr
import warnings

warnings.filterwarnings("ignore")


def get_image(img):
    image = Image.open(img)
    return np.asarray(image)


def get_reader_lang(lang='ar'):
    # print("....... Define OCR Reader")
    reader = easyocr.Reader(['en', 'ar'], gpu=True)
    # reader = easyocr.Reader(['en', 'ar'])
    return reader


def get_result(reader, image, lang='ar'):
    # reader = get_reader_lang(lang)

    print("............ start extract text ")
    result = reader.readtext(image)
    return result


def get_text_from_image(reader, image_arrays):
    # image_file = "../../Arabic-OCR-master/src/test/page1.jpg"

    # image = get_image(image_file)
    extracted_text = ""
    for image_array in image_arrays:
        result = get_result(reader=reader, image=image_array)

        # annoted_image = utils_ocr.annotate_image(image, result)
        # annoted_image = Image.fromarray(annoted_image)

        extracted_text += utils_ocr.get_raw_text(result)

    return extracted_text
