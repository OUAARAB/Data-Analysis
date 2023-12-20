from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Function to convert and create a JSON file with scraped data
from ToFile import write_into_a_json_file

from Service import Service

# Instantiation
service = Service()

# Getting user input for the search query
search = input("Search : ")

# Setting up the Chrome webdriver
driver = webdriver.Chrome()
driver.get("https://scholar.google.com/")

# Entering the search query in the search box
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(search)
search_box.send_keys(Keys.RETURN)

data = []
# Looping through multiple pages of search results
for i in range(0, 501, 10):
    url = f"https://scholar.google.com/scholar?start={i}&hl=fr&as_sdt=0%2C5&q={search}&btnG="
    driver.get(url)
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "gs_res_ccl")))
    soup = BeautifulSoup(driver.page_source, "lxml")
    try:
        # Appending data from each page to the main data list
        data.append(service.getData(soup))
    except Exception as ex:
        print(ex)
        continue

# Flattening the nested list of data
data = [j for dic in data for j in dic]

# Converting data objects to a list of dictionaries
jdata = [obj.__dict__ for obj in data]

# Writing the data to a JSON file
write_into_a_json_file(json_file_path=f"./files/{search}{str(datetime.now().date()).replace('-', '_')}.json",
                       data=jdata)

# Quitting the webdriver
driver.quit()
