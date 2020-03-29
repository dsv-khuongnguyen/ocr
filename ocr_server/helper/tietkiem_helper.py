# sotien, taikhoan

import re
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as distance

currencys = ['VND', 'USD', 'JPY', 'EUR', 'GBP', 'AUD', 'CAD']

def replace_char (text) :
    text = text.replace("Z", '7')
    text = text.replace('z', '7')
    text = text.replace("s", '5')
    text = text.replace('S', '5')
    text = text.replace("i", '1')
    text = text.replace('¡', '1')
    text = text.replace('I', '1')
    text = text.replace("l", '1')
    text = text.replace('B', '8')
    text = text.replace('O', '0')
    text = text.replace('o', '0')
    return text

def replace_char_money (text):
    text = text.replace(',', '')
    text = text.replace('.', '')
    text = text.replace(' ', '')
    return text
    
def read_file (data):
    # data = open(filename, 'r').read()
    return data

def digit_detect (text) :
    digit = re.findall(r'[\d]+', text)
    return digit

def acc_detect (text) :
    a = re.findall(r'[a-zA-Z0-9]+[A-Z]', text)
    return a

def detect_currency(filename):
    data = read_file(filename).split()
    cur = None
    for i in data :
        if i in currencys:
            cur = i
        else:
            continue

    if cur != None:
        return cur
    else:
        thres = 0.5
        for i in currencys :
            for j in data :
                if distance(i, j) < thres:
                    cur = i
                else:
                    continue
    return cur

def detect_interest (filename) :
    data = read_file(filename).replace('.', '').split()
    for i in data:
        if i.isdigit()==True and len(i)==3:
            return i[0]+'.'+i[1:]

def detect_saving_id (filename) :
    text = read_file(filename).split()
    try:
        for i in range(len(text)):
            if "TP" in text[i] :
                stk_so = 'TP' + replace_char(text[i][2:])
                return stk_so
            else:
                continue
    except:
        return None

def detect_period (filename) :
    thres = 0.4
    period = None
    data = read_file(filename).split('\n')
    for text in data:
        if distance(text[:6], 'Kỳ hạn') < thres:
            if distance(text.strip(' -')[-3:], 'Năm') < thres:
                period = digit_detect(replace_char(text.strip().replace(text[:6], '').replace(text[-3:], '')))[0] + ' Năm'
            else:
                period = digit_detect(replace_char(text.strip().replace(text[:6], '').replace(text[-5:], '')))[0] + ' Tháng'
        else:
            continue
    return period

def account_detect(filename) :
    data = read_file(filename).split('\n')
    for text in data:
        # print(text, len(acc_detect(text)))
        if len(acc_detect(text))>0:
            for i in acc_detect(text):
                if len(i) == 11:
                    return replace_char(i[:10]) + i[-1]
                else:
                    continue
        else:
            continue


for i in range(3):
    print(account_detect('tietkiem/taikhoan'+str(i+1)+'.txt'))

def read_data (period_file, interest_file, currency_file, money_file, saving_id_file, acc_file) :
    result = {}
    result['stk'] = account_detect(acc_file)
    result['kyhan'] = detect_period(period_file)
    result['laisuat'] = detect_interest(interest_file)
    result['currency'] = detect_currency(currency_file)
    result['stks'] = detect_saving_id(saving_id_file)
    result['money'] = None

    data = read_file(money_file).split('\n')
    for text in data :
        text = replace_char_money(text)
        if len(digit_detect(text)) > 0 :
            for i in digit_detect(text) :
                if len(i) > 3:
                    result['money'] = i[:-2]
                else:
                    continue
        else: continue
    return result

# def aa (money_file) :
#     data = read_file(money_file).split('\n')
#     for text in data :
#         text = replace_char_money(text)
#         if len(digit_detect(text)) > 0 :
#             for i in digit_detect(text) :
#                 if len(i) > 3:
#                     print(i[:-2])
#                 else:
#                     continue
#         else: continue

# for i in range(3):
#     aa('tietkiem/sotien'+str(i+1)+'.txt')
