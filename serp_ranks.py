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

from bs4 import BeautifulSoup
import pandas as pd
import requests
import collections
import time
import re

start_time = time.time()
serp_rank = collections.defaultdict(list)
for keyword in keyword_list:
  url= ("https://www.google.com/search?q=" + keyword)
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html.parser")
  links = soup.findAll("a")
  l1 = 0
  t1 = 0 
  for index,link in enumerate(links):
    link_href = link.get('href')
    if "url?q=" in link_href and not "webcache" in link_href:
        title = link.find_all('h3')
        
        if len(title) > 0:
            link = (link.get('href').split("?q=")[1].split("&sa=U")[0])
            title = (title[0].getText())
            l1 += 1
            t1 += 1
            match1 = re.search(r'\bmyzahntechnik\b',link,re.IGNORECASE)
            #print(link)
            #print(title)
            if match1:
              serp_rank[keyword].append(l1)
              #print(link, i)
              
              continue
            match2 = re.search(r'\bmyzahntechnik\b',title,re.IGNORECASE)
            if match2:
              serp_rank[keyword].append(t1)
              #print(title, i)
            if not match1 and not match2:
              serp_rank[keyword].append(0)
                          
  time.sleep(0.5)   
  for city in cities_list:
    query = keyword+ " "+city
    url = "https://www.google.com/search?q="+keyword+ " "+city
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.findAll("a")
    l2 = 0
    t2 = 0  
    for index,link in enumerate(links):
      link_href = link.get('href')
      if "url?q=" in link_href and not "webcache" in link_href:
          title = link.find_all('h3')
          
          if len(title) > 0:
              link = (link.get('href').split("?q=")[1].split("&sa=U")[0])
              title = (title[0].getText())
              l2 += 1
              t2 += 1
              match1 = re.search(r'\bmyzahntechnik\b',link,re.IGNORECASE)
              #print(link)
              #print(title)
              if match1:
                serp_rank[query].append(l2)
                #print(link, i)
                
                continue
              match2 = re.search(r'\bmyzahntechnik\b',title,re.IGNORECASE)
              if match2:
                serp_rank[query].append(t2)
                #print(title, i)
              if not match1 and not match2:
                serp_rank[query].append(0)
                            
    time.sleep(0.5)   

max_ranks = [k for k in serp_rank.keys() if sum(serp_rank.get(k))==max([sum(n) for n in serp_rank.values()])]
df=pd.DataFrame.from_dict(serp_rank,orient="index", columns=["Rank" for i in range(len(serp_rank[max_ranks[0]]))])
df.to_excel("SERP.xlsx")
print(time.time() - start_time, "seconds")