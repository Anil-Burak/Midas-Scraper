import json
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By

# from selenium.webdriver.chrome.options import Options

parser = argparse.ArgumentParser(description="Hisse senetleri işleyen program.")
parser.add_argument("-yenile", action="store_true", help="Verileri güncelle")
parser.add_argument("-artan", action="store_true", help="Artan hisseleri göster")
parser.add_argument("-azalan", action="store_true", help="Azalan hisseleri göster")
parser.add_argument("-hisseSor", type=str, help="Sorulan hissenin verilerini göster")


def yenile():
    cService = webdriver.ChromeService(executable_path='C:\\Program Files (x86)\\chromedriver.exe')
    driver = webdriver.Chrome(service=cService)
    driver.get("https://www.getmidas.com/canli-borsa/")
    driver.implicitly_wait(2)
    driver.minimize_window()
    driver.find_element(By.CLASS_NAME, "cookie-close-button").click()
    driver.implicitly_wait(1)
    driver.find_element(By.CLASS_NAME, "btn.btn-primary.w-100").click()
    hisseSatirlari = driver.find_elements(By.TAG_NAME, "tr")[1:]
    tumVeriler = []
    print("Hisse	Son	Alış	Satış	Fark	En Düşük	En Yüksek	AOF	Hacim TL	Hacim Lot")
    for i in range(len(hisseSatirlari)):
        seciliTr = hisseSatirlari[i]
        tdList = seciliTr.find_elements(By.TAG_NAME, "td")
        tdVerileri = [td.text for td in tdList]
        tumVeriler.append(tdVerileri)

    for satir in tumVeriler:
        print(satir)
    driver.quit()

    hisseAlanlari = ["Hisse", "Son", "Alis", "Satis", "Fark", "En Dusuk",
                     "En Yuksek", "AOF", "Hacim TL", "Hacim Lot"]

    tumVeriler_dict = [dict(zip(hisseAlanlari, hisse)) for hisse in tumVeriler]

    with open("hisse-verileri.json", "w") as hv:
        json.dump(tumVeriler_dict, hv, indent=2)


def artan():
    with open('hisse-verileri.json', 'r') as file:
        okunanVeriler = json.load(file)
        for hisse in okunanVeriler:
            try:
                fark = float(hisse["Fark"].replace(',', '.').replace('%', ''))  # Yüzde işaretini kaldır
                if fark > 0:
                    print(hisse['Hisse'])
            except ValueError:
                continue


def azalan():
    with open('hisse-verileri.json', 'r') as file:
        okunanVeriler = json.load(file)
        for hisse in okunanVeriler:
            try:
                fark = float(hisse["Fark"].replace(',', '.').replace('%', ''))  # Yüzde işaretini kaldır
                if fark < 0:
                    print(hisse['Hisse'])
            except ValueError:
                continue


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
if args.yenile:
    yenile()
elif args.artan:
    artan()
elif args.azalan:
    azalan()
elif args.hisseSor:
    hisseSor(args.hisseSor.upper())