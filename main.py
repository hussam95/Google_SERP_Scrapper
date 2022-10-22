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
from datetime import date
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
gbr_ranks = dict()
gmap_ranks = dict()

for keyword in keywords_list:
#=============================================== SERP ============================================================
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    url = "https://www.google.ch/search?q=" + keyword
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
#========================================= KP  ===============================================================
    try:
            kp = WebDriverWait(driver, 0.5).until(
            EC.presence_of_element_located((By.ID, "rhs"))
        )
            
            match = re.search(r'\bmyzahntechnik\b',kp.text,re.IGNORECASE)
            if match:
                has_kp[keyword] = 1   
            else:
                has_kp[keyword] = 0
                      
    except:
        has_kp[keyword] = 0
        

# ======================================= GBR ===================================================================
    try:
        gbrs = WebDriverWait(driver, 0.5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "kuydt")))

        gbr_containers = gbrs.find_elements(By.CLASS_NAME, "VkpGBb")
        gbr_container_length = len(gbr_containers)
        gbr_rank = 1
        for gbr_container in gbr_containers:
            match = re.search(r"\bmyzahntechnik\b", gbr_container.text, re.IGNORECASE)
            if not match:
                gbr_rank += 1
                continue
            if match:
                gbr_ranks[keyword] = f"{gbr_rank}/{gbr_container_length}"
                gbr_rank += 1
        if keyword not in gbr_ranks:
            gbr_ranks[keyword] = f"0/{gbr_container_length}"
            
    except:
        gbr_ranks[keyword] = 0
    
    finally:
        driver.close()
    
#======================================== GMAP ===================================================================
    
    url = "https://www.google.ch/maps/search/" + keyword
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    try:  
      gmaps = driver.find_element(By.CLASS_NAME,"w6VYqd")
      gmap_listings = re.findall(r".+?(?=Directions)", gmaps.text, re.DOTALL)
      gmap_listings_length = len(gmap_listings)
      for index,gmap_listing in enumerate(gmap_listings):
        if re.search(r"\bmyzahntechnik\b", gmap_listing, re.IGNORECASE):
          gmap_ranks[keyword] = f"{index + 1}/{gmap_listings_length}"
          
      if keyword not in gmap_ranks:
        gmap_ranks[keyword] = f"0/{gmap_listings_length}"

    except:
      gmap_ranks[keyword] = 0

    finally:
      driver.close()

    time.sleep(0.5)



#========================================== Inner Loop ============================================================
    for city in cities_list:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        query = keyword + " " + city
        url = "https://www.google.ch/search?q=" + query
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
        #========================================= KP  ========================================================
        try:
                kp = WebDriverWait(driver, 0.5).until(
                EC.presence_of_element_located((By.ID, "rhs"))
            )
                
                match = re.search(r'\bmyzahntechnik\b',kp.text,re.IGNORECASE)
                if match:
                    has_kp[query] = 1
                    
                else:
                    has_kp[query] = 0         
        except:
            has_kp[query] = 0
            
        # ============================================== GBR ======================================================        
        try:
          gbrs = WebDriverWait(driver, 0.5).until(
              EC.presence_of_element_located((By.CLASS_NAME, "kuydt")))

          gbr_containers = gbrs.find_elements(By.CLASS_NAME, "VkpGBb")
          gbr_container_length = len(gbr_containers)
      
          gbr_rank = 1
          for gbr_container in gbr_containers:
              match = re.search(r"\bmyzahntechnik\b", gbr_container.text, re.IGNORECASE)
              if not match:
                  gbr_rank += 1
                  continue
              if match:
                  gbr_ranks[query] = f"{gbr_rank}/{gbr_container_length}"
                  gbr_rank += 1
          if query not in gbr_ranks:
              gbr_ranks[query] = f"0/{gbr_container_length}"
              
        except:
          gbr_ranks[query] = 0
      
        finally:
          driver.close()

        time.sleep(1)

# ========================================== GMAP ================================================================
        
        url = "https://www.google.ch/maps/search/" + query
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        try:
          gmaps = driver.find_element(By.CLASS_NAME,"w6VYqd")
          gmap_listings = re.findall(r".+?(?=Directions)", gmaps.text, re.DOTALL)
          gmap_listings_length = len(gmap_listings)
          for index,gmap_listing in enumerate(gmap_listings):
            if re.search(r"\bmyzahntechnik\b", gmap_listing, re.IGNORECASE):
              gmap_ranks[query] = f"{index + 1}/{gmap_listings_length}"
            
              
          if query not in gmap_ranks:
            gmap_ranks[query] = f"0/{gmap_listings_length}"  
        except:
          gmap_ranks[query] = 0

        finally:
          driver.close()
        time.sleep(1)

# =================================== Coalescing results in df =====================================================
max_ranks = [k for k in serp_ranks.keys() if sum(serp_ranks.get(k))==max([sum(n) for n in serp_ranks.values()])]
try:
  df = pd.DataFrame.from_dict(serp_ranks,orient="index", columns=[f"SERP Rank {date.today()}" for i in range(len(serp_ranks[max_ranks[0]]))])
except:
  df = pd.DataFrame.from_dict(serp_ranks,orient="index", columns=[f"SERP Rank {date.today()}" for i in range(len(serp_ranks[max_ranks[0]])+1)])

df['Has KP'] = df.index.map(has_kp)
df['GBR'] = df.index.map(gbr_ranks)
df["GMAPs Ranks"] = df.index.map(gmap_ranks)
df.to_excel("MyZahntechnik GSERP.xlsx", index_label="Keywords + Cities")

print((time.time()-start_time)/60, "mins")