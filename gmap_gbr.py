from nntplib import NNTPPermanentError
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
test = ["Dentallabor für Prothesen"
"Dentallabor für Prothesen Dietlikon Zürich",
"Dentallabor für Prothesen Dietlikon",
"Labor für Zahnprothetik Dietlikon Zürich",
"Labor für Zahnprothetik Dietlikon",
"Dental Prothesen Dietlikon Zürich",
"Dental Prothesen Dietlikon",
"Prothetische Reparaturen Dietlikon Zürich",
"Dental Reparaturen Dietlikon Zürich",
"Dental Reparaturen Dietlikon",
"Zahnprothetik Reparaturen Dietlikon",
"Dental Retainer Dietlikon Zürich",
"Weitere Schienen Dietlikon Zürich",
"Weitere Schienen Dietlikon",
"Zahnprothesen Dietlikon",
"Atelier für Zahnprothesen Dietlikon Zürich",
"Atelier für Zahnprothesen Dietlikon",
"Zahnprothetik Dietlikon",
"Zahnprothetik Vollprothesen Dietlikon Zürich",
"Zahnprothetik Vollprothesen Dietlikon",
"Zahnprothetiker Dietlikon",
"Zahntechnisches Labor Mansour Dietlikon Zürich",
"Zahntechnisches Labor Mansour Dietlikon",
"Zahntechnikerin Dietlikon Zürich",
"Zahntechnikerin Dietlikon",
"Zahntechnisches Labor Dietlikon Zürich",
"Zahntechnisches Labor Dietlikon",
"Vollprothesen Dietlikon Zürich",
"Professionelle Zahntechnik Dietlikon Zürich",
"Professionelle Zahntechnik Dietlikon",
"Vollkeramischer Zahnersatz Dietlikon"
]

serp_ranks = defaultdict(list)
has_kp = {}
has_gbr = {}

for keyword in test[:2]:
    url = "https://www.google.com/search?q=" + keyword
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    organic_search_contaier = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "rso")))

    searches = organic_search_contaier.find_elements(By.CLASS_NAME, "MjjYud")
    url_ranks = list()
    title_ranks  = list()
    title_rank  = 1
    link_rank = 1
    for search in searches:
        try:
            title = search.find_element(By.TAG_NAME, "h3")
            link = search.find_element(By.TAG_NAME, "a").get_attribute('href')
            title_match = re.search(r"\bmyzahntechnik\b", title.text, re.IGNORECASE)
            link_match = re.search(r"\bmyzahntechnik\b", link, re.IGNORECASE)
            if title_match:
                title_ranks.append(title_rank)
                #print(title.text, title_rank)
                title_rank += 1
            else:
                title_rank += 1
            if link_match:
                url_ranks.append(link_rank)
                #print(link, link_rank)
                link_rank += 1
            else:
                link_rank +=1
        except:
            continue
    final_ranks = sorted(list(set(title_ranks).union(set(url_ranks))))
    if final_ranks is not None:
        serp_ranks[keyword] = final_ranks
    else:
        serp_ranks[keyword] = [0]
#=========================================================================================================    
    try:
        kp = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "rhs")))
        match = re.search(r'\bmyzahntechnik\b',kp.text,re.IGNORECASE)
        if match:
            has_kp[keyword] = 1
            #print("Has KP")
            try:
                gbr = kp.find_element(By.CLASS_NAME, "Ob2kfd")
                if gbr.text is not None:
                    has_gbr[keyword] = 1
                    #print("Has GBR")
            except:
                has_gbr[keyword] = 0
            
        else:
            has_kp[keyword] = 0
            has_gbr[keyword] = 0
            #print("Not in KP")
            #print("No GBR")
        
    except:
        has_kp[keyword] = 0
        has_gbr[keyword] = 0
        #print("Not in KP")
        #print("No GBR")
    time.sleep(1)
    
print(has_kp)
print(has_gbr)
print(serp_ranks)

