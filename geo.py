from selenium import webdriver
import selenium
from selenium.webdriver.chrome.service import Service

def geoLocationTest():
    driver = webdriver.Chrome()
    Map_coordinates = dict({
        "latitude": 47.4226586,
        "longitude": 8.5920091,
        "accuracy": 100
        })
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", Map_coordinates)
    driver.get("https://www.google.com/search?q="+"Dentallabor für Prothesen")


geoLocationTest()