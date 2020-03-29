
import re
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as distance

currency = ['VND', 'USD', 'JPY', 'EUR', 'GBP', 'AUD', 'CAD']

def replace_char (text):
    text = text.replace(',', '')
    text = text.replace('.', '')
    text = text.replace(' ', '')
    return text


def read_file (data) :
    # data = open(filename, 'r').read()
    return data

def speical_digit_detect(text) :
    return __speical_digit_detect(text)


def __speical_digit_detect (text) :
    percent = re.findall(r'[\d]+%',text)
    digit = re.findall(r'[\d]+', text)
    a = re.findall(r'[a-zA-Z]+[0-9]+[a-zA-Z]', text)
    return percent + digit + a


def read_money (filename) :
    texts = read_file(filename).split('\n')
    for text in texts :
        digit = re.findall(r'[\d]+', replace_char(text))
        if len(digit)==1 and len(digit[0])>3:
            return digit[0]
            # return ','.join(digit)
        else:
            continue


def stk_detect (filename) :
    text = read_file(filename)
    a = speical_digit_detect(text)
    if len (a) > 0:
        for i in a :
            if len(i) == 11 and i.isdigit()==True :
                return i
            elif len(i) > 3:
                return '*******'+i[-4:]
            else :
                continue
    else :
        return []


def detect_currency(filename):
    data = read_file(filename).split()
    cur = None
    for i in data :
        if i in currency:
            cur = i
        else:
            continue

    if cur != None:
        return cur
    else:
        thres = 0.5
        for i in currency :
            for j in data :
                if distance(i, j) < thres:
                    cur = i
                else:
                    continue
    return cur

def read_data (currency, stk, money) :
    result = {}
    result['money'] = read_money(money)
    result['currency'] = detect_currency(currency)
    result['stk'] = stk_detect(stk)
    return result

# print(stk_detect('stk/cropped12.txt'))
# for i in range(25):
#     print(i+1, ' ___ ', stk_detect('stk/cropped'+str(i+1)+'.txt'))

# print(read_money('money/money7.txt'))
# for i in range(25):
#     print(i+1, ' ___ ', read_money('money/money'+str(i+1)+'.txt'))

# print(detect_currency('currency/currency5.txt'))
# for i in range(25):
#     print(i+1, ' ___ ', detect_currency('currency/currency'+str(i+1)+'.txt'))
# for i in range(76, 100):
#     print(i, ' ___ ', detect_currency('currency/currency'+str(i)+'.txt'))






