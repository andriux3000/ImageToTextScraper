from PIL import Image
from selenium import webdriver
import asyncio
import pytesseract
import os
import csv
from bs4 import BeautifulSoup as bs
import requests
from urllib3 import request
import time


pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


domain_url = 'https://www.busscenter.se'
url2019 = '/sv-SE/levererade-fordon-41765687'
url2018 = '/sv-SE/levererade-fordon-2018-38536624'
url2017 = '/sv-SE/levererade-fordon-2017-39256350'
url2016 = '/sv-SE/levererade-fordon-2016-39256280'
url2015 = '/sv-SE/levererade-fordon-2015-38920974'
url2014 = '/sv-SE/levererade-fordon-2014-38942241'
url2013 = '/sv-SE/levererade-fordon-2013-39068932'
url2012 = '/sv-SE/levererade-fordon-2012-39080725'
url2011 = '/sv-SE/levererade-fordon-2011-39070282'
url2010 = '/sv-SE/levererade-fordon-2010-39105173'

def filtras(x):
    if ("nummer" in x):
        return True
    elif ("Registrer" in x):
        return True
    elif ("Motor" in x):
        return True
    elif ("kW" in x):
        return True
    elif ("Vaxellada" in x):
        return True
    elif ("passagerare" in x):
        return True
    elif ("Lang" in x):
        return True
    elif ("klass" in x):
        return False
    elif (len(x)>=20):
        return True
    else:
        return False
    pass

async def screenshot(url):
    #options = webdriver.ChromeOptions()
    #options.add_argument('--ignore-certificate-errors')
    #options.add_argument("--test-type")
    #options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(r'C:/Users/andri/Downloads/chromedriver.exe')
    driver.get(url)
    driver.save_screenshot("screenshot.png")
    driver.close()
    img = Image.open("screenshot.png")
    text = pytesseract.image_to_string(img).splitlines()
    filtered = list(filter(filtras, text))
    print(text)
    print(filtered)
    bus_name = filtered[0]
    number = filtered[1].split(":")[1].strip().rstrip()
    year = filtered[2].split(":")[1].strip().rstrip()
    fuel = filtered[4].split(":")[1].strip().rstrip()
    power = filtered[5].split(":")[1].strip().rstrip()
    transmission = filtered[6].split(":")[1].strip().rstrip()
    passengers = filtered[7].split(":")[1].strip().rstrip()
    length = filtered[8].split(":")[1].strip().rstrip()
    data = [bus_name, number, year, fuel, power, transmission, passengers, length, url]
    with open('data.csv', mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
    csvfile.close()
    os.remove("screenshot.png")
    pass



async def main():
    url = domain_url + url2019
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    containers = soup.find_all("div", class_="h24_frame_frame_6_text")
    for container in containers:
        a_tag = container.find("a")
        link = a_tag['href']
        await screenshot(domain_url + link)
        pass
    pass

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
