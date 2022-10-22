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

start_time = time.time()

keywords_list=  [
'Ästhetischer Zahnersatz','Ästhetischer Zahnersatz aus Vollkeramik','Dentallabor für Prothesen','Dentallabor','Goldkronen','Implantatgetragenen Hybridprothesen',
'Hybridprothesen','KeramikImplantaten','Labor für Zahnprothetik','Metallfreier Zahnersatz','Metallfreier Zahnersatz mit Keramik Implantaten','Dental Prothesen','Prothetik',
'Prothetische Reparaturen','Schnarchschienen','Dental Reparaturen','Zahnprothetik Reparaturen','Dental Retainer','Retentionsschienen','Retentionsplatten','Teilprothesen','Teilprothetik',
'Totalprothesen','Weitere Schienen','Zahnprothesen','Atelier für Zahnprothesen','Zahnprothetik','Zahnprothetik Vollprothesen','Zahnprothetiker','Zahnschienen',
'Zahntechnisches Labor Mansour','Zahnmedizinische Prothetik','Zahntechnikerin','Zahntechnisches Labor','Unterfütterungen','Prothesenunterfütterung',
'Totalprothetik','Vollprothesen','Professionelle Zahntechnik','Michigan Schiene','Prothetiker','Vollkeramischer Zahnersatz','Zahnprotetik','Kieferorthopädie','Zahnweiss-Service',
'Ästhetik und Bleaching','Bleaching der Zähne','Bleichen und aufhellen','Zähne bleaching','Zähne bleichen','Zahnbleaching',
 'Zähne verschönern']

cities_list = ["Dietlikon Zürich", "Dietlikon", "Zürich"]

serp_ranks = defaultdict(list)
has_kp = dict()
has_gbr = {}
in_gmap = dict()
for keyword in keywords_list:
#=============================================== SERP ============================================================
    url = "https://www.google.ch/search?q=" + keyword
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    organic_search_contaier = WebDriverWait(driver, 0.5).until(
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
#========================================= KP & GBR ===============================================================
    try:
            kp = WebDriverWait(driver, 0.5).until(
            EC.presence_of_element_located((By.ID, "rhs"))
        )
            
            match = re.search(r'\bmyzahntechnik\b',kp.text,re.IGNORECASE)
            if match:
                has_kp[keyword] = 1
                # Check if GBRs within KP (assumes that if match, GBRs must be of match)
                try:
                    gbr = kp.find_element(By.CLASS_NAME, "Ob2kfd")
                    if gbr.text is not None:
                        has_gbr[keyword] = 1
                
                # If no GBRs at all    
                except:
                    has_gbr[keyword] = 0
            
            # If KP but no match
            else:
                has_kp[keyword] = 0
                has_gbr[keyword] = 0
    
    # If no KP at all        
    except:
        has_kp[keyword] = 0
        has_gbr[keyword] = 0


# ======================================= GMAP ===================================================================
    try:
        gmaps = WebDriverWait(driver, 0.5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "kuydt")))

        gmap_containers = gmaps.find_elements(By.CLASS_NAME, "VkpGBb")
        
        gmap_rank = 1
        for gmap_container in gmap_containers:
            match = re.search(r"\bmyzahntechnik\b", gmap_container.text, re.IGNORECASE)
            if not match:
                gmap_rank += 1
                continue
            if match:
                in_gmap[keyword] = gmap_rank
                gmap_rank += 1
        if keyword not in in_gmap:
            in_gmap[keyword] = 0
            
    except:
        in_gmap[keyword] = 0
    
    finally:
        driver.close()



#========================================== Inner Loop ============================================================
    for city in cities_list:
        query = keyword + " " + city
        url = "https://www.google.ch/search?q=" + query
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        organic_search_contaier = WebDriverWait(driver, 0.5).until(
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
            serp_ranks[query] = final_ranks
        else:
            serp_ranks[query] = [0]
        #========================================= KP & GBR ========================================================
        try:
                kp = WebDriverWait(driver, 0.5).until(
                EC.presence_of_element_located((By.ID, "rhs"))
            )
                
                match = re.search(r'\bmyzahntechnik\b',kp.text,re.IGNORECASE)
                if match:
                    has_kp[query] = 1
                    try:
                        gbr = kp.find_element(By.CLASS_NAME, "Ob2kfd")
                        if gbr.text is not None:
                            has_gbr[query] = 1
                    except:
                        has_gbr[query] = 0
            

                else:
                    has_kp[query] = 0
                    has_gbr[query] = 0
                
        except:
            has_kp[query] = 0
            has_gbr[query] = 0

        # ============================================== GMAP ======================================================        
        try:
            gmaps = WebDriverWait(driver, 0.5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "kuydt")))

            gmap_containers = gmaps.find_elements(By.CLASS_NAME, "VkpGBb")
            
            gmap_rank = 1
            for gmap_container in gmap_containers:
                match = re.search(r"\bmyzahntechnik\b", gmap_container.text, re.IGNORECASE)
                if not match:
                    gmap_rank += 1
                    continue
                else:
                    in_gmap[query] = gmap_rank
                    gmap_rank += 1
            if query not in in_gmap:
                in_gmap[query] = 0
                
        except:
            in_gmap[query] = 0

        finally:
            driver.close()

        time.sleep(0.5)

# =================================== Coalescing results in df =====================================================
max_ranks = [k for k in serp_ranks.keys() if sum(serp_ranks.get(k))==max([sum(n) for n in serp_ranks.values()])]
df = pd.DataFrame.from_dict(serp_ranks,orient="index", columns=["Rank" for i in range(len(serp_ranks[max_ranks[0]]))])
df['Has KP'] = df.index.map(has_kp)
df['Has GBR'] = df.index.map(has_gbr)
df['In GMAPs'] = df.index.map(in_gmap)
df.to_excel("complete.xlsx")
print((time.time()-start_time)/60, "mins")