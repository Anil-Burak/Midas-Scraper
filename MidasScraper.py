import json
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

cService = webdriver.ChromeService(executable_path='C:\\Program Files (x86)\\chromedriver.exe')
driver = webdriver.Chrome(service=cService)
driver.get("https://www.getmidas.com/canli-borsa/")
driver.implicitly_wait(2)
driver.minimize_window()
driver.find_element(By.CLASS_NAME, "cookie-close-button").click()
driver.implicitly_wait(1)
driver.find_element(By.CLASS_NAME, "btn.btn-primary.w-100").click()

hisseSatirlari = driver.find_elements(By.TAG_NAME, "tr")
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
