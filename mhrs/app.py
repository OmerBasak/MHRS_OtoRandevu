import requests, json, platform, os, sys
from termcolor import colored
import mhrs # Kod karmaşasından kurtulmak için modülleştirdim.

clear = "clear"
if platform.system() == "Windows": clear = "cls"
os.system(clear)

def idVerification(number: int) -> int:
    numberCheck = isinstance(number, int)
    if numberCheck:
        numberList = [int(x) for x in str(number)]
        if len(numberList) == 11:
            numberList = numberList[:9]

            tenDigit = ((numberList[0] + numberList[2] + numberList[4] + numberList[6] + numberList[8]) * 7)
            tenDigit = tenDigit - (numberList[1] + numberList[3] + numberList[5] + numberList[7])
            tenDigitLast = tenDigit % 10
            numberList.append(tenDigitLast)

            elevenDigit = sum(numberList)
            elevenDigitLast = elevenDigit % 10
            numberList.append(elevenDigitLast)

            result = "".join( [str(integer) for integer in numberList] )

            if int(result) == number: return True
            else: return False
        else: return False
    else: return False


token = ""
name = ""
while True:
    while True:
        print(colored('Tc Kimlik No: ', 'green'), end="")
        id = input("").replace(" ", "")
        check = idVerification(int(id))
        if check == True: break 
        else:
            print(colored('Kimlik numarası hatalı', 'light_red'))
            print(colored('Lütfen kontrol edip tekrar giriniz!', 'light_red'), end="\n\n")

    print(colored('Şifreniz: ', 'green'), end="")
    pwd = input("")
    
    rGetToken = mhrs.getToken(True, id, pwd)
    if rGetToken == "password": print(colored('Kimlik numarası hatalı', 'light_red'))
    elif len(rGetToken) == 2: break



name, token = rGetToken[0], rGetToken[1]

os.system(clear)

print(colored('Giriş Başarılı: ', 'light_green'), end="")
print(colored(name, 'white'))

while True:
    print(colored('Bilgilendirme İçin Mail Giriniz: ', 'dark_grey'), end="")
    mail = input()
    if "@" not in mail or "." not in mail: print(colored('Hatalı mail adresi !', 'light_red'), end="\n\n")
    else: break

print()

plate = 34
while True:
    print(colored('Şehrinizin Plaka Numarası (34, 06 vb.): ', 'dark_grey'), end="")
    plate = input().replace(" ", "") # User yanlışlıkla boşluk bırakabilir.
    if not plate.isdigit() or int(plate) > 81: print(colored('Lütfen 34, 06 şeklinde şehrin plakasını giriniz!', 'light_red'), end="\n\n")
    else: break

os.system(clear)
print(colored('        Aktif Kullanıcı: ', 'light_green'), end="")
print(colored(name, 'white'))

data_ = mhrs.getIlce(plate, token)
liste, liste2 = dict(), dict()

liste["-1"] = "0 -> Fark etmez"
liste2["0"] = "-1"

count = 0
for data in data_:
    count+=1
    liste[data["value"]] = "{0} -> {1}".format(str(count), data["text"])
    liste2[str(count)] = data["value"]

print(colored('İlçe Kodlari ;', 'light_cyan'))

count = 0
for data in liste.values():
    count+=1 # Daha okunur olması için
    if count % 2 != 0: print(colored(data, 'white'))
    else: print(colored(data, 'cyan'))
print(colored("e -> Şehir değiştir.", 'light_magenta'), end="\n\n")

while True:
    print(colored('İlçe Numarasını Giriniz: ', 'dark_grey'), end="")
    district = input().replace(" ", "") # Kullanıcı yanlışlıkla boşluk bırakabilir.
    if district == "": district = "-1"
    elif district == "0": district = "-1"
    elif district == "e": pass # TODO: Bu özellik eklenecek.
    if district in liste2.keys(): 
        district = liste2[district]
        break
    else: print(colored('Lütfen bulunduğunuz ilçenin karşısındaki sayıyı giriniz!', 'light_red'), end="\n\n")

os.system(clear)
print(colored('        Aktif Kullanıcı: ', 'light_green'), end="")
print(colored(name, 'white'))

data_ = mhrs.getPolikinlik(plate, district, token)

liste, liste2 = dict(), dict()

liste2["0"] = "-1"

count = 0
for data in data_:
    count+=1
    liste[data["value"]] = "{0} -> {1}".format(str(count), data["text"])
    liste2[str(count)] = data["value"]

count = 0
print(colored('Polikinlik Kodlari ;', 'light_cyan'))
for data in liste.values():
    count+=1
    if count % 2 != 0: print(colored(data, 'white'))
    else: print(colored(data, 'cyan'))
print(colored("e -> İlçe değiştir.", 'light_magenta'), end="\n\n")

while True:
    print(colored('Polikinlik Numarasını Giriniz: ', 'dark_grey'), end="")
    polId = input().replace(" ", "")
    if polId == "e": pass # TODO: Bu özellik eklenecek.
    if polId in liste2.keys(): 
        polId = liste2[polId]
        break
    else: print(colored('Lütfen randevu alacağınız bölümün karşısındaki sayıyı giriniz!', 'light_red'), end="\n\n")

os.system(clear)
print(colored('        Aktif Kullanıcı: ', 'light_green'), end="")
print(colored(name, 'white'), end="\n\n")

print(colored('>>> Hizmetlerimiz <<<', 'light_cyan'))
print(colored("1) Otomatik Randevu Al", 'cyan'))
print(colored("2) Randevu Haber Ver", 'cyan'))

job = "2"
while True:
    print(colored('Seçiniz (1 veya 2): ', 'dark_grey'), end="")
    job = input()
    if job == "1" or job == "2": break
    else: print(colored('Lütfen 1 veya 2 arasından değer giriniz.', 'light_red'), end="\n\n")
print("\n\n")
if job == "2":
    available = set()
    count = 0
    while True:
        if len(available) != 0: print(colored('Müsait olduğunuz tarihler; ', 'light_cyan'))
        for ava in available: 
            count+=1
            if count % 2 != 0: print(colored(ava, 'white'))
            else: print(colored(ava, 'cyan'))
        if len(available) != 0: print()
        
        
        print(colored('Onayla: o', 'light_red'))
        print(colored('Müsait olduğunuz bir tarih giriniz gün/ay (27.5): ', 'dark_grey'), end="")
        days = input()
        if days == "o":
            if len(available) >= 1: break
            else: print(colored('En az 1 gün belirtmelisiniz!', 'light_red'))
        if days.count(".") != 1: print(colored('Lütfen gün.ay cinsinden giriniz: 25.11 gibi', 'light_red'))
        else:
            available.add(days + ".2023")
            os.system(clear)

    os.system(clear)
    print(colored('        Aktif Kullanıcı: ', 'light_green'), end="")
    print(colored(name, 'white'))

    print(colored('Müsait günleriniz; ', 'light_cyan'))
    count = 0
    for ava in available: 
        count+=1
        if count % 2 != 0: print(colored(ava, 'white'))
        else: print(colored(ava, 'cyan'))
    print()

    resultSearch = mhrs.getData(plate, district, polId, token)
    data = resultSearch.json()["data"]

    hastane, semt = data["hastane"], data["semt"]
    hospitalNames, hospitalList = set(), dict()

    for h in hastane: hospitalNames.add(h["kurum"]["kurumAdi"])
    for h in semt: hospitalNames.add(h["kurum"]["kurumAdi"])

    print(colored('Size Uyan Randevular; ', 'light_cyan'))
    for h in hastane:
        date = h["baslangicZamaniStr"]
        if date["tarih"] in available:
            hastaneAdi = h["kurum"]["kurumAdi"]
            hekimAdi = h["hekim"]["ad"] + " " + h["hekim"]["soyad"]
            text = hekimAdi + " " + date["tarih"] + " " + date["saat"]
            if hastaneAdi in hospitalList.keys():
                hospitalList[hastaneAdi]+="*"+text
            else:
                hospitalList[hastaneAdi]=text
            

    for h in semt:
        date = h["baslangicZamaniStr"]
        if date["tarih"] in available:
            hastaneAdi = h["kurum"]["kurumAdi"]
            hekimAdi = h["hekim"]["ad"] + " " + h["hekim"]["soyad"]
            text = hekimAdi + " " + date["tarih"] + " " + date["saat"]
            if hastaneAdi in hospitalList.keys():
                hospitalList[hastaneAdi]+="*"+text
            else:
                hospitalList[hastaneAdi]=text

    for hospitalName in hospitalList.keys():
        print(colored(hospitalName, 'green'))
        hastaneData = hospitalList[hospitalName].split("*")
        count = 0
        for hd in hastaneData:
            count+=1
            if count % 2 != 0: print(colored("        " + hd, 'light_yellow'))
            else: print(colored("        " + hd, 'cyan'))
        print("\n\n")

elif job == "1":
    print(colored('Yakında Eklnecek!', 'light_red'))
    sys.exit()