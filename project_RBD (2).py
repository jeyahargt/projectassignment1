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



                        

    


# In[ ]:




