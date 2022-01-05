import easyocr
import numpy as np
import torch
from flask import Flask, request
from flask_restful import Api, Resource
from datetime import datetime
import imageio
import ocr
import utils

app = Flask(__name__)
api = Api(app)

path_upload = ".\\upload\\temp"
list_allowed_file_types = ['jpg', 'png', 'jpeg', 'pdf']


def get_images(image_path):
    arr_images = []
    ext = image_path.split('.')[-1]
    if ext == 'pdf':
        print("========= Convert PDF to Image")
        arr_images = utils.convert_pdf_2_images(pdf_path=image_path)
    else:
        arr_images.append(np.array(imageio.imread(image_path)))
    return arr_images


if torch.cuda.is_available():
    print("============= Load OCR READER - GPU ...")
    ocr_reader = easyocr.Reader(['en', 'ar'], gpu=True)
else:
    print("============= Load OCR READER - CPU ...")
    ocr_reader = easyocr.Reader(['en', 'ar'], gpu=True)


class ApplyOCR(Resource):
    def post(self):

        global dict_sentiment
        file = request.files['file']
        file_name, file_ext = file.filename.split('.')

        path_save_file = None

        # Check received file is in allowed types
        if file_ext in list_allowed_file_types:
            # Create directory with file name followed by date
            path_output_dir = f"{path_upload}\\" \
                              f"{file_name.split('.')[0]}_{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}"
            if utils.check_dir(path_output_dir):
                # save received file in directory
                print("==================== Save uploaded file")
                path_save_file = f"{path_output_dir}\\{file_name}.{file_ext}"
                file.save(dst=path_save_file)

            try:
                arr_images = get_images(path_save_file)

                print("============= Extract text from images")
                extracted_text = ocr.get_text_from_image(reader=ocr_reader, image_arrays=arr_images)

                return {"TEXT": extracted_text}
            except Exception as e:
                return {"ERROR": str(e)}

        else:
            return {"ERROR": f"file type is not allowed, Allowed types {str(list_allowed_file_types)}"}


api.add_resource(ApplyOCR, '/api/getTextfromImage')
if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=8081, debug=True)
    app.run()
