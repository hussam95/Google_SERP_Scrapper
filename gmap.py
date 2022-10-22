from email.policy import default
from regex import IGNORECASE
import selenium
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
cities_list = ["Dietlikon Zürich", "Dietlikon", "Zürich"]

keyword_list=  [
'Ästhetischer Zahnersatz','Ästhetischer Zahnersatz aus Vollkeramik','Dentallabor für Prothesen','Dentallabor','Goldkronen','Implantatgetragenen Hybridprothesen',
'Hybridprothesen','KeramikImplantaten','Labor für Zahnprothetik','Metallfreier Zahnersatz','Metallfreier Zahnersatz mit Keramik Implantaten','Dental Prothesen','Prothetik',
'Prothetische Reparaturen','Schnarchschienen','Dental Reparaturen','Zahnprothetik Reparaturen','Dental Retainer','Retentionsschienen','Retentionsplatten','Teilprothesen','Teilprothetik',
'Totalprothesen','Weitere Schienen','Zahnprothesen','Atelier für Zahnprothesen','Zahnprothetik','Zahnprothetik Vollprothesen','Zahnprothetiker','Zahnschienen',
'Zahntechnisches Labor Mansour','Zahnmedizinische Prothetik','Zahntechnikerin','Zahntechnisches Labor','Unterfütterungen','Prothesenunterfütterung',
'Totalprothetik','Vollprothesen','Professionelle Zahntechnik','Michigan Schiene','Prothetiker','Vollkeramischer Zahnersatz','Zahnprotetik','Kieferorthopädie','Zahnweiss-Service',
'Ästhetik und Bleaching','Bleaching der Zähne','Bleichen und aufhellen','Zähne bleaching','Zähne bleichen','Zahnbleaching',
 'Zähne verschönern']

gmap_ranks ={}
for keyword in keyword_list[:3]:
    url = "https://www.google.ch/maps/search/" + keyword
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    #try:

    gmaps = driver.find_element(By.CLASS_NAME,"w6VYqd")
    gmap_listings = re.findall(r".+?(?=Directions)", gmaps.text, re.DOTALL)
    gmap_listings_length = len(gmap_listings)
    for index,gmap_listing in enumerate(gmap_listings):
        if re.search(r"\bmyzahntechnik\b", gmap_listing, re.IGNORECASE):
            gmap_ranks[keyword] = f"{index+1}/{gmap_listings_length}"
    if keyword not in gmap_ranks:
        gmap_ranks[keyword] = f"0/{gmap_listings_length}"
    time.sleep(2)
    for city in cities_list:
        query = keyword + " " + city
        url = "https://www.google.ch/maps/search/" + query
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        #try:

        gmaps = driver.find_element(By.CLASS_NAME,"w6VYqd")
        gmap_listings = re.findall(r".+?(?=Directions)", gmaps.text, re.DOTALL)
        gmap_listings_length = len(gmap_listings)
        for index,gmap_listing in enumerate(gmap_listings):
            if re.search(r"\bmyzahntechnik\b", gmap_listing, re.IGNORECASE):
                gmap_ranks[query] = f"{index+1}/{gmap_listings_length}"
        if query not in gmap_ranks:
            gmap_ranks[query] = f"0/{gmap_listings_length}"
        time.sleep(2)

print(gmap_ranks)