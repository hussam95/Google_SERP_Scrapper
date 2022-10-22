from os import execv
import selenium
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_time = time.time()

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

has_kp = {}
for keyword in keyword_list: 
    url="https://www.google.com/search?q=" + keyword
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    try:
        main = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "rcnt"))
        )
        kp = main.find_element(By.ID, "rhs")
        match = re.search(r'\bmyzahntechnik\b',kp.text,re.IGNORECASE)
        if match:
            has_kp[keyword] = 1
            #print("MyZahntechnik appears in the KP against the enetered G-query")

        else:
            has_kp[keyword] = 0
            #print("Not in KP")
    except:
        has_kp[keyword] = 0

    finally:
        driver.quit()
    
    time.sleep(2)

    for city in cities_list:
        query = keyword + " " + city
        url="https://www.google.com/search?q=" + query
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)

        driver.get(url)

        try:
            main = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "rcnt"))
            )
            kp = main.find_element(By.ID, "rhs")
            match = re.search(r'\bmyzahntechnik\b',kp.text,re.IGNORECASE)
            if match:
                has_kp[query] = 1
                #print("MyZahntechnik appears in the KP against the enetered G-query")

            else:
                has_kp[query] = 0
                #print("Not in KP")
        except:
            has_kp[query] = 0

        finally:
            driver.quit()
        
        time.sleep(2)

df = pd.DataFrame.from_dict(has_kp, orient="index",columns=["Has Knowledge Panel"])
df = df.to_excel("has_kp.xlsx")
print((time.time() - start_time)/60, "mins")