from selenium import webdriver
#import time
import json
import os
import psutil
import sys
cookie_txt = 'seisson_cookie.txt'
login_suc = "https://masters.caravan-stories.com.tw/game_start/launch"
cookie_temp = type(None)()

"""
#Try cookie file exsist
try:
    f = open(cookie_txt, 'r')
    for line in f.readlines():
        print(line)
except IOError:
    f = open(cookie_txt,'w')
    print(type(None),file=f)
    print("Cookie Not Found, Please Re-Login")
    if f:
        f.close()
finally:
    if f:
        f.close()
"""


#cookie_txt_write = open(cookie_txt,'w') #Write cookie file

#Check cookie txt status
cookie_filesize = os.path.getsize(cookie_txt)
if cookie_filesize == 0:
    print("No cookie detected, please re-login")
else:
    open_cookie_temp = open(cookie_txt,'r')
    cookie_temp = open_cookie_temp.read()
    """
    cookie_temp = cookie_temp.replace('\'','\"')
    cookie_temp = cookie_temp.replace(',',',\n')
    cookie_temp = cookie_temp.replace('{','{\n')
    cookie_temp = cookie_temp.replace('}','\n}')
    cookie_temp = cookie_temp.replace('True','true')
    #print(cookie_temp)
    """
    cookie_temp = json.loads(cookie_temp)
    #Formatting JSON 
    #fuck you double quotta

driver = webdriver.Edge("./edgedriver_win64/msedgedriver.exe")

driver.get("https://masters.caravan-stories.com.tw/game_start/launch") #go launch

if cookie_temp != type(None)():
    driver.delete_all_cookies()
    driver.add_cookie(cookie_temp)
    driver.execute_script("window.stop();")
    driver.get("https://masters.caravan-stories.com.tw/game_start/launch")
    #time.sleep(1)

cookie = type(None)()
while True:
    if driver.current_url == login_suc:
        cookie = driver.get_cookie("_caravan_stories_session")
        print("%s -> %s" % (cookie['name'], cookie['value']))
        #print(cookie,file=open(cookie_txt,'w'))
        f1 = open(cookie_txt, 'w')
        f1.write(json.dumps(cookie))
        #Save Current Cookie

        print(driver.find_element_by_xpath("/html/body").text)
        start_url = driver.find_element_by_xpath("/html/body").text
        start_url_arr = json.loads(start_url)
        print(start_url_arr['url'])
        start_url = start_url_arr['url']
        driver.get(start_url)

    if cookie != type(None)():
        break

caravan_proc = 'Caravan.exe'

def checkIfProcessRunning(processName):
    #Check if there is any running process that contains the given name processName.
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
while True:
    if checkIfProcessRunning('Caravan.exe'):
        driver.close()
        break

print('program finished')
sys.exit()