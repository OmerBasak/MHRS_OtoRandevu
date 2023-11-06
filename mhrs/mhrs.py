import requests, json, sys, datetime
from termcolor import colored
import time as t


headers = {
    'Host': 'prd.mhrs.gov.tr',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://mhrs.gov.tr/',
    'Origin': 'https://mhrs.gov.tr',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'tr-TR',
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'DELETE, POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Authorization,Content-Type, Accept, X-Requested-With, remember-me',
    'Access-Control-Allow-Credentials': 'true'
}

loginUrl = "https://prd.mhrs.gov.tr/api/vatandas/login"
searchUrl = "https://prd.mhrs.gov.tr/api/kurum-rss/randevu/slot-sorgulama/arama"
ilceUrl = "https://prd.mhrs.gov.tr/api/yonetim/genel/ilce/selectinput/"
polikinlik = "https://prd.mhrs.gov.tr/api/kurum/kurum/kurum-klinik/il/{0}/ilce/{1}/kurum/-1/aksiyon/200/select-input"

def getToken(first, id, pwd): # Excepts: password, token, again
    id, pwd = int(id), str(pwd) 

    loginJson = {"kullaniciAdi":int(id),"parola":pwd,"islemKanali":"VATANDAS_WEB","girisTipi":"PAROLA","captchaKey":None}

    while True:
        try:
            resultLogin = requests.post(loginUrl, json=loginJson, headers=headers, timeout=30)
            break
        except requests.exceptions.ConnectionError:
            print(colored("{0}: İnternet kesintisi !".format(datetime.datetime.now().strftime("%X")), 'light_red'))
            if first == True: sys.exit()
            else:
                while True:
                    try:
                        resultLogin = requests.post(loginUrl, json=loginJson, headers=headers, timeout=30)
                        break
                    except requests.exceptions.ConnectionError: t.sleep(15)
                break
    
    if resultLogin.status_code == 400: return "password"
    elif resultLogin.status_code == 200:
        data = resultLogin.json()["data"]
        token = data["jwt"]
        if token != "": 
            name = data["kullaniciAdi"] + " " + data["kullaniciSoyadi"]
            del(data)
            return (name, token)
        else: 
            print(colored("{0}: Token alınamadı.!".format(datetime.datetime.now().strftime("%X")), 'light_red'))
            if first == True: sys.exit()
            else: return "token"
    else: 
        print(colored("{0} getToken tanımlanmamış hata: ".format(datetime.datetime.now().strftime("%X")) + str(resultLogin.status_code), 'light_red'))
        if first == True: sys.exit()
        else: return "again" # Kullanıcının haberi olmayabilir, yazılım kapanmasın



def getIlce(plate, token):
    plate = str(plate)
    hWithToken = headers
    hWithToken["Authorization"] = 'Bearer {0}'.format(token)

    try:
        data = requests.get(ilceUrl + plate, headers=hWithToken, timeout=30).json()
    except requests.exceptions.ConnectionError:
        print(colored('İnternet kesintisi !', 'light_red'))
        print(colored('İlçeler alınamadı.', 'light_red'))
        sys.exit()
    return data

def getPolikinlik(plate, district, token):
    plate, district = str(plate), str(district)
    hWithToken = headers
    hWithToken["Authorization"] = 'Bearer {0}'.format(token)
    try:
        data = requests.get(polikinlik.format(str(plate), str(district)), headers=hWithToken, timeout=30).json()["data"]
        return data
    except requests.exceptions.ConnectionError:
        print(colored('İnternet kesintisi !', 'light_red'))
        print(colored('Polikinlik isimleri alınamadı.', 'light_red'))
        sys.exit()

def getData(plate, district, polId, token):
    plate, district, polId = int(plate), int(district), int(polId)

    hWithToken = headers
    hWithToken["Authorization"] = 'Bearer {0}'.format(token)

    searchValues = {"aksiyonId":"200","cinsiyet":"F","mhrsHekimId":-1,"mhrsIlId":plate,"mhrsIlceId":district,"mhrsKlinikId":polId,"mhrsKurumId":-1,"muayeneYeriId":-1,"tumRandevular":False,"ekRandevu":True,"randevuZamaniList":[]}
    try: 
        data = requests.post(searchUrl, json=searchValues, headers=hWithToken, timeout=30)
        return data
    except requests.exceptions.ConnectionError: pass