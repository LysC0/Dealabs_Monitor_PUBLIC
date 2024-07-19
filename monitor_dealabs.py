"""
Dealabs Monitor
@LysC0
"""

# "" # " # LIB # " # "" # 

from rich.console import Console
from rich.table import Table

#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
from time import strftime
import requests
import json
import time
import os

#"""# selenium settings #"""#

options = Options()
#options.page_load_strategy = 'eager'
#options.add_argument('--headless')

#driver = webdriver.Chrome(options=options)
driver = webdriver.Safari(options=options)
print('--> Wait driver launch..')
driver.set_window_position(16000, 16000)

## required info ##

with open ('setup.json', 'r') as f :
    stock_main = []
    j = json.load(f)
    Range = j['Range']
    Webhook = j['Webhook']
    Master_link = j['Master_link']
    keyword = j['Keyword']
    await_time = j['await_time']

    for i in keyword :
        stock_main.append(i)

## function ##
        
def driver_locate_price(url_product) :
    try :
        driver.get(url_product)
        try : 
            btn = driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/div[3]/div[3]/div[2]/div/section/div/div/div/div/div/div[2]/div[3]/div/button[1]')
            btn.click()
        except : 
            pass 

        xx = url_product[-7:]

        try :
            c_price = driver.find_element(By.XPATH, f'//*[@id="thread_{xx}"]/div[2]/span/span[1]/span').text
        except :
            pass 

        try : 
            old_price = driver.find_element(By.XPATH, f'//*[@id="thread_{xx}"]/div[2]/span/span[2]').text
        except :
            old_price = None
            pass 

        try : 
            pourcentage = driver.find_element(By.XPATH, f'//*[@id="thread_{xx}"]/div[2]/span/span[3]').text
        except :
            pass 
            
        try : 
            prisse = driver.find_element(By.XPATH, f'//*[@id="thread_{xx}"]/div[2]/span/span/span').text
        except :
            pass 


        if prisse and old_price == None :
            return f"{prisse}"
        elif pourcentage and old_price and c_price :
            return f"{c_price} / {old_price} / {pourcentage}"
        else :
            return "Other or Free"
    except :
        pass

def found_product(num):
    r = HTMLSession()
    stock = [['',''], ['','']]
    
    x = 1
    y = -1
    while range(int(num)):

        if int(x) == int(num):
            exit()
        
        pat_h = strftime("%H:%M:%S") 
        time.sleep(0.4)

        base = r.get(Master_link)
        s = BeautifulSoup(base.text, 'lxml')

        article = s.find_all('article', {'class', 'thread cept-thread-item thread--type-list imgFrame-container--scale thread--deal'})

        for target in article:
            div = target.find('strong', {'class','thread-title'})
            break
 
        for result in div :
                    title = result.get('title')
                    href = result.get('href')
                    break
        
        for i in stock :
            if i[0] == title:
                break
        
        if title in i[0]:
                stock.append([title, href])
                x +=1
                instance(num, x, y, pat_h)
                      
        else :
            try : 
                stock.append([title, href])
                url = checker_img(href)
                y += 1
                
                
                #value_price = f"{driver_locate_price(href)[0]} / {driver_locate_price(href)[1]} / {driver_locate_price(href)[2]}"
                value = driver_locate_price(href)
                sender('True', Webhook, title, href, url, value)  
                instance(num, x, y, pat_h)
                print(f'\nproduct found : {title}\n')
                
            except :
                print('error')
                pass 
             
        # wait time ( sec )
            
        time.sleep(await_time)

def sender(var_sender, url, title, link, img, price) : 

    stock = []
    stock.append(title)

    for i in stock_main :
        if i.lower() in title.lower() :
            linkprod = f"https://www.dealabs.com/visit/threadmain/{link[-7:]}"
            title = stock[0]
            embed = {
                "title": ':sparkles: **Monitor dealabs .me** :sparkles:',
                "url" : linkprod,
                "description" : f":white_check_mark: Keyword **__{i}__** Found :white_check_mark:\n\n- **info  :  monitor dealabs**\n- **id  :  {link[-7:]}**",
                "color": 3120166,
                "fields": [
                    {"name": "__Title :__", "value": title, "inline": True},
                    {"name": "__Dealabs Link :__", "value": link, "inline": True},
                    {"name": "__Direct Link :__", "value": linkprod, "inline": True},
                    {"name": "__Price / Old Price / % :__", "value": price, "inline": True},
                    {"name": "", "value": "<@441531224557879307>"},
                ],

                "thumbnail": {
                    "url": img
                }
            }

            payload = {
                "content": "",
                "embeds": [embed]
            }

            response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        
            if response.status_code == 204:
                print('\033[1;32m')
                var_sender = 'None'
                break      
            else:
                print(f"\033[1;31mWebhook error: {response.status_code}\033[0m") 

    if var_sender == 'True' :
                linkprod = f"https://www.dealabs.com/visit/threadmain/{link[-7:]}"
                embed = {
                    'title' : ':sparkles: **Monitor dealabs .me** :sparkles:',
                    "url" : link,
                    "description" : f"- **info  :  monitor dealabs**\n- **id  :  {link[-7:]}**",
                    "color": 16777215,
                    "fields": [
                        {"name": "**Title :**", "value": title, "inline": True},
                        {"name": "**Dealabs Link :**", "value": link, "inline": True},
                        {"name": "**Direct Link :**", "value": linkprod, "inline": True},
                        {"name": "**Price / Old Price / % :**", "value": price, "inline": True},
                    ],           
                    "thumbnail" : {
                        "url" : img
                        }
                }      
                payload = {
                        "content": "",
                        "embeds": [embed]
                    }
                
                response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})   
                if response.status_code == 204:
                    print('\033[1;32m')                
                else:
                    print("\033[1;31mWebhook error :", response.status_code)
         
def checker_img(url):
    r = HTMLSession().get(url)
    base = r.text
    s = BeautifulSoup(base, 'lxml')
    
    span = s.find('section')

    for i in span :
        img = i.find_all('div')
        for a in img :
            im = a.find('picture')   
            try :
                for final in im :
                    r_img = final.get('srcset')[0:]
                    return r_img
            except TypeError:
                break

def instance(num_range, tr, found, time) :
    #os.system('cls') #windows clear
    os.system('clear') #mac/linux clear

    table = Table(style="White", border_style='bold', caption='Dealabs Monitor v1', show_lines=True)

    table.add_column("Range", style="cyan", justify='center')
    table.add_column("Found", style="green", justify='center')
    table.add_column("Time", style="cyan", justify='center')

    table.add_row(f"{tr}/{num_range}", f"{found}", f"{time}")

    console = Console()
    console.print(table)

# "" main "" #
    
def Dealabs_monitor() :
    try :
        found_product(Range)
    except requests.exceptions.MissingSchema :
        print('error on setup.json / check this file !')
    except requests.exceptions.ConnectionError as e:
        print('Error connection : wait')
        time.sleep(3)
    except UnboundLocalError :
        print('somethings wrong')

if __name__ == "__main__" :
    Dealabs_monitor()

"""
add feature :
. proxy 
. undetectable
"""