import json
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By

parser = argparse.ArgumentParser(description="Hisse senetleri işleyen program.")
parser.add_argument("-yenile",type=int, choices=[0,1], help="Verileri güncelle")
parser.add_argument("-artan", action="store_true", help="Artan hisseleri göster")
parser.add_argument("-azalan", action="store_true", help="Azalan hisseleri göster")
parser.add_argument("-hisseSor", type=str, help="Sorulan hissenin verilerini göster")


def yenile(outputCheck):
    driver = webdriver.Chrome()
    driver.get("https://www.getmidas.com/canli-borsa/")
    driver.implicitly_wait(2)
    driver.minimize_window()
    driver.find_element(By.CLASS_NAME, "cookie-close-button").click()
    driver.implicitly_wait(1)
    driver.find_element(By.CLASS_NAME, "btn.btn-primary.w-100").click()
    hisseSatirlari = driver.find_elements(By.TAG_NAME, "tr")[1:]
    tumVeriler = []
    for i in range(len(hisseSatirlari)):
        seciliTr = hisseSatirlari[i]
        tdList = seciliTr.find_elements(By.TAG_NAME, "td")
        tdVerileri = [td.text for td in tdList]
        tumVeriler.append(tdVerileri)
    driver.quit()
    if outputCheck:
        print("Hisse	Son	Alış	Satış	Fark	En Düşük	En Yüksek	AOF	Hacim TL	Hacim Lot")
        for satir in tumVeriler:
            print(satir)
    else:
        print("Güncelleme yapıldı.")



    hisseAlanlari = ["Hisse", "Son", "Alis", "Satis", "Fark", "En Dusuk",
                     "En Yuksek", "AOF", "Hacim TL", "Hacim Lot"]

    tumVeriler_dict = [dict(zip(hisseAlanlari, hisse)) for hisse in tumVeriler]

    with open("hisse-verileri.json", "w") as hv:
        json.dump(tumVeriler_dict, hv, indent=2)


def artan():
    with open('hisse-verileri.json', 'r') as file:
        maks = 0
        okunanVeriler = json.load(file)
        for hisse in okunanVeriler:
            try:
                fark = float(hisse["Fark"].replace(',', '.').replace('%', ''))
                if fark > 0:
                    if fark > maks:
                        maks = fark
                        maksHisse = hisse['Hisse']
                    print(hisse['Hisse'],end="  ")
                    print(hisse['Fark'])
            except ValueError:
                continue
        print(f"Günün en çok artan hissesi {maksHisse}, artış: {maks}")


def azalan():
    with open('hisse-verileri.json', 'r') as file:
        min = 0
        okunanVeriler = json.load(file)
        for hisse in okunanVeriler:
            try:
                fark = float(hisse["Fark"].replace(',', '.').replace('%', ''))
                if fark < 0:
                    if fark < min:
                        min = fark
                        minHisse = hisse['Hisse']
                    print(hisse['Hisse'], end="  ")
                    print(hisse['Fark'])
            except ValueError:
                continue
        print(f"Günün en çok düşen hissesi {minHisse}, düşüş: {min}")



def hisseSor(hisseAdi):
    try:
        with open('hisse-verileri.json', 'r') as file:
            okunanVeriler = json.load(file)
            for hisse in okunanVeriler:
                if hisse.get("Hisse") == hisseAdi:
                    for key, value in hisse.items():
                        print(f"{key}: {value}")
                    return
            print(f"'{hisseAdi}' adında bir hisse bulunamadı.")

    except FileNotFoundError:
        print("Hisse verileri dosyası bulunamadı. Önce -yenile çalıştırın.")


args = parser.parse_args()
if args.yenile is not None:
    yenile(args.yenile)
elif args.artan:
    artan()
elif args.azalan:
    azalan()
elif args.hisseSor:
    hisseSor(args.hisseSor.upper())