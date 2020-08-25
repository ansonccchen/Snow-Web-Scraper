import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL_PB1 = 'https://pacificboarder.com/catalog/product/mens/smartwool-phd-pro-free-ski-sock-2020/'
URL_Comor1 = 'https://comorsports.com/catalog/product/outerwear/smartwool-phd-pro-free-ski-sock-2020/'
URL_Comor2 = 'https://comorsports.com/catalog/product/outerwear/socks/smartwool-phd-ski-ultra-light-sock-2019/'
headers = {
    "User-Agent": 'UA'
    # replace UA with own User Agent by googling "my user agent"
}
def priceCheck():
    page_PB1 = requests.get(URL_PB1, headers=headers)
    page_Comor1 = requests.get(URL_Comor1, headers=headers)
    page_Comor2 = requests.get(URL_Comor2, headers=headers)

    soup_PB1 = BeautifulSoup(page_PB1.content, "html.parser")
    soup_Comor1 = BeautifulSoup(page_Comor1.content, "html.parser")
    soup_Comor2 = BeautifulSoup(page_Comor2.content, "html.parser")

    price_PB1 = float(soup_PB1.find('span', class_="price price-without-tax").text[1:])
    title_PB1 = soup_PB1.find("h1", class_="product-title").text

    price_Comor1 = float(soup_Comor1.find('span', class_="price price-without-tax").text[1:])
    title_Comor1 = soup_Comor1.find("h1", class_="product-title").text

    price_Comor2 = float(soup_Comor2.find('span', class_="price price-without-tax").text[1:])
    title_Comor2 = soup_Comor2.find("h1", class_="product-title").text

    if price_Comor1 < 19:
        sendEmail(title_Comor1, URL_Comor1)
    if price_Comor2 < 14:
        sendEmail(title_Comor2, URL_Comor2)
    if price_PB1 < 19:
        sendEmail(title_PB1, URL_PB1)
    print("no prices went down")

def sendEmail(title, link):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('q1', "q2") # replace q1 with email, replace q2 with email password

    subject = f'Price of {title} went down'
    body = f"Check this link: {link}"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        '', # write from email inside quotes
        "", # write to email inside quotes
        msg
    )
    print("success")
    server.quit()

while(True):
    priceCheck()
    time.sleep(60*60*24)