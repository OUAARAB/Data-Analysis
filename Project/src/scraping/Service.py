"""
In this Project we use 2 packages named selenium and bs4
"""

# Importing necessary packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Importing custom classes and functions
from Data import Data  # Class for storing scraped data


class Service:
    # Function to create BeautifulSoup object from a given URL using Selenium
    def getSoup(self, url: str):
        driver = webdriver.Chrome()
        driver.get(url)
        return BeautifulSoup(driver.page_source, "lxml")

    # Function to scrape profile information from a given URL
    def getProfileInfo(self, url):
        web = webdriver.Chrome()
        try:
            web.get(url)
            button = web.find_element(By.ID, "gsc_bpf_more")
            button.click()
            sleep(2)
        except Exception as ex:
            print(ex)
        else:
            soup = BeautifulSoup(web.page_source, "lxml")

            body = soup.find(id="gs_bdy")

            full_name = body.find(id="gsc_prf_in").text
            university = body.find("div", {"class": "gsc_prf_il"}).text
            profiles = [a.text for a in body.find(id="gsc_prf_int").find_all("a", {"class": "gsc_prf_inta gs_ibl"})]

            # Extracting information from the table
            table = body.find(id="gsc_rsb_st")
            head_row = table.find("thead").find_all("th")
            body_rows = [i.find_all("td") for i in table.find("tbody").find_all("tr")]

            tableData = {
                head_row[1].text: {
                    "Citations": int(body_rows[0][1].text),
                    "h-index": int(body_rows[1][1].text),
                    "i10-index": int(body_rows[2][1].text)
                },
                head_row[2].text: {
                    "Citations": int(body_rows[0][2].text),
                    "h-index": int(body_rows[1][2].text),
                    "i10-index": int(body_rows[2][2].text)
                }
            }

            # Extracting information from the graph
            graph = body.find("div", {"class": "gsc_md_hist_b"})
            graphYears = [i.text for i in graph.find_all("span", {"class": "gsc_g_t"})]
            graphValues = [int(i.text) for i in graph.find_all("a")]
            graphData = dict(zip(graphYears, graphValues))

            # Extracting information from the list of articles
            trs_articles = soup.find(id="gsc_a_b").find_all("tr", {"class", "gsc_a_tr"})
            tds_article = [i.find_all("td") for i in trs_articles]
            articles = [
                {
                    "title": article[0].find("a").text,
                    "href": f"https://scholar.google.com/{article[0].find('a')['href']}",
                    "authors": article[0].find("div", {"class", "gs_gray"}).text.split(","),
                    "subject": article[0].find_all("div", {"class", "gs_gray"})[1].text,
                    "cited_by": article[1].find("a").text,
                    "cited_by_href": article[1].find("a")["href"],
                    "year": article[2].find("span").text
                }
                for article in tds_article]

            web.close()

            # Returning a dictionary containing the extracted information
            return {"full_name": full_name, "university": university, "profiles": profiles, "table data": tableData,
                    "graphData": graphData, "articles": articles}

    # Function to extract data from the search results page
    def getData(self, soup):
        card = soup.find(id="gs_res_ccl_mid")
        cardRows = card.find_all("div", {"class": "gs_scl"})
        data = []
        for row in cardRows:
            try:
                # Extracting information from each search result card
                # right item
                right_item = row.find("div", {"class": "gs_ri"})

                # Title
                title = right_item.contents[0].find('a').text.strip()
                title_url = right_item.contents[0].find('a')['href']

                # Authors Information
                authors_div = right_item.contents[1]

                # Created Date
                created_data = [x for x in authors_div.text.strip().split() if x.isdigit() and int(x) > 1900][0]

                all_authors_link = authors_div.find_all('a')

                authors = []
                if not all_authors_link:
                    author = authors_div.text.strip().split()
                    authors.append(author)

                for author_a in all_authors_link:
                    authors.append(
                        {"profile_url": f"https://scholar.google.com/{author_a['href']}",
                         "name": author_a.text.strip()})

                # Profile Data
                for author in authors:
                    if type(author) == dict:
                        author.update(self.getProfileInfo(author["profile_url"]))
                        print(author)

                # Description
                description = right_item.contents[2].text.strip()

                # Relative Article
                relative_article = f"https://scholar.google.com{right_item.contents[3].find_all('a')[3]['href']}"

                # Update data array
                data.append(Data(title=title, url=title_url, authors=authors, desc=description, created=created_data,
                                 relative_article=relative_article))
            except IndexError as iex:
                print("Index Error")
            except AttributeError as aer:
                print("AttributeError")
        return data


# if __name__ == "__main__":
#     # Getting user input for the search query
#     search = input("Search : ")
#
#     # Setting up the Chrome webdriver
#     driver = webdriver.Chrome()
#     driver.get("https://scholar.google.com/")
#
#     # Entering the search query in the search box
#     search_box = driver.find_element(By.NAME, "q")
#     search_box.send_keys(search)
#     search_box.send_keys(Keys.RETURN)
#
#     data = []
#     # Looping through multiple pages of search results
#     for i in range(0, 501, 10):
#         url = f"https://scholar.google.com/scholar?start={i}&hl=fr&as_sdt=0%2C5&q={search}&btnG="
#         driver.get(url)
#         WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "gs_res_ccl")))
#         soup = BeautifulSoup(driver.page_source, "lxml")
#         try:
#             # Appending data from each page to the main data list
#             data.append(getData(soup))
#         except Exception as ex:
#             print(ex)
#             continue
#
#     # Flattening the nested list of data
#     data = [j for dic in data for j in dic]
#
#     # Converting data objects to a list of dictionaries
#     jdata = [obj.__dict__ for obj in data]
#
#     # Writing the data to a JSON file
#     write_into_a_json_file(json_file_path=f"{search}.json", data=jdata)
#
#     # Quitting the webdriver
#     driver.quit()
