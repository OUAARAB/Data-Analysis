# Google Scholar Project

## Requirements

- Python 3.x
- Pandas
- Selenium
- BeautifulSoup

You can install the required Python packages using the following command:

```bash
pip install pandas Selenium BeautifulSoup

```

## Usage

1. Setup
    1. Clone the repository or download the scripts and modules

2. Web Scraping

   1. Run the first script `scrap.py` using the following command:

      ``` python
      python scrap.py 
      ```

   2. Enter the search query when prompted.

   3. The script launches a Chrome browser, performs a Google Scholar search, and scrapes data.

   4. Extracted data is stored in ./files/ with the search query and current date.

3. Data Analysis

   1. Ensure the web scraping script has been run to generate the JSON file (python2023_12_20.json in this example).

   2. Run the first script `main.py` using the following command:

      ``` python
      python main.py
      ```

   3. The script loads data, creates a Pandas DataFrame, and displays the results.

## File Structure

- ToFile.py : Module with a function to write data into a JSON file.
- Service.py : Module with a Service class containing the logic to extract data.
- Data.py : Module with a Class for storing scraped data.
- scrap.py : The main script containing the web scraping logic.
- main.py : This script loads data from a file and creates a DataFrame.

