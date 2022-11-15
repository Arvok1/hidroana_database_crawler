import os
import sys

import logging.config
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.chrome.options import Options
import random
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [PID %(process)d] [Thread %(thread)d] [%(levelname)s] [%(name)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ]
    }
})


URL_TO_CRAWL = "https://www.snirh.gov.br/hidroweb/serieshistoricas"
LOGGER = logging.getLogger()
checked_checkbox = 0
#FUCK A BACIA VAMO BAIXAR TUDO


def run(driver):
    num_retries_attempted = 0
    driver.get(URL_TO_CRAWL)
    set_viewport_size(driver=driver)
    pesquisa_inicial(driver)
    change_quantity_per_page(driver)
    while checked_checkbox < 37570:
        time.sleep(5)
        select_checkbox(driver)
        time.sleep(1)
        download(driver)
        next_page(driver)

        
    



def pesquisa_inicial(driver):
    xpath = "//button[contains(@type,'submit')]"
    wait_until_clickable(driver, xpath=xpath)
    driver.find_element("xpath", xpath).click()


def select_checkbox(driver):
    checkboxes = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='mat-checkbox-inner-container mat-checkbox-inner-container-no-side-margin']")))
    for checkbox in checkboxes:
        
        #driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        if not checkbox.is_selected():
            checkbox.click() # to tick it

def download(driver):
    
    xpath_2 = "//div[@class= 'mat-radio-inner-circle' ]"
    wait_until_clickable(driver, xpath = xpath_2)
    driver.find_element("xpath",xpath_2).click() #selecionando mdb
    xpath = "//a[@class='mat-raised-button mat-primary']"
    driver.find_element("xpath", xpath).click()
    time.sleep(15)

def change_quantity_per_page(driver):
    xpath = "//mat-select[@aria-label='Qtd. por página:']"
    driver.find_element("xpath", xpath).click()
    xpath_2 = "//span[text()='100']"
    driver.find_element("xpath", xpath_2).click()


def next_page(driver):
    xpath = "//button[@class='mat-paginator-navigation-next mat-icon-button']"
    wait_until_clickable(driver, xpath=xpath)
    driver.find_element("xpath", xpath).click()



def wait_until_clickable(driver, xpath=None, class_name=None, id=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
    elif id:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.ID, id)))

def wait_until_visible(driver, xpath=None, class_name=None, id=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
    elif id:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.ID, id)))

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

def set_viewport_size(driver, width=1200, height=1200):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

if __name__ == "__main__":
    
    driver = None


    options = uc.ChromeOptions()
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
    print(userAgent)
    ##'geolocation': 2, 'durable_storage': 2, 
    
    # prefs = {'profile.default_content_setting_values': { 'images': 2,
    #                    'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
    #                    'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
        #                   'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
        #                   'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
        #                   'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
        #                   'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 'dom.webdriver.enabled': 2, 'useAutomationExtension':2}}
    #options.add_experimental_option('prefs', prefs)
    #options.add_argument("--start-maximized")
    #options.add_argument("--disable-infobars")
    #options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", {
    "download.default_directory": r"C:\Users\david\Desktop\IC",
    "download.prompt_for_download": True,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
    })

    #options.add_argument("--incognito")
    #options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--lang=pt-br")
    #options.add_argument("--disable-blink-features=AutomationControlled") #


    if sys.platform == "darwin":
        executable_path = "./bin/chromedriver_mac"
    elif "linux" in sys.platform:
        executable_path = "./bin/chromedriver_linux"
    elif "win32" in sys.platform:
        executable_path ="./bin/chromedriver_win"
    else:
        raise Exception("Unsupported operating system. Please add your own Selenium driver for it.")
    driver = uc.Chrome(options=options)
    #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    run(driver=driver)



