
import re
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as distance
import string
import locale

locale.setlocale( locale.LC_ALL, '' )
punct = set(string.punctuation)

def remove_punct (text) :
    for i in punct :
        text = text.replace(i, '')
    return text

def format_money (text) :
    if text != None :
        a = len(text)%3
        b = len(text)//3
        print(b)
        for i in range(1,b) :
            text = text.replace(text[-(4*i)], ','+text[-(4*i)])
            print(text)
        return text

currencys = ['VND', 'USD', 'JPY', 'EUR', 'GBP', 'AUD', 'CAD']

def read_file (data) :
    return data

def digit_detect (text) :
    digit = re.findall(r'[\d]+', text)
    return digit

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
    text = text.replace('§', '8')
    text = text.replace('O', '0')
    text = text.replace('o', '0')
    return text

def replace_char_money (text):
    text = text.replace(',', '')
    text = text.replace(' ', '')
    return text

def acc_detect (text) :
    a = re.findall(r'[a-zA-Z0-9§]+', text)
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
                if distance(i, remove_punct(j)) < thres:
                    cur = i
                else:
                    continue
    return cur

def stk_detect (filename) :
    text = read_file(filename)
    a = acc_detect(text)
    if len (a) > 0:
        for i in a :
            if len(i) == 11 and replace_char(i).isdigit()==True:
                return replace_char(i)
            else :
                continue
    else :
        return []

def read_data (currency_file, stk_file, money_file) :
    result = {}
    result['currency'] = detect_currency(currency_file)
    result['stk'] = stk_detect(stk_file)
    result['money'] = 0

    data = read_file(money_file).split('\n')
    for text in data :
        text = replace_char_money(text)
        if len(digit_detect(text)) > 0 :
            for i in digit_detect(text) :
                if result['currency'] == 'VND' and len(i) > 3:
                    result['money'] = i
                elif result['currency'] != 'VND':
                    result['money'] = i
                else :
                    continue
        else: continue
    return result

