import cv2 
import pytesseract
import configparser
import json
from helper import ruttien_helper, chuyentien_helper, tietkiem_helper, tattoan_helper

config = configparser.ConfigParser()
config.read('ocr.cfg')


def execute_ocr(type_doc="", file_name=""):
    img = cv2.imread(file_name, 0)
    # print(img.shape)
    try:
        if config[type_doc]['size_image']:
            size_image = eval(config[type_doc]['size_image'])
            img = cv2.resize(img, size_image)
    except Exception as e:
        raise e
    finally:
        ocr_result = {}
        
        for key in config[type_doc]:
            if(key != "size_image") :
                field = eval(config[type_doc][key])
                #crop
                y,h,x,w = field[0], field[1], field[2],field[3]
                crop_img = img[y:y+h, x:x+w]
                # resize
                width = int(crop_img.shape[1] * field[4] / 100)
                height = int(crop_img.shape[0] * field[5] / 100)
                dim = (width, height)
                resized = cv2.resize(crop_img, dim)
                if field[6] == 1:
                    ret, resized = cv2.threshold(resized,field[8],255,cv2.THRESH_TRUNC)
                
                conf = ("--psm 11 --psm 3")
                result = pytesseract.image_to_string(resized)
                if (field[7] == 1):
                    conf = ("-l vie --psm 11 --psm 3")
                    result = pytesseract.image_to_string(resized, config=conf)
                
                   
                ocr_result[key] = result
                # if(key == "stk"):
                #     print(result) 
                #     cv2.imshow("money"+str(i), resized)
                #     cv2.waitKey(0)

        if(type_doc == "rut-tien"):
            return ruttien_helper.read_data(ocr_result['currency'],ocr_result['stk'],ocr_result['money'])
        elif(type_doc == "nop-tien"):
            return chuyentien_helper.read_data(ocr_result['currency'],ocr_result['stk'],ocr_result['money'])
        elif(type_doc == "tiet-kiem"):
            return tietkiem_helper.read_data(ocr_result['stk'],ocr_result['stks'],ocr_result['money'],ocr_result['currency'],ocr_result['kyhan'],ocr_result['laisuat'])
        elif(type_doc == "tat-toan"):
            return tattoan_helper.read_data(ocr_result['money'],ocr_result['stk'],ocr_result['stt'])       
 
