from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 
import re, time, pandas as pd
'''

Takes a URL as the target.  Filters out Ads, and allows to get events form only one specific month.

'''
#Initiate driver, set URL
driver = webdriver.Chrome(executable_path=r'H:\Learning\Python\chromedriver_win32\chromedriver.exe') 
url = 'https://www.joinnus.com/search?searchKey={"text":"","maps":false,"filters":{"price":{"min":"","max":""},"categories":["concerts"],"dates":{"key":"all","dateStart":"2020-12-11T06:00:37","dateEnd":"2020-12-11T23:59:00"},"location":{"z":12,"center":{"lat":-12.149422,"lng":-77.020820}}},"page":1,"country":"PE"}'
driver.implicitly_wait(10)
driver.get(url)

#click More Events to load more until it cant be clicked.  Page sometimes takes a bit, increase sleep time if needed.
exs = 1
btn = None
sleepFor = 5

while exs == 1:
    try:
        #xpath for 'load more' btn
        btn = driver.find_element_by_xpath('//*[@id="__next"]/div/div/main/div/div/section[1]/div/div[2]/button')
    except NoSuchElementException:
        btn = None
    except ElementClickInterceptedException:
        btn = None
        continue
    if(btn):
        btn.click()
        time.sleep(sleepFor)
    else:
        #no more btn!
        exs = 0
    btn = None



#search for events and create df to be used for storing
events = driver.find_elements(By.XPATH, "//div[@class='col-12 col-md-6 col-lg-4 col-xl-3 mb-4']")
df = pd.DataFrame(columns = ('Title', 'Price', 'Date' ,'Time', 'Link'))
count = 0
#month to target, change only first part.
targetMonth = 'Dec' + ' - '
for i in events:
    #Filter out duds
    if 'ADVERTISING' in i.text:
        continue
    elif ' Dec - ' not in i.text:
        continue
    else:
        #print('+++++++++++++++++')
        #print(i.text)
        link = (i.find_element(By.CLASS_NAME,'card-event')).get_attribute('href')  #str
        title = (i.find_element(By.CLASS_NAME, 'card-event__title')).text  #webelement
        calendar = (i.find_element(By.CLASS_NAME, 'card-event__calendar')).text  #webelement
        footer = (i.find_element(By.CLASS_NAME, 'card-event__footer'))
        price = footer.text.split('\n')[0]
        #handle prices
        price = re.sub('[^\d\.]', '', price)
        if price == '':
            price = 'Free'
        # print("Title: " + title.text)
        # print("Link: " + link)
        # print("Date/Time: " + calendar.text)
        # print("Price: " + price)
        calendar = calendar.split(' ')
        date = calendar[1] + ' ' + calendar[2]
        time = calendar[4] + ' ' + calendar[5]
        df.loc[count] = [title, 'S/ '+ price, date, time, link]
        count += 1
    
#close and store
driver.quit()
df.to_csv('data.csv')
