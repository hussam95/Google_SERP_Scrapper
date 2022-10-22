from encodings import search_function
from os import execv
from pyexpat import EXPAT_VERSION
from tkinter import N
from matplotlib import collections
from matplotlib.pyplot import text
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


serp_ranks = defaultdict(list)
has_kp = dict()

for keyword in keyword_list:
    url = "https://www.google.com/search?q=" + " " + keyword
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    organic_search_contaier = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "rso")))

    search_result_headlines = organic_search_contaier.find_elements(By.CSS_SELECTOR, "h3")

    
    headline_ranks =list()
    headline_rank = 1
    for search_result_headline in search_result_headlines:
        ignore = re.search(r"^(Images)", search_result_headline.text, re.IGNORECASE) 
        match = re.search(r"\bmyzahntechnik\b", search_result_headline.text, re.IGNORECASE)
        if not ignore:
            if match:
                headline_ranks.append(headline_rank)
                #print(search_result_headline.text, rank)
                headline_rank += 1
            if not match:
            #print(search_result_headline.text, rank)
                headline_rank += 1

    search_result_urls = organic_search_contaier.find_elements(By.CSS_SELECTOR, "a")

    url_ranks = list()
    url_rank = 1
    for search_result_url in search_result_urls:
        try:
            href = search_result_url.get_attribute("href")
            # ignores google translate and google images urls
            ignore = re.search(r"\bgoogle.com\b", href, re.IGNORECASE) 
            match = re.search(r"\bmyzahntechnik\b", href, re.IGNORECASE)
            if not ignore:
                if match:
                    url_ranks.append(url_rank)
                    #print(href, rank)
                    url_rank += 1
                if not match:
                    url_rank += 1

        except Exception as e:
            print(e, keyword)
            continue            
    
    final_ranks = sorted(list(set(headline_ranks).union(set(url_ranks))))
    if final_ranks is not None:
        serp_ranks[keyword] = final_ranks
    else:
        serp_ranks[keyword] = [0]

    
    try:
        kp = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "rhs"))
        )

        
        
        # This is KP
        
        match = re.search(r'\bmyzahntechnik\b',kp.text,re.IGNORECASE)
        if match:
            has_kp[keyword] = 1
            #print("MyZahntechnik appears in the KP against the enetered G-query")

        else:
            has_kp[keyword] = 0
            #print("Not in KP")
    except:
        has_kp[keyword] = 0

    #finally:
        #driver.quit()
    
    time.sleep(1)


    # Let's do headlines union urls


    for city in cities_list:
        query = keyword + " " + city
        url = "https://www.google.com/search?q=" + " " + query
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(url)


        organic_search_contaier = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "rso")))

        search_result_headlines = organic_search_contaier.find_elements(By.CSS_SELECTOR, "h3")

        
        headline_ranks2 = list()
        rank = 1
        for search_result_headline in search_result_headlines:
            ignore = re.search(r"^(Images)", search_result_headline.text, re.IGNORECASE) 
            match = re.search(r"\bmyzahntechnik\b", search_result_headline.text, re.IGNORECASE)
            if not ignore:
                if match:
                    headline_ranks2.append(rank)
                    #print(search_result_headline.text, rank)
                    rank += 1
                if not match:
                #print(search_result_headline.text, rank)
                    rank += 1

        search_result_urls = organic_search_contaier.find_elements(By.CSS_SELECTOR, "a")

        url_ranks2 = list()
        rank = 1
        for search_result_url in search_result_urls:
            try:
                href = search_result_url.get_attribute("href")
                # ignores google translate and google images urls
                ignore = re.search(r"\bgoogle.com\b", href, re.IGNORECASE) 
                match = re.search(r"\bmyzahntechnik\b", href, re.IGNORECASE)
                if not ignore:
                    if match:
                        url_ranks2.append(rank)
                        #print(href, rank)
                        rank += 1
                    if not match:
                        rank += 1
            except Exception as e:
                print(e, query)
                continue

        final_ranks2 = sorted(list(set(headline_ranks2).union(set(url_ranks2))))
        if final_ranks2 is not None:
            serp_ranks[query] = final_ranks2
        else:
            serp_ranks[query] = [0]

        try:
            kp = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "rhs"))
        )
        # This is KP
            
            match = re.search(r'\bmyzahntechnik\b',kp.text,re.IGNORECASE)
            if match:
                has_kp[query] = 1
            #print("MyZahntechnik appears in the KP against the enetered G-query")

            else:
                has_kp[query] = 0
            #print("Not in KP")
        except:
            has_kp[query] = 0

        #finally:
            #driver.quit()
    
    time.sleep(1)

        

max_ranks = [k for k in serp_ranks.keys() if sum(serp_ranks.get(k))==max([sum(n) for n in serp_ranks.values()])]
df=pd.DataFrame.from_dict(serp_ranks,orient="index") #columns=["Rank" for i in range(len(serp_ranks[max_ranks[0]]))])
df['Has KP'] = df.index.map(has_kp)
df.to_excel("test3.xlsx")
print(serp_ranks)