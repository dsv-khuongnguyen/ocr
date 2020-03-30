import time
import base64
import os
import random

from flask import Flask, request

from utils import sysconfig
from utils.logger import logger, logging_config
from request_manager import RequestManager
from flask_cors import CORS
from werkzeug.utils import secure_filename

from ocr import execute_ocr

app = Flask(__name__)
app.secret_key = os.urandom(24)

cors = CORS(app, resources={"*": {"origins": "*"}},supports_credentials=True)

import requests
import json


def save_images(request_id, images):
    if not os.path.isdir(sysconfig.data_dir):
        os.makedirs(sysconfig.data_dir)
    sub_dir = os.path.join(sysconfig.data_dir, request_id)
    if not os.path.isdir(sub_dir):
        os.makedirs(sub_dir)
    for index, image in enumerate(images):
        image.save(os.path.join(sub_dir, "{}.png".format(str(index))))


@app.route(sysconfig.upload_image_api, methods=sysconfig.upload_image_method)
def upload_images():
    try:
        images = request.files.values()
        # type_doc = request.data['type_doc']
        type_doc = "nop-tien"
        logger.info("Received new request from {}".format(request.remote_addr))

        request_id = time.strftime("%Y%M%d") + "_" + str(time.time())
        save_images(request_id, images)
        logger.info("name {}".format(sysconfig.data_dir+"/" +str(request_id)+"/0.png"))
        file_name = sysconfig.data_dir+"/" +str(request_id)+"/0.png"
        result = execute_ocr(type_doc=type_doc,file_name=file_name)
        logger.info(result)
        

        return app.response_class(
            status=200,
            response=json.dumps(result)
        )

    except Exception as e:
        logger.error(str(e))
        return app.response_class(
            status=200,
            response="Unresolved Error"
        )


if __name__ == "__main__":
    logging_config("Signature Server")
    request_manager = RequestManager()
    logger.info("Running thread request manger")
    request_manager.start()
    logger.info("Server running on {}:{}".format(sysconfig.server_ip, sysconfig.server_port))
    app.run(host=sysconfig.server_ip, port=sysconfig.server_port)
