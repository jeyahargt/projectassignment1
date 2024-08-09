#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    driver.get('https://www.redbus.in')
    
    # Wait until the element is present
    wait = WebDriverWait(driver, 10)
    view_all = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="https://www.redbus.in/online-booking/rtc-directory"]')))
    
    # Perform actions on the element
    view_all.click()
    
finally:
    driver.quit()


# In[2]:


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import mysql.connector

driver = webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/rtc-directory")
driver.maximize_window()
rajasthan = driver.find_element(By.CSS_SELECTOR, 'a[href="/online-booking/rsrtc"]')
driver.execute_script("arguments[0].click();", rajasthan) 
#driver.find_element(By.LINK_TEXT, 'RSRTC').click()
# rajasthan.click();
time.sleep(3)
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")

rajasthan_route_names = []
rajasthan_route_links = []

def scrape_data():
    route_names = driver.find_elements(By.CLASS_NAME, "route")
    for route_name in route_names:
        rajasthan_route_names.append(route_name.text)

    route_links = driver.find_elements(By.CLASS_NAME, "route")
    hrefs = [route_link.get_attribute('href') for route_link in route_links]
    for href in hrefs:
        rajasthan_route_links.append(href)

page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")
for i in range(len(page_tabs)):
    if i > 0:
        page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")[i]
        driver.execute_script("arguments[0].click();", page_tabs)        
        time.sleep(4)
    scrape_data()

# print(rajasthan_route_names)
# print(rajasthan_route_links)

df = pd.DataFrame(columns=['route_name', 'route_link', 'busname', 'bustype', 'departing_time', 
                           'duration', 'reaching_time', 'star_rating', 'price', 'seats_available'])

count = 0
for link in rajasthan_route_links:
    driver.get(link)
    driver.maximize_window()

    try:
        wait = WebDriverWait(driver, 3)
        wait_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
        driver.execute_script("arguments[0].click();", wait_button)
        # government_buses = driver.find_element(By.CLASS_NAME, "button")
        #driver.execute_script("arguments[0].click();", government_buses)
        
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass

    # government_buses = driver.find_element(By.CLASS_NAME, "button")
    # driver.execute_script("arguments[0].click();", government_buses)
    # time.sleep(1)

    for t in range(33):     #scrolling 12 times so that whole website loads
        driver.execute_script("window.scrollBy(0, 650);")
        time.sleep(0.25)

    
    route_name = []
    route_link = []
    bus_name = []
    bus_type = []
    departing = []
    duration = []
    reaching = []
    rating = []
    price = []
    availability = []
    dict = {}
    df1 = pd.DataFrame()

    names = driver.find_elements(By.CLASS_NAME,"travels")
    types = driver.find_elements(By.CLASS_NAME,"bus-type")
    depart_timings = driver.find_elements(By.CLASS_NAME,"dp-time")
    travel_durations = driver.find_elements(By.CLASS_NAME,"dur")
    arrivals = driver.find_elements(By.CLASS_NAME,"bp-time")
    star_ratings = driver.find_elements(By.CLASS_NAME,"column-six")
    fares = driver.find_elements(By.CLASS_NAME,"fare")
    seats_available = driver.find_elements(By.CLASS_NAME,"seat-left")

    for name in names:
        bus_name.append(name.text)

    for type in types:
        bus_type.append(type.text)

    for depart_timing in depart_timings:
        departing.append(depart_timing.text)

    for travel_duration in travel_durations:
        duration.append(travel_duration.text)

    for arrival in arrivals:
        reaching.append(arrival.text)

    for star_rating in star_ratings:
        rating.append(star_rating.text[:3])

    for fare in fares:
        if (fare.text).isdigit():
            price.append(fare.text)
        else:
            price.append((fare.text).replace('INR','').strip())

    for seat_available in seats_available:
        availability.append(seat_available.text[:2].strip())
    
    for i in range(len(bus_name)):
        route_name.append(rajasthan_route_names[count])
        route_link.append(link)

    count += 1


    # print(route_name)
    # print(route_link)
    # print(bus_name)
    # print(bus_type)
    # print(departing)
    # print(duration)
    # print(reaching)
    # print(rating)
    # print(price)
    # print(availability)

    for i in range(len(rating)):
        if rating[i] == 'New' or rating[i] == ' ':
            rating[i] = '0.0'

    dict = {'route_name':route_name, 'route_link':route_link, 'busname':bus_name, 'bustype':bus_type, 'departing_time':departing,
            'duration':duration, 'reaching_time':reaching, 'star_rating':rating, 'price':price, 'seats_available':availability}
    
    df1 = pd.DataFrame(dict)
    df = pd.concat([df, df1], ignore_index=True)
    
print(df)


# In[3]:


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import mysql.connector

driver = webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/rtc-directory")
driver.maximize_window()
kerala = driver.find_element(By.CSS_SELECTOR, 'a[href="/online-booking/ksrtc-kerala"]')
kerala.click();
time.sleep(3)
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")

kerala_route_names = []
kerala_route_links = []

def scrape_data():
    route_names = driver.find_elements(By.CLASS_NAME, "route")
    for route_name in route_names:
        kerala_route_names.append(route_name.text)

    route_links = driver.find_elements(By.CLASS_NAME, "route")
    hrefs = [route_link.get_attribute('href') for route_link in route_links]
    for href in hrefs:
        kerala_route_links.append(href)

page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")
for i in range(len(page_tabs)):
    if i > 0:
        page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")[i]
        driver.execute_script("arguments[0].click();", page_tabs)        
        time.sleep(4)
    scrape_data()

# print(kerala_route_names)
# print(kerala_route_links)


count = 0
for link in kerala_route_links:
    driver.get(link)
    driver.maximize_window()

    try:
        wait = WebDriverWait(driver, 3)
        wait_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
        driver.execute_script("arguments[0].click();", wait_button)
        # government_buses = driver.find_element(By.CLASS_NAME, "button")
        #driver.execute_script("arguments[0].click();", government_buses)
        
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass    
    
    for t in range(22):     #scrolling 20 times so that whole website loads
        driver.execute_script("window.scrollBy(0, 650);")
        time.sleep(0.3)

    
    route_name = []
    route_link = []
    bus_name = []
    bus_type = []
    departing = []
    duration = []
    reaching = []
    rating = []
    price = []
    availability = []
    dict = {}
    df1 = pd.DataFrame()

    names = driver.find_elements(By.CLASS_NAME,"travels")
    types = driver.find_elements(By.CLASS_NAME,"bus-type")
    depart_timings = driver.find_elements(By.CLASS_NAME,"dp-time")
    travel_durations = driver.find_elements(By.CLASS_NAME,"dur")
    arrivals = driver.find_elements(By.CLASS_NAME,"bp-time")
    star_ratings = driver.find_elements(By.CLASS_NAME,"column-six")
    fares = driver.find_elements(By.CLASS_NAME,"fare")
    seats_available = driver.find_elements(By.CLASS_NAME,"seat-left")

    for name in names:
        bus_name.append(name.text)

    for type in types:
        bus_type.append(type.text)

    for depart_timing in depart_timings:
        departing.append(depart_timing.text)

    for travel_duration in travel_durations:
        duration.append(travel_duration.text)

    for arrival in arrivals:
        reaching.append(arrival.text)

    for star_rating in star_ratings:
        rating.append(star_rating.text[:3])

    for fare in fares:
        if (fare.text).isdigit():
            price.append(fare.text)
        else:
            price.append((fare.text).replace('INR','').strip())

    for seat_available in seats_available:
        availability.append(seat_available.text[:2].strip())
    
    for i in range(len(bus_name)):
        route_name.append(kerala_route_names[count])
        route_link.append(link)

    count += 1


    # print(route_name)
    # print(route_link)
    # print(bus_name)
    # print(bus_type)
    # print(departing)
    # print(duration)
    # print(reaching)
    # print(rating)
    # print(price)
    # print(availability)

    for i in range(len(rating)):
        if rating[i] == 'New' or rating[i] == ' ':
            rating[i] = '0.0'


    dict = {'route_name':route_name, 'route_link':route_link, 'busname':bus_name, 'bustype':bus_type, 'departing_time':departing,
            'duration':duration, 'reaching_time':reaching, 'star_rating':rating, 'price':price, 'seats_available':availability}
    
    df1 = pd.DataFrame(dict)
    #df.append(dict, ignore_index=True)
    df = pd.concat([df, df1], ignore_index=True)
    
print(df)


# In[4]:


# experimental code (Himachal HRTC)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import mysql.connector

driver = webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/rtc-directory")
driver.maximize_window()
himachal = driver.find_element(By.CSS_SELECTOR, 'a[href="/online-booking/hrtc"]')
driver.execute_script("arguments[0].click();", himachal) 
time.sleep(2)
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")

himachal_route_names = []
himachal_route_links = []

def scrape_data():
    route_names = driver.find_elements(By.CLASS_NAME, "route")
    for route_name in route_names:
        himachal_route_names.append(route_name.text)

    route_links = driver.find_elements(By.CLASS_NAME, "route")
    hrefs = [route_link.get_attribute('href') for route_link in route_links]
    for href in hrefs:
        himachal_route_links.append(href)

page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")
for i in range(len(page_tabs)):
    if i > 0:
        page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")[i]
        driver.execute_script("arguments[0].click();", page_tabs)        
        time.sleep(1)
    scrape_data()

# print(himachal_route_names)
# print(himachal_route_links)


count = 0
for link in himachal_route_links:
    driver.get(link)
    driver.maximize_window()

    try:
        wait = WebDriverWait(driver, 3)
        wait_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
        driver.execute_script("arguments[0].click();", wait_button)
        # government_buses = driver.find_element(By.CLASS_NAME, "button")
        #driver.execute_script("arguments[0].click();", government_buses)
        
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass

    # government_buses = driver.find_element(By.CLASS_NAME, "p-left-10")
    # driver.execute_script("arguments[0].click();", government_buses)
    # time.sleep(1)

    for t in range(33):     #scrolling 12 times so that whole website loads
        driver.execute_script("window.scrollBy(0, 650);")
        time.sleep(0.25)

    
    route_name = []
    route_link = []
    bus_name = []
    bus_type = []
    departing = []
    duration = []
    reaching = []
    rating = []
    price = []
    availability = []
    dict = {}
    df1 = pd.DataFrame()

    names = driver.find_elements(By.CLASS_NAME,"travels")
    types = driver.find_elements(By.CLASS_NAME,"bus-type")
    depart_timings = driver.find_elements(By.CLASS_NAME,"dp-time")
    travel_durations = driver.find_elements(By.CLASS_NAME,"dur")
    arrivals = driver.find_elements(By.CLASS_NAME,"bp-time")
    star_ratings = driver.find_elements(By.CLASS_NAME,"column-six")
    fares = driver.find_elements(By.CLASS_NAME,"fare")
    seats_available = driver.find_elements(By.CLASS_NAME,"seat-left")

    for name in names:
        bus_name.append(name.text)

    for type in types:
        bus_type.append(type.text)

    for depart_timing in depart_timings:
        departing.append(depart_timing.text)

    for travel_duration in travel_durations:
        duration.append(travel_duration.text)

    for arrival in arrivals:
        reaching.append(arrival.text)

    for star_rating in star_ratings:
        rating.append(star_rating.text[:3])

    for fare in fares:
        if (fare.text).isdigit():
            price.append(fare.text)
        else:
            price.append((fare.text).replace('INR','').strip())

    for seat_available in seats_available:
        availability.append(seat_available.text[:2].strip())
    
    for i in range(len(bus_name)):
        route_name.append(himachal_route_names[count])
        route_link.append(link)

    count += 1

    # print(route_name)
    # print(route_link)
    # print(bus_name)
    # print(bus_type)
    # print(departing)
    # print(duration)
    # print(reaching)
    # print(rating)
    # print(price)
    # print(availability)

    for i in range(len(rating)):
        if rating[i] == 'New' or rating[i] == ' ':
            rating[i] = '0.0'

    dict = {'route_name':route_name, 'route_link':route_link, 'busname':bus_name, 'bustype':bus_type, 'departing_time':departing,
            'duration':duration, 'reaching_time':reaching, 'star_rating':rating, 'price':price, 'seats_available':availability}
    
    df1 = pd.DataFrame(dict)
    df = pd.concat([df, df1], ignore_index=True)
    
print(df)


# In[5]:


# experimental code (punjab pepsu)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import mysql.connector

driver = webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/rtc-directory")
driver.maximize_window()
punjab = driver.find_element(By.CSS_SELECTOR, 'a[href="/online-booking/pepsu-punjab"]')
driver.execute_script("arguments[0].click();", punjab) 
time.sleep(2)
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")

punjab_route_names = []
punjab_route_links = []

def scrape_data():
    route_names = driver.find_elements(By.CLASS_NAME, "route")
    for route_name in route_names:
        punjab_route_names.append(route_name.text)

    route_links = driver.find_elements(By.CLASS_NAME, "route")
    hrefs = [route_link.get_attribute('href') for route_link in route_links]
    for href in hrefs:
        punjab_route_links.append(href)

page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")
for i in range(len(page_tabs)):
    if i > 0:
        page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")[i]
        driver.execute_script("arguments[0].click();", page_tabs)        
        time.sleep(1)
    scrape_data()

# print(punjab_route_names)
# print(punjab_route_links)


count = 0
for link in punjab_route_links:
    driver.get(link)
    driver.maximize_window()

    try:
        wait = WebDriverWait(driver, 3)
        wait_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
        driver.execute_script("arguments[0].click();", wait_button)
        # government_buses = driver.find_element(By.CLASS_NAME, "button")
        #driver.execute_script("arguments[0].click();", government_buses)
        
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass

    # government_buses = driver.find_element(By.CLASS_NAME, "p-left-10")
    # driver.execute_script("arguments[0].click();", government_buses)
    # time.sleep(1)

    for t in range(32):     #scrolling 12 times so that whole website loads
        driver.execute_script("window.scrollBy(0, 650);")
        time.sleep(0.25)

    
    route_name = []
    route_link = []
    bus_name = []
    bus_type = []
    departing = []
    duration = []
    reaching = []
    rating = []
    price = []
    availability = []
    dict = {}
    df1 = pd.DataFrame()

    names = driver.find_elements(By.CLASS_NAME,"travels")
    types = driver.find_elements(By.CLASS_NAME,"bus-type")
    depart_timings = driver.find_elements(By.CLASS_NAME,"dp-time")
    travel_durations = driver.find_elements(By.CLASS_NAME,"dur")
    arrivals = driver.find_elements(By.CLASS_NAME,"bp-time")
    star_ratings = driver.find_elements(By.CLASS_NAME,"column-six")
    fares = driver.find_elements(By.CLASS_NAME,"fare")
    seats_available = driver.find_elements(By.CLASS_NAME,"seat-left")

    for name in names:
        bus_name.append(name.text)

    for type in types:
        bus_type.append(type.text)

    for depart_timing in depart_timings:
        departing.append(depart_timing.text)

    for travel_duration in travel_durations:
        duration.append(travel_duration.text)

    for arrival in arrivals:
        reaching.append(arrival.text)

    for star_rating in star_ratings:
        rating.append(star_rating.text[:3])

    for fare in fares:
        if (fare.text).isdigit():
            price.append(fare.text)
        else:
            price.append((fare.text).replace('INR','').strip())

    for seat_available in seats_available:
        availability.append(seat_available.text[:2].strip())
    
    for i in range(len(bus_name)):
        route_name.append(punjab_route_names[count])
        route_link.append(link)

    count += 1


    # print(route_name)
    # print(route_link)
    # print(bus_name)
    # print(bus_type)
    # print(departing)
    # print(duration)
    # print(reaching)
    # print(rating)
    # print(price)
    # print(availability)

    for i in range(len(rating)):
        if rating[i] == 'New' or rating[i] == ' ':
            rating[i] = '0.0'

    dict = {'route_name':route_name, 'route_link':route_link, 'busname':bus_name, 'bustype':bus_type, 'departing_time':departing,
            'duration':duration, 'reaching_time':reaching, 'star_rating':rating, 'price':price, 'seats_available':availability}
    
    df1 = pd.DataFrame(dict)
    df = pd.concat([df, df1], ignore_index=True)
    
print(df)


# In[6]:


# experimental code (BIHAR bsrtc)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import mysql.connector

driver = webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/rtc-directory")
driver.maximize_window()
bihar = driver.find_element(By.CSS_SELECTOR, 'a[href="/online-booking/bihar-state-road-transport-corporation-bsrtc"]')
driver.execute_script("arguments[0].click();", bihar) 
time.sleep(2)
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")

bihar_route_names = []
bihar_route_links = []

def scrape_data():
    route_names = driver.find_elements(By.CLASS_NAME, "route")
    for route_name in route_names:
        bihar_route_names.append(route_name.text)

    route_links = driver.find_elements(By.CLASS_NAME, "route")
    hrefs = [route_link.get_attribute('href') for route_link in route_links]
    for href in hrefs:
        bihar_route_links.append(href)

page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")
for i in range(len(page_tabs)):
    if i > 0:
        page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")[i]
        driver.execute_script("arguments[0].click();", page_tabs)        
        time.sleep(1)
    scrape_data()

# print(bihar_route_names)
# print(bihar_route_links)


count = 0
for link in bihar_route_links:
    driver.get(link)
    driver.maximize_window()

    try:
        wait = WebDriverWait(driver, 3)
        wait_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
        driver.execute_script("arguments[0].click();", wait_button)
        # government_buses = driver.find_element(By.CLASS_NAME, "button")
        #driver.execute_script("arguments[0].click();", government_buses)
        
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass

    # government_buses = driver.find_element(By.CLASS_NAME, "p-left-10")
    # driver.execute_script("arguments[0].click();", government_buses)
    # time.sleep(1)

    for t in range(30):     #scrolling 12 times so that whole website loads
        driver.execute_script("window.scrollBy(0, 650);")
        time.sleep(0.25)

    
    route_name = []
    route_link = []
    bus_name = []
    bus_type = []
    departing = []
    duration = []
    reaching = []
    rating = []
    price = []
    availability = []
    dict = {}
    df1 = pd.DataFrame()

    names = driver.find_elements(By.CLASS_NAME,"travels")
    types = driver.find_elements(By.CLASS_NAME,"bus-type")
    depart_timings = driver.find_elements(By.CLASS_NAME,"dp-time")
    travel_durations = driver.find_elements(By.CLASS_NAME,"dur")
    arrivals = driver.find_elements(By.CLASS_NAME,"bp-time")
    star_ratings = driver.find_elements(By.CLASS_NAME,"column-six")
    fares = driver.find_elements(By.CLASS_NAME,"fare")
    seats_available = driver.find_elements(By.CLASS_NAME,"seat-left")

    for name in names:
        bus_name.append(name.text)

    for type in types:
        bus_type.append(type.text)

    for depart_timing in depart_timings:
        departing.append(depart_timing.text)

    for travel_duration in travel_durations:
        duration.append(travel_duration.text)

    for arrival in arrivals:
        reaching.append(arrival.text)

    for star_rating in star_ratings:
        rating.append(star_rating.text[:3])

    for fare in fares:
        if (fare.text).isdigit():
            price.append(fare.text)
        else:
            price.append((fare.text).replace('INR','').strip())

    for seat_available in seats_available:
        availability.append(seat_available.text[:2].strip())
    
    for i in range(len(bus_name)):
        route_name.append(bihar_route_names[count])
        route_link.append(link)

    count += 1


    # print(route_name)
    # print(route_link)
    # print(bus_name)
    # print(bus_type)
    # print(departing)
    # print(duration)
    # print(reaching)
    # print(rating)
    # print(price)
    # print(availability)

    for i in range(len(rating)):
        if rating[i] == 'New' or rating[i] == ' ':
            rating[i] = '0.0'

    dict = {'route_name':route_name, 'route_link':route_link, 'busname':bus_name, 'bustype':bus_type, 'departing_time':departing,
            'duration':duration, 'reaching_time':reaching, 'star_rating':rating, 'price':price, 'seats_available':availability}
    
    df1 = pd.DataFrame(dict)
    df = pd.concat([df, df1], ignore_index=True)
    
print(df)


# In[7]:


# experimental code (south bengal sbstc)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import mysql.connector

driver = webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/rtc-directory")
driver.maximize_window()
s_bengal = driver.find_element(By.CSS_SELECTOR, 'a[href="/online-booking/south-bengal-state-transport-corporation-sbstc"]')
driver.execute_script("arguments[0].click();", s_bengal) 
time.sleep(2)
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")

s_bengal_route_names = []
s_bengal_route_links = []

def scrape_data():
    route_names = driver.find_elements(By.CLASS_NAME, "route")
    for route_name in route_names:
        s_bengal_route_names.append(route_name.text)

    route_links = driver.find_elements(By.CLASS_NAME, "route")
    hrefs = [route_link.get_attribute('href') for route_link in route_links]
    for href in hrefs:
        s_bengal_route_links.append(href)

page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")
for i in range(len(page_tabs)):
    if i > 0:
        page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")[i]
        driver.execute_script("arguments[0].click();", page_tabs)        
        time.sleep(1)
    scrape_data()

# print(s_bengal_route_names)
# print(s_bengal_route_links)


count = 0
for link in s_bengal_route_links:
    driver.get(link)
    driver.maximize_window()

    try:
        wait = WebDriverWait(driver, 3)
        wait_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
        driver.execute_script("arguments[0].click();", wait_button)
        # government_buses = driver.find_element(By.CLASS_NAME, "button")
        #driver.execute_script("arguments[0].click();", government_buses)
        
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass

    # government_buses = driver.find_element(By.CLASS_NAME, "p-left-10")
    # driver.execute_script("arguments[0].click();", government_buses)
    # time.sleep(1)

    for t in range(25):     #scrolling 12 times so that whole website loads
        driver.execute_script("window.scrollBy(0, 650);")
        time.sleep(0.25)

    
    route_name = []
    route_link = []
    bus_name = []
    bus_type = []
    departing = []
    duration = []
    reaching = []
    rating = []
    price = []
    availability = []
    dict ={}
    df1 = pd.DataFrame()

    names = driver.find_elements(By.CLASS_NAME,"travels")
    types = driver.find_elements(By.CLASS_NAME,"bus-type")
    depart_timings = driver.find_elements(By.CLASS_NAME,"dp-time")
    travel_durations = driver.find_elements(By.CLASS_NAME,"dur")
    arrivals = driver.find_elements(By.CLASS_NAME,"bp-time")
    star_ratings = driver.find_elements(By.CLASS_NAME,"column-six")
    fares = driver.find_elements(By.CLASS_NAME,"fare")
    seats_available = driver.find_elements(By.CLASS_NAME,"seat-left")

    for name in names:
        bus_name.append(name.text)

    for type in types:
        bus_type.append(type.text)

    for depart_timing in depart_timings:
        departing.append(depart_timing.text)

    for travel_duration in travel_durations:
        duration.append(travel_duration.text)

    for arrival in arrivals:
        reaching.append(arrival.text)

    for star_rating in star_ratings:
        rating.append(star_rating.text[:3])

    for fare in fares:
        if (fare.text).isdigit():
            price.append(fare.text)
        else:
            price.append((fare.text).replace('INR','').strip())

    for seat_available in seats_available:
        availability.append(seat_available.text[:2].strip())
    
    for i in range(len(bus_name)):
        route_name.append(s_bengal_route_names[count])
        route_link.append(link)

    count += 1


    # print(route_name)
    # print(route_link)
    # print(bus_name)
    # print(bus_type)
    # print(departing)
    # print(duration)
    # print(reaching)
    # print(rating)
    # print(price)
    # print(availability)

    for i in range(len(rating)):
        if rating[i] == 'New' or rating[i] == ' ':
            rating[i] = '0.0'

    dict = {'route_name':route_name, 'route_link':route_link, 'busname':bus_name, 'bustype':bus_type, 'departing_time':departing,
            'duration':duration, 'reaching_time':reaching, 'star_rating':rating, 'price':price, 'seats_available':availability}
    
    df1 = pd.DataFrame(dict)
    df = pd.concat([df, df1], ignore_index=True)
    
print(df)


# In[8]:


# experimental code (West bengal)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import mysql.connector

driver = webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/rtc-directory")
driver.maximize_window()
w_bengal = driver.find_element(By.CSS_SELECTOR, 'a[href="/online-booking/west-bengal-transport-corporation"]')
driver.execute_script("arguments[0].click();", w_bengal) 
time.sleep(2)
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")

w_bengal_route_names = []
w_bengal_route_links = []

def scrape_data():
    route_names = driver.find_elements(By.CLASS_NAME, "route")
    for route_name in route_names:
        w_bengal_route_names.append(route_name.text)

    route_links = driver.find_elements(By.CLASS_NAME, "route")
    hrefs = [route_link.get_attribute('href') for route_link in route_links]
    for href in hrefs:
        w_bengal_route_links.append(href)

# page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")
# for i in range(len(page_tabs)):
#     if i > 0:
#         page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")[i]
#         driver.execute_script("arguments[0].click();", page_tabs)        
#         time.sleep(1)
#     scrape_data()

scrape_data()

# print(w_bengal_route_names)
# print(w_bengal_route_links)


count = 0
for link in w_bengal_route_links:
    driver.get(link)
    driver.maximize_window()

    # government_buses = driver.find_element(By.CLASS_NAME, "p-left-10")
    # driver.execute_script("arguments[0].click();", government_buses)
    # time.sleep(1)

    for t in range(20):     #scrolling 12 times so that whole website loads
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(0.3)

    
    route_name = []
    route_link = []
    bus_name = []
    bus_type = []
    departing = []
    duration = []
    reaching = []
    rating = []
    price = []
    availability = []
    dict = {}
    df1 = pd.DataFrame()

    names = driver.find_elements(By.CLASS_NAME,"travels")
    types = driver.find_elements(By.CLASS_NAME,"bus-type")
    depart_timings = driver.find_elements(By.CLASS_NAME,"dp-time")
    travel_durations = driver.find_elements(By.CLASS_NAME,"dur")
    arrivals = driver.find_elements(By.CLASS_NAME,"bp-time")
    star_ratings = driver.find_elements(By.CLASS_NAME,"column-six")
    fares = driver.find_elements(By.CLASS_NAME,"fare")
    seats_available = driver.find_elements(By.CLASS_NAME,"seat-left")

    for name in names:
        bus_name.append(name.text)

    for type in types:
        bus_type.append(type.text)

    for depart_timing in depart_timings:
        departing.append(depart_timing.text)

    for travel_duration in travel_durations:
        duration.append(travel_duration.text)

    for arrival in arrivals:
        reaching.append(arrival.text)

    for star_rating in star_ratings:
        rating.append(star_rating.text[:3])

    for fare in fares:
        if (fare.text).isdigit():
            price.append(fare.text)
        else:
            price.append((fare.text).replace('INR','').strip())

    for seat_available in seats_available:
        availability.append(seat_available.text[:2].strip())
    
    for i in range(len(bus_name)):
        route_name.append(w_bengal_route_names[count])
        route_link.append(link)

    count += 1

    # print(route_name)
    # print(route_link)
    # print(bus_name)
    # print(bus_type)
    # print(departing)
    # print(duration)
    # print(reaching)
    # print(rating)
    # print(price)
    # print(availability)

    for i in range(len(rating)):
        if rating[i] == 'New' or rating[i] == ' ':
            rating[i] = '0.0'

    dict = {'route_name':route_name, 'route_link':route_link, 'busname':bus_name, 'bustype':bus_type, 'departing_time':departing,
            'duration':duration, 'reaching_time':reaching, 'star_rating':rating, 'price':price, 'seats_available':availability}
    
    df1 = pd.DataFrame(dict)
    df = pd.concat([df, df1], ignore_index=True)


# In[9]:


print(df)


# In[10]:


# experimental code (Chandigarh CTU)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import mysql.connector

driver = webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/rtc-directory")
driver.maximize_window()
chandigarh = driver.find_element(By.CSS_SELECTOR, 'a[href="/online-booking/chandigarh-transport-undertaking-ctu"]')
driver.execute_script("arguments[0].click();", chandigarh) 
time.sleep(2)
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")

chandigarh_route_names = []
chandigarh_route_links = []

def scrape_data():
    route_names = driver.find_elements(By.CLASS_NAME, "route")
    for route_name in route_names:
        chandigarh_route_names.append(route_name.text)

    route_links = driver.find_elements(By.CLASS_NAME, "route")
    hrefs = [route_link.get_attribute('href') for route_link in route_links]
    for href in hrefs:
        chandigarh_route_links.append(href)

page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")
for i in range(len(page_tabs)):
    if i > 0:
        page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")[i]
        driver.execute_script("arguments[0].click();", page_tabs)        
        time.sleep(1)
    scrape_data()


# print(chandigarh_route_names)
# print(chandigarh_route_links)


count = 0
for link in chandigarh_route_links:
    driver.get(link)
    driver.maximize_window()

    try:
        wait = WebDriverWait(driver, 3)
        wait_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
        driver.execute_script("arguments[0].click();", wait_button)
        # government_buses = driver.find_element(By.CLASS_NAME, "button")
        #driver.execute_script("arguments[0].click();", government_buses)
        
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass

    # government_buses = driver.find_element(By.CLASS_NAME, "p-left-10")
    # driver.execute_script("arguments[0].click();", government_buses)
    # time.sleep(1)

    for t in range(20):     #scrolling 12 times so that whole website loads
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(0.3)

    
    route_name = []
    route_link = []
    bus_name = []
    bus_type = []
    departing = []
    duration = []
    reaching = []
    rating = []
    price = []
    availability = []
    dict = {}
    df1 = pd.DataFrame()

    names = driver.find_elements(By.CLASS_NAME,"travels")
    types = driver.find_elements(By.CLASS_NAME,"bus-type")
    depart_timings = driver.find_elements(By.CLASS_NAME,"dp-time")
    travel_durations = driver.find_elements(By.CLASS_NAME,"dur")
    arrivals = driver.find_elements(By.CLASS_NAME,"bp-time")
    star_ratings = driver.find_elements(By.CLASS_NAME,"column-six")
    fares = driver.find_elements(By.CLASS_NAME,"fare")
    seats_available = driver.find_elements(By.CLASS_NAME,"seat-left")

    for name in names:
        bus_name.append(name.text)

    for type in types:
        bus_type.append(type.text)

    for depart_timing in depart_timings:
        departing.append(depart_timing.text)

    for travel_duration in travel_durations:
        duration.append(travel_duration.text)

    for arrival in arrivals:
        reaching.append(arrival.text)

    for star_rating in star_ratings:
        rating.append(star_rating.text[:3])

    for fare in fares:
        if (fare.text).isdigit():
            price.append(fare.text)
        else:
            price.append((fare.text).replace('INR','').strip())

    for seat_available in seats_available:
        availability.append(seat_available.text[:2].strip())
    
    for i in range(len(bus_name)):
        route_name.append(chandigarh_route_names[count])
        route_link.append(link)

    count += 1


    # print(route_name)
    # print(route_link)
    # print(bus_name)
    # print(bus_type)
    # print(departing)
    # print(duration)
    # print(reaching)
    # print(rating)
    # print(price)
    # print(availability)

    for i in range(len(rating)):
        if rating[i] == 'New' or rating[i] == ' ':
            rating[i] = '0.0'

    dict = {'route_name':route_name, 'route_link':route_link, 'busname':bus_name, 'bustype':bus_type, 'departing_time':departing,
            'duration':duration, 'reaching_time':reaching, 'star_rating':rating, 'price':price, 'seats_available':availability}
    
    df1 = pd.DataFrame(dict)
    df = pd.concat([df, df1], ignore_index=True)
    
print(df)


# In[11]:


# experimental code (Assam ASTC)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import mysql.connector

driver = webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/rtc-directory")
driver.maximize_window()
assam = driver.find_element(By.CSS_SELECTOR, 'a[href="/online-booking/astc"]')
driver.execute_script("arguments[0].click();", assam) 
time.sleep(2)
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")

assam_route_names = []
assam_route_links = []

def scrape_data():
    route_names = driver.find_elements(By.CLASS_NAME, "route")
    for route_name in route_names:
        assam_route_names.append(route_name.text)

    route_links = driver.find_elements(By.CLASS_NAME, "route")
    hrefs = [route_link.get_attribute('href') for route_link in route_links]
    for href in hrefs:
        assam_route_links.append(href)

page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")
for i in range(len(page_tabs)):
    if i > 0:
        page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")[i]
        driver.execute_script("arguments[0].click();", page_tabs)        
        time.sleep(1)
    scrape_data()


# print(assam_route_names)
# print(assam_route_links)


count = 0
for link in assam_route_links:
    driver.get(link)
    driver.maximize_window()

    try:
        wait = WebDriverWait(driver, 3)
        wait_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
        driver.execute_script("arguments[0].click();", wait_button)
        # government_buses = driver.find_element(By.CLASS_NAME, "button")
        #driver.execute_script("arguments[0].click();", government_buses)
        
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass

    # government_buses = driver.find_element(By.CLASS_NAME, "p-left-10")
    # driver.execute_script("arguments[0].click();", government_buses)
    # time.sleep(1)

    for t in range(20):     #scrolling 12 times so that whole website loads
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(0.3)

    
    route_name = []
    route_link = []
    bus_name = []
    bus_type = []
    departing = []
    duration = []
    reaching = []
    rating = []
    price = []
    availability = []
    dict = {}
    df1 = pd.DataFrame()

    names = driver.find_elements(By.CLASS_NAME,"travels")
    types = driver.find_elements(By.CLASS_NAME,"bus-type")
    depart_timings = driver.find_elements(By.CLASS_NAME,"dp-time")
    travel_durations = driver.find_elements(By.CLASS_NAME,"dur")
    arrivals = driver.find_elements(By.CLASS_NAME,"bp-time")
    star_ratings = driver.find_elements(By.CLASS_NAME,"column-six")
    fares = driver.find_elements(By.CLASS_NAME,"fare")
    seats_available = driver.find_elements(By.CLASS_NAME,"seat-left")

    for name in names:
        bus_name.append(name.text)

    for type in types:
        bus_type.append(type.text)

    for depart_timing in depart_timings:
        departing.append(depart_timing.text)

    for travel_duration in travel_durations:
        duration.append(travel_duration.text)

    for arrival in arrivals:
        reaching.append(arrival.text)

    for star_rating in star_ratings:
        rating.append(star_rating.text[:3])

    for fare in fares:
        if (fare.text).isdigit():
            price.append(fare.text)
        else:
            price.append((fare.text).replace('INR','').strip())

    for seat_available in seats_available:
        availability.append(seat_available.text[:2].strip())
    
    for i in range(len(bus_name)):
        route_name.append(assam_route_names[count])
        route_link.append(link)

    count += 1


    # print(route_name)
    # print(route_link)
    # print(bus_name)
    # print(bus_type)
    # print(departing)
    # print(duration)
    # print(reaching)
    # print(rating)
    # print(price)
    # print(availability)

    for i in range(len(rating)):
        if rating[i] == 'New' or rating[i] == ' ':
            rating[i] = '0.0'

    dict = {'route_name':route_name, 'route_link':route_link, 'busname':bus_name, 'bustype':bus_type, 'departing_time':departing,
            'duration':duration, 'reaching_time':reaching, 'star_rating':rating, 'price':price, 'seats_available':availability}
    
    df1 = pd.DataFrame(dict)
    df = pd.concat([df, df1], ignore_index=True)
    
print(df)


# In[13]:


from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/rtc-directory")
driver.maximize_window()

# Explicit wait for the element to be clickable
kadamba = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/online-booking/ktcl"]'))
)

# Scroll the element into view using JavaScript
driver.execute_script("arguments[0].scrollIntoView(true);", kadamba)
time.sleep(1)  # Wait a bit for the scroll to complete

# Click the element using ActionChains
ActionChains(driver).move_to_element(kadamba).click().perform()

time.sleep(5)
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")
driver.execute_script("window.scrollBy(0, window.innerHeight);")

kadamba_route_names = []
kadamba_route_links = []

def scrape_data():
    route_elements = driver.find_elements(By.CLASS_NAME, "route")
    for route_element in route_elements:
        kadamba_route_names.append(route_element.text)
        kadamba_route_links.append(route_element.get_attribute('href'))

# Using explicit wait for the page tabs
page_tabs = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "DC_117_pageTabs"))
)

for i in range(len(page_tabs)):
    if i > 0:
        page_tabs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "DC_117_pageTabs"))
        )
        ActionChains(driver).move_to_element(page_tabs[i]).click().perform()
        time.sleep(2)
    scrape_data()

count = 0

for link in kadamba_route_links:
    driver.get(link)
    driver.maximize_window()
    
    for t in range(22):
        driver.execute_script("window.scrollBy(0,500);")
        time.sleep(0.5)
        
    route_name = []
    route_link = []
    bus_name = []
    bus_type = []
    departing = []
    duration = []
    reaching = []
    rating = []
    price = []
    availability = []
    dict = {}
    df1 = pd.DataFrame()
    
    names = driver.find_elements(By.CLASS_NAME, "travels")
    types = driver.find_elements(By.CLASS_NAME, "bus-type")
    depart_timings = driver.find_elements(By.CLASS_NAME, "dp-time")
    travel_durations = driver.find_elements(By.CLASS_NAME, "dur")
    arrivals = driver.find_elements(By.CLASS_NAME, "bp-time")
    star_ratings = driver.find_elements(By.CLASS_NAME, "column-six")
    fares = driver.find_elements(By.CLASS_NAME, "fare")
    seats_available = driver.find_elements(By.CLASS_NAME, "seat-left")
    
    for name in names:
        bus_name.append(name.text)
    
    for bus_type_element in types:
        bus_type.append(bus_type_element.text)
        
    for depart_timing in depart_timings:
        departing.append(depart_timing.text)
        
    for travel_duration in travel_durations:
        duration.append(travel_duration.text)
        
    for arrival in arrivals:
        reaching.append(arrival.text)
        
    for star_rating in star_ratings:
        rating.append(star_rating.text[:3])
        
    for fare in fares:
        price.append(fare.text.replace('INR', '').strip() if not fare.text.isdigit() else fare.text)

    for seat_available in seats_available:
        availability.append(seat_available.text[:2].strip())
        
    for i in range(len(bus_name)):
        route_name.append(kadamba_route_names[count])
        route_link.append(link)
        
    count += 1
    
    for i in range(len(rating)):
        if rating[i] == 'New' or rating[i] == '':
            rating[i] = '0.0'
            
    dict = {
        'route_name': route_name,
        'route_link': route_link,
        'bus_name': bus_name,
        'bus_type': bus_type,
        'departing_time': departing,
        'duration': duration,
        'reaching_time': reaching,
        'star_rating': rating,
        'seat_available': availability
    }
    
    df1 = pd.DataFrame(dict)
    df = pd.concat([df, df1], ignore_index=True)
    
print(df)


# In[14]:


df.to_csv('final_dcsv.csv')


# In[15]:


df = pd.read_csv('final_dcsv.csv')
df['seat_available'] = df['seat_available'].fillna(0).astype('int64')
print(df.dtypes)


# In[16]:


df = df.fillna({
    'route_name': '',
    'route_link': '',
    'busname': '',
    'bustype': '',
    'departing_time': '00:00:00',
    'duration': '0h 0m',
    'reaching_time': '00:00:00',
    'star_rating': 0.0,
    'price': 0.0,
    'seats_available': 0
})


# In[18]:


def normalize_time(time_str):
    if len(time_str) == 5:  # If format is "%H:%M"
        return time_str + ":00"  # Add seconds
    return time_str
# Normalize the time strings
df['departing_time'] = df['departing_time'].apply(normalize_time)
df['reaching_time'] = df['reaching_time'].apply(normalize_time)
# Convert to datetime
df['departing_time'] = pd.to_datetime(df['departing_time'], format='%H:%M:%S').dt.time
df['reaching_time'] = pd.to_datetime(df['reaching_time'], format='%H:%M:%S').dt.time

# Ensure other columns are correctly formatted
df['star_rating'] = pd.to_numeric(df['star_rating'], errors='coerce').fillna(0.0).astype(float).round(1)
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0).astype(float)

print(df)


# In[19]:


con = mysql.connector.connect(
host = "localhost",
user = "root",
password = "Saran@123"
)
cursor = con.cursor()

query = "create database if not exists redbus_data_project"
cursor.execute(query)
query = "use redbus_data_project"
cursor.execute(query)

query = """create table if not exists All_bus_data(id INT AUTO_INCREMENT PRIMARY KEY, route_name varchar(70), route_link varchar(180), busname varchar(100), bustype varchar(50), departing_time TIME, duration varchar(20), reaching_time TIME, star_rating float(2,1), price DECIMAL(7, 2), seats_available INT  )"""
cursor.execute(query)

query = """insert into All_bus_data(route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
for i in range(len(df)):
    data = (df.loc[i, 'route_name'],df.loc[i, 'route_link'],df.loc[i, 'busname'],df.loc[i, 'bustype'],df.loc[i, 'departing_time'],df.loc[i, 'duration'],df.loc[i, 'reaching_time'],df.loc[i, 'star_rating'],df.loc[i, 'price'],df.loc[i, 'seats_available'])
    cursor.execute(query, data)
    con.commit()


# In[22]:


import streamlit as st
import pandas as pd
import mysql.connector

def fetch_data(query):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Saran@123",
        database="redbus_data_project"
    )
    cursor = con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    # get column names
    column_names = [column[0] for column in cursor.description]
    con.close()
    return rows, column_names

with st.sidebar:
    state_transport_corp = st.selectbox('Select the State Transport Corporation:',
    ['Rajasthan (RSRTC)','Kerala (KSRTC)','Himachal Pradesh (HRTC)','Punjab (PEPSU)','Bihar (BSRTC)',
     'South Bengal (SBSTC)','West Bengal','Chandigarh (CTU)','Assam (ASTC)', 'Kadamba (KTCL)'])
    
    if state_transport_corp == 'Rajasthan (RSRTC)':
            route = ['Jodhpur to Ajmer', 'Beawar (Rajasthan) to Jaipur (Rajasthan)', 'Udaipur to Jodhpur', 
                     'Jaipur (Rajasthan) to Jodhpur', 'Sikar to Jaipur (Rajasthan)', 'Kishangarh to Jaipur (Rajasthan)', 
                     'Aligarh (uttar pradesh) to Jaipur (Rajasthan)', 'Jodhpur to Beawar (Rajasthan)', 
                     'Kota (Rajasthan) to Jaipur (Rajasthan)', 'Jaipur (Rajasthan) to Aligarh (uttar pradesh)', 
                     'Jaipur (Rajasthan) to Kota (Rajasthan)', 'Pali (Rajasthan) to Udaipur', 'Udaipur to Pali (Rajasthan)', 
                     'Sikar to Bikaner', 'Jaipur (Rajasthan) to Bharatpur', 'Kishangarh to Jodhpur', 
                     'Jaipur (Rajasthan) to Bhilwara', 'Kota (Rajasthan) to Udaipur', 'Jaipur (Rajasthan) to Pilani', 
                     'Jaipur (Rajasthan) to Mathura', 'Bikaner to Sikar']
    elif state_transport_corp == 'Kerala (KSRTC)':
        route = ['Bangalore to Kozhikode', 'Kozhikode to Ernakulam', 'Kozhikode to Bangalore', 
                 'Ernakulam to Kozhikode', 'Kozhikode to Mysore', 'Kozhikode to Thiruvananthapuram', 
                 'Bangalore to Kalpetta (kerala)', 'Mysore to Kozhikode', 'Kalpetta (kerala) to Bangalore', 
                 'Kozhikode to Thrissur', 'Thiruvananthapuram to Kozhikode', 'Bangalore to Kannur', 
                 'Kozhikode to Kottayam', 'Kannur to Bangalore', 'Kottayam to Kozhikode', 'Thrissur to Kozhikode', 
                 'Kozhikode to Kalpetta (kerala)', 'Coimbatore to Ooty', 'Kalpetta (kerala) to Kozhikode']
    elif state_transport_corp == 'Himachal Pradesh (HRTC)':
        route = ['Delhi to Shimla', 'Shimla to Delhi', 'Manali to Chandigarh', 'Chandigarh to Manali', 
                 'Delhi to Manali', 'Hamirpur (Himachal Pradesh) to Chandigarh', 'Delhi to Hamirpur (Himachal Pradesh)', 
                 'Delhi to Chandigarh', 'Manali to Delhi', 'Hamirpur (Himachal Pradesh) to Delhi', 
                 'Chandigarh to Hamirpur (Himachal Pradesh)', 'Shimla to Manali', 'Delhi to Dharamshala (Himachal Pradesh)', 
                 'Shimla to Chandigarh', 'Chandigarh to Dharamshala (Himachal Pradesh)', 'Delhi to Baddi (Himachal Pradesh)', 
                 'Dharamshala (Himachal Pradesh) to Chandigarh', 'Chamba (Himachal Pradesh) to Chandigarh', 
                 'Delhi to Dalhousie', 'Delhi to Chamba (Himachal Pradesh)', 'Dalhousie to Delhi', 'Solan to Delhi', 
                 'Delhi to Palampur', 'Dharamshala (Himachal Pradesh) to Delhi', 'Delhi to Solan', 
                 'Chandigarh to Reckong Peo (Himachal Pradesh)', 'Manali to Shimla', 'Palampur to Delhi', 
                 'Chandigarh to Kullu', 'Kangra to Chandigarh', 'Kullu to Chandigarh', 'Delhi to Kangra', 
                 'Chamba (Himachal Pradesh) to Delhi', 'Palampur to Chandigarh', 'Chandigarh to Shimla', 
                 'Chandigarh to Kangra', 'Delhi to Nalagarh', 'Baddi (Himachal Pradesh) to Delhi', 'Kangra to Delhi', 
                 'Ghumarwin to Delhi', 'Delhi to Sarkaghat']
    elif state_transport_corp == 'Punjab (PEPSU)':
        route = ['Patiala to Delhi', 'Delhi to Patiala', 'Ludhiana to Delhi', 'Delhi to Ludhiana', 
                 'Phagwara to Delhi', 'Jalandhar to Delhi', 'Delhi to Jalandhar', 'Patiala to Delhi Airport', 
                 'Jalandhar to Delhi Airport', 'Ludhiana to Delhi Airport', 'Phagwara to Delhi Airport', 
                 'Delhi Airport to Ludhiana', 'Delhi to Phagwara', 'Delhi to Amritsar', 'Amritsar to Delhi', 
                 'Delhi Airport to Patiala', 'Amritsar to Delhi Airport', 'Kapurthala to Delhi', 'Delhi Airport to Jalandhar', 
                 'Chandigarh to Bathinda', 'Chandigarh to Faridkot', 'Chandigarh to Patiala']
    elif state_transport_corp == 'Bihar (BSRTC)':
        route = ['Patna (Bihar) to Bettiah', 'Gopalganj (Bihar) to Delhi', 'Patna (Bihar) to Motihari', 
                 'Delhi to Motihari', 'Bettiah to Patna (Bihar)', 'Motihari to Delhi', 'Patna (Bihar) to Balmiki Nagar (bihar)', 
                 'Balmiki Nagar (bihar) to Patna (Bihar)', 'Patna (Bihar) to Kathmandu', 'Patna (Bihar) to Katihar', 
                 'Patna (Bihar) to Purnea', 'Patna (Bihar) to Hazaribagh', 'Ranchi to Patna (Bihar)', 
                 'Hazaribagh to Patna (Bihar)', 'Patna (Bihar) to Raxaul', 'Muzaffarpur (Bihar) to Kathmandu', 
                 'Patna (Bihar) to Ranchi', 'Muzaffarpur (Bihar) to Ranchi', 'Kathmandu to Patna (Bihar)', 
                 'Ranchi to Muzaffarpur (Bihar)', 'Motihari to Lucknow', 'Lucknow to Motihari', 'Motihari to Kathmandu', 
                 'Agra to Motihari', 'Patna (Bihar) to Janakpur (Nepal)', 'Muzaffarpur (Bihar) to Hazaribagh', 
                 'Purnea to Patna (Bihar)', 'Patna (Bihar) to Araria (Bihar)', 'Darbhanga to Patna (Bihar)', 
                 'Patna (Bihar) to Saharsa', 'Motihari to Agra', 'Hajipur (Bihar) to Kathmandu', 'Kathmandu to Motihari', 
                 'Patna (Bihar) to Forbesganj', 'Ranchi to Hajipur (Bihar)', 'Lucknow to Gopalganj (Bihar)']
    elif state_transport_corp == 'South Bengal (SBSTC)':
        route = ['Burdwan to Kolkata', 'Kolkata to Burdwan', 'Durgapur (West Bengal) to Kolkata', 
                 'Kolkata to Haldia', 'Haldia to Kolkata', 'Kolkata to Durgapur (West Bengal)', 
                 'Kolkata to Arambagh (West Bengal)', 'Digha to Kolkata', 'Kolkata to Digha', 'Kolkata to Bankura', 
                 'Asansol (West Bengal) to Kolkata', 'Midnapore to Kolkata', 'Kolkata to Asansol (West Bengal)', 
                 'Kolkata to Siliguri', 'Kolkata to Nimtouri', 'Siliguri to Kolkata', 'Kolkata to Contai (Kanthi)', 
                 'Digha to Durgapur (West Bengal)', 'Kolkata to Midnapore', 'Kolkata to Nandakumar (west bengal)', 
                 'Kolkata to Burdwan']
    elif state_transport_corp == 'West Bengal':
        route = ['Kolkata to Digha', 'Digha to Kolkata', 'Burdwan to Kolkata', 'Durgapur (West Bengal) to Kolkata', 
                 'Haldia to Kolkata', 'Asansol (West Bengal) to Kolkata', 'Kolkata to Durgapur (West Bengal)', 
                 'Kolkata to Burdwan', 'Midnapore to Kolkata', 'Kolkata to Nimtouri', 'Nimtouri to Kolkata', 
                 'Kolkata to Arambagh (West Bengal)', 'Arambagh (West Bengal) to Kolkata', 'Kolkata to Asansol (West Bengal)', 
                 'Siliguri to Kolkata', 'Kolkata to Siliguri', 'Kolkata to Contai (Kanthi)', 'Contai (Kanthi) to Kolkata', 
                 'Kolkata to Nandakumar (west bengal)', 'Nandakumar (west bengal) to Kolkata']
    elif state_transport_corp == 'Chandigarh (CTU)':
        route = ['Delhi to Chandigarh', 'Chandigarh to Delhi', 'Chandigarh to Shimla', 'Shimla to Chandigarh', 
                 'Chandigarh to Manali', 'Manali to Chandigarh', 'Chandigarh to Dehradun', 'Dehradun to Chandigarh', 
                 'Chandigarh to Jaipur (Rajasthan)', 'Jaipur (Rajasthan) to Chandigarh', 'Chandigarh to Haridwar', 
                 'Haridwar to Chandigarh', 'Chandigarh to Jalandhar', 'Jalandhar to Chandigarh', 'Chandigarh to Katra', 
                 'Katra to Chandigarh', 'Chandigarh to Pathankot', 'Pathankot to Chandigarh', 'Chandigarh to Kullu', 
                 'Kullu to Chandigarh', 'Chandigarh to Dharamshala (Himachal Pradesh)', 'Dharamshala (Himachal Pradesh) to Chandigarh', 
                 'Chandigarh to Ludhiana', 'Ludhiana to Chandigarh', 'Chandigarh to Amritsar', 'Amritsar to Chandigarh', 
                 'Chandigarh to Jammu', 'Jammu to Chandigarh', 'Chandigarh to Gurdaspur', 'Gurdaspur to Chandigarh', 
                 'Chandigarh to Kangra', 'Kangra to Chandigarh', 'Chandigarh to Ambala', 'Ambala to Chandigarh']
    elif state_transport_corp == 'Assam (ASTC)':
        route = ['Guwahati to Jorhat', 'Jorhat to Guwahati', 'Guwahati to Sivasagar', 'Guwahati to Tezpur', 
                 'Guwahati to Tinsukia', 'Tezpur to Guwahati', 'Guwahati to Dibrugarh', 'Sivasagar to Guwahati', 
                 'Guwahati to Nagaon', 'Tinsukia to Guwahati', 'Guwahati to Silchar', 'Guwahati to Bongaigaon', 
                 'Guwahati to Bongaigaon', 'Guwahati to Nalbari', 'Guwahati to Barpeta', 'Guwahati to Lakhimpur', 
                 'Guwahati to Nalbari', 'Nagaon to Guwahati', 'Bongaigaon to Guwahati', 'Silchar to Guwahati', 
                 'Lakhimpur to Guwahati', 'Barpeta to Guwahati', 'Nalbari to Guwahati', 'Dibrugarh to Guwahati']
    elif state_transport_corp == 'Kadamba (KTCL)':
        route = ['Panjim to Margao', 'Margao to Panjim', 'Margao to Vasco', 'Panjim to Vasco', 'Vasco to Panjim', 
                 'Vasco to Margao', 'Mapusa to Panjim', 'Panjim to Mapusa', 'Panjim to Calangute', 'Calangute to Panjim', 
                 'Panjim to Canacona', 'Canacona to Panjim', 'Mapusa to Calangute', 'Calangute to Mapusa', 
                 'Mapusa to Margao', 'Margao to Mapusa', 'Panjim to Ponda', 'Ponda to Panjim', 'Mapusa to Vasco', 
                 'Vasco to Mapusa']

    bus_route = st.selectbox('Select the route:',route)

    bus_type = st.selectbox('Select the bus type:',['Sleeper','Seater'])

    air_con = st.selectbox('Select A/C or Non A/C:',['A/C', 'Non A/C'])

    ratings = st.selectbox('Select the ratings:',['4 to 5','3 to 4','2 to 3','1 to 2','0 to 1','unrated'])

    starting_time = st.selectbox('Select the starting time:',['00:00 to 06:00','06:00 to 12:00','12:00 to 18:00','18:00 to 24:00'])

    price_option = ['upto ₹200','upto ₹400','upto ₹600','upto ₹800','upto ₹1000', '₹1000+']
    price = st.select_slider('Select the bus fare:',price_option)
    

    click_button = st.button('search')

if bus_type == 'Sleeper' and air_con == 'A/C':
     bustype_query = """bustype LIKE '%Sleeper%'
                    AND (bustype LIKE '%A/C%' OR
                        bustype LIKE 'A/C%')
                    AND (bustype NOT LIKE '%Non%' OR
                        bustype NOT LIKE 'Non%' OR
                        bustype NOT LIKE 'NON%')"""
elif bus_type == 'Seater' and air_con == 'A/C':
     bustype_query = """bustype LIKE '%Seater%'
                    AND (bustype LIKE '%A/C%' OR
                        bustype LIKE 'A/C%')
                    AND bustype LIKE '%MULTI AXLE'
                    And (bustype NOT LIKE '%Non%' OR
                        bustype NOT LIKE 'Non%' OR
                        bustype NOT LIKE 'NON%')"""
elif bus_type == 'Sleeper' and air_con == 'Non A/C':
     bustype_query = """bustype LIKE '%Sleeper%'
                    AND (bustype LIKE '%Non%' OR
                        bustype LIKE 'Non%' OR
                        bustype LIKE 'NON%')"""  
elif bus_type == 'Seater' and air_con == 'Non A/C':
     bustype_query = """bustype LIKE '%Seater%'
                    AND (bustype LIKE '%Non%' OR
                        bustype LIKE 'Non%' OR
                        bustype LIKE 'NON%')"""         

if ratings == '4 to 5':
     rating_query = """star_rating >= 4 AND
                        star_rating <= 5"""
elif ratings == '3 to 4':
     rating_query = """star_rating >= 3 AND
                        star_rating <= 4"""
elif ratings == '2 to 3':
     rating_query = """star_rating >= 2 AND
                        star_rating <= 3"""
elif ratings == '1 to 2':
     rating_query = """star_rating >= 1 AND
                        star_rating <= 2"""
elif ratings == '0 to 1':
     rating_query = """star_rating > 0 AND
                        star_rating <= 1"""
elif ratings == 'unrated':
     rating_query = "star_rating = 0"

if starting_time == '00:00 to 06:00':
     time_query = f"""departing_time >= '{starting_time[:6]}' AND 
                    departing_time <= '{starting_time[-5:]}'"""
elif starting_time == '06:00 to 12:00':
     time_query = f"""departing_time >= '{starting_time[:6]}' AND 
                    departing_time <= '{starting_time[-5:]}'"""
elif starting_time == '12:00 to 18:00':
     time_query = f"""departing_time >= '{starting_time[:6]}' AND 
                    departing_time <= '{starting_time[-5:]}'"""
elif starting_time == '18:00 to 24:00':
     time_query = f"""departing_time >= '{starting_time[:6]}' AND 
                    departing_time <= '{starting_time[-5:]}'"""


if price == 'upto ₹200':
     price_query = "price <= 200"
elif price == 'upto ₹400':
     price_query = "price <= 400"
elif price == 'upto ₹600':
     price_query = "price <= 600"
elif price == 'upto ₹800':
     price_query = "price <= 800"
elif price == 'upto ₹1000':
     price_query = "price <= 1000"
elif price == '₹1000+':
     price_query = "price >= 1000"

st.title(':rainbow[Bus information for the route]')

query = f"""SELECT * FROM all_bus_data WHERE
            route_name = '{bus_route}' AND 
            {bustype_query} AND
            {rating_query} AND
            {time_query} AND
            {price_query};"""
if click_button:
        # Fetch data from the database
        data, columns = fetch_data(query)
        # Convert to a DataFrame
        df = pd.DataFrame(data, columns=columns)
        
        st.write(df)

    


# In[ ]:




