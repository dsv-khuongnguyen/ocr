
import re 

currencys = ['VND', 'USD', 'JPY', 'EUR', 'GBP', 'AUD', 'CAD']

def replace_char (text) :
    text = text.replace("Z", '7')
    text = text.replace('z', '7')
    text = text.replace("s", '5')
    text = text.replace('S', '5')
    text = text.replace("i", '1')
    text = text.replace('I', '1')
    text = text.replace("l", '1')
    text = text.replace('B', '8')
    text = text.replace('O', '0')
    text = text.replace('o', '0')
    return text

def read_file(data):
    # data = open(filename, 'r').read()
    return data

def digit_detect (text) :
    digit = re.findall(r'[\d]+', text)
    return digit


def tattoan_taikhoan_detect (text) :
    a = re.findall(r'[0-9]+[A-Z]', text)
    return a

# def tattoan_loaitien (filename) :
#     data = read_file(filename).replace(' ', '')
#     for i in currency:
#         if i in data:
#             currency = i
#         else:
            

def tattoan_money (filename) :
    data = read_file(filename)
    for i in currencys:
        if i in data:
            currency = i
            break
        else:
            continue

    data = data.split('\n')
    for text in data :
        digit = digit_detect(text)
        if len(digit)>0:
            money = ''.join(digit)
            break
    return currency, money

def tattoan_taikhoan (filename) :
    text = read_file(filename)
    try :
        tk = tattoan_taikhoan_detect(text)
        if ''.join(tk)[:-1].isdigit()==True:
            return ''.join(tk)
        else:
            return replace_char(''.join(tk)[:-1]) + ''.join(tk)[-1]
    except:
        return None

def tattoan_saving_id (filename) :
    text = read_file(filename).split()
    try:
        for i in range(len(text)):
            if "TP" in text[i] :
                stk_so = 'TP' + ''.join(digit_detect(''.join(text[i:])))[:7]
                return stk_so
            else:
                continue
    except:
        return None

def read_data (money_file, acc_file, saving_id_file) :
    result = {}
    a = tattoan_money(money_file)
    result['currency'] = a[0]
    result['money'] = a[1]
    result['id'] = tattoan_saving_id(saving_id_file)
    result['acc'] = tattoan_taikhoan(acc_file)
    return result

