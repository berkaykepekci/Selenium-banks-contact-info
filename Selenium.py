import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time

driver= selenium.webdriver.Firefox()

taban=sqlite3.connect("halkbank.db")
imlec=taban.cursor()



# sehirler=["istanbul","ankara","izmir","adana","antalya","aydin","bursa","denizli","samsun","trabzon","mugla","eskisehir","gaziantep","kocaeli","manisa","mersin","tekirdag","yalova","konya","balikesir"]

sehirler=["istanbul","ankara","izmir","adana","antalya","aydin","bursa","denizli","samsun","trabzon","mugla","eskisehir","gaziantep","kocaeli","manisa","mersin","tekirdag","yalova","konya","balikesir"]


for sehir in sehirler:

    sorgu1="CREATE TABLE IF NOT EXISTS {}(İsim TEXT,Adres TEXT,İletişim TEXT)".format(sehir)
    imlec.execute(sorgu1)
    taban.commit()


    url="https://www.bankalar.org/halkbankasi/subeler/{}-subeleri/".format(sehir)

    driver.get(url)

    elems = driver.find_elements_by_css_selector(".row [href]")
    links = [elem.get_attribute('href') for elem in elems]

    elems = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".row [href]")))


    linkler=[]

    for i in links:
        if "subesi" in i:
            linkler.append(i)

    def zamanla(fonksiyon):
        def wrapper(adres):
            baslama=time.time()
            fonksiyon(adres)
            bitis=time.time()
            sure=bitis-baslama
            print(fonksiyon.__name__ +"fonksiyonu {} saniye sürdü.".format(sure))

        return wrapper

    # @zamanla
    def subeanaliz(adres):

        driver.get(adres)
        liste=driver.find_elements_by_css_selector(".content")

        geçici1=liste[0].text.split(" ")
        şubesa=geçici1.index("Şubesinin")
        sonliste=geçici1[4:şubesa+1]
        isim=" ".join(sonliste)[:-3]

        tel=liste[1].text
        faks=liste[2].text
        adres=liste[3].text+" "+liste[4].text+" "+liste[5].text
        ilet="Telefon:{} Faks:{}".format(tel,faks)

        sorgu2="INSERT INTO {} VALUES(?,?,?)".format(sehir)
        imlec.execute(sorgu2,(isim,adres,ilet))
        taban.commit()


    for adres in linkler:
        try:
            subeanaliz(adres)
        except ValueError:
            continue