import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def getUrlContent(url,headers,timeout):
    html=requests.get(url,headers,timeout=timeout).text
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    return soup

def convertSoup(df,html_soap):
    tr_list = html_soap.find_all('tr')
    for tr in tr_list:
        td_list = tr.find_all('td')
        temp = {}
        if len(td_list) > 0:
            id, brand, car_type, car_model, problem_desc, problem_dict, complain_time, status = td_list[0].string, td_list[1].string, td_list[2].string, td_list[3].string, td_list[4].string, td_list[5].string, td_list[6].string, td_list[7].find('em').string
            temp['id'], temp['brand'], temp['car_type'], temp['car_model'], temp['problem_desc'], temp['problem_dict'], temp['complain_time'], temp['status'] = id, brand, car_type, car_model, problem_desc, problem_dict, complain_time, status
            df = df.append(temp, ignore_index=True)
    return df

base_url = "http://www.12365auto.com/zlts/19-0-0-0-0-0_0-0-"
headers = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
car_complain_list = pd.DataFrame(columns=['id','brand','car_type','car_model','problem_desc','problem_dict','complain_time','status'])
timeout = 100
for i in range(10):
    html_soap = getUrlContent(base_url + str(i) + '.shtml',headers,timeout)
    car_complain_list = convertSoup(car_complain_list,html_soap)
    print("第%d次成功"%i)
    time.sleep(90)
car_complain_list.to_csv('car_complain_list.csv',encoding='GBK')
