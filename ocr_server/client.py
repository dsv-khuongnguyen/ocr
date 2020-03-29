import requests
import base64
import json
from utils import sysconfig


def send_request():
    with open("images/signature_1.png", "rb") as s1:
        with open("images/signature_2.png", "rb") as s2:
            img_1 = base64.encodebytes(s1.read()).decode()
            img_2 = base64.encodebytes(s2.read()).decode()
            data = {
                "images": [img_1, img_2]
            }

            url = "{}://{}:{}{}".format(sysconfig.server_protocol, sysconfig.server_ip,
                                        sysconfig.server_port, sysconfig.upload_image_api)
            response = requests.post(url, json=data)
            print("Score: {}".format(response.text))


if __name__ == "__main__":
    send_request()
