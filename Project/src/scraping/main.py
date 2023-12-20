"""
In this model we load data from a json file wn we create our DataFrame
"""
import json
import pandas as pd

# Specify the path to your JSON file
json_file_path = './files/python2023_12_20.json'

# Open the JSON file and load the data
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Extracting authors' information from the loaded JSON data
authors = [author
           for item in list(map(lambda x: x["authors"], data))
           for author in item]

# Filtering out non-dictionary elements from the list of authors
authors = list(filter(lambda x: type(x) == dict, authors))

# Extracting specific information from each author
list_of_names = [author["full_name"] for author in authors]
list_of_universities = [author["university"] for author in authors]
list_of_citations = [author["table data"]["Toutes"]["Citations"] for author in authors]
list_of_h_index = [author["table data"]["Toutes"]["h-index"] for author in authors]
list_of_i10_index = [author["table data"]["Toutes"]["i10-index"] for author in authors]

# Counting the number of publications for each author
publications = [len(author["articles"]) for author in authors]

# Extracting citation data for the years 2022 and 2023
citations_2023 = []
citations_2022 = []

# Looping through authors to extract citation data for the respective years
for author in authors:
    a = 0
    try:
        a = author["graphData"]["2023"]
    except KeyError as keyex:
        a = 0
    finally:
        citations_2023.append(a)

for author in authors:
    a = 0
    try:
        a = author["graphData"]["2022"]
    except KeyError as keyex:
        a = 0
    finally:
        citations_2022.append(a)

# Creating a dictionary with extracted data
data_dict = {"full_name": list_of_names, "university": list_of_universities, "Citations": list_of_citations,
             "h-index": list_of_h_index, "i10-index": list_of_i10_index, "publications": publications,
             "citations_2022": citations_2022, "citations_2023": citations_2023}

# Creating a DataFrame from the dictionary
DF = pd.DataFrame(data_dict)

# Dropping duplicate rows in the DataFrame
DF = DF.drop_duplicates()

print(DF)

# The following section is commented out
# data = [{
#     "full_name": list_of_names[i],
#     "university": list_of_universities[i],
#     "citations": list_of_citations[i],
#     "h-index": list_of_h_index[i],
#     "i10-index": list_of_i10_index[i],
#     "publications": publications[i]
# } for i in range(100)]
#
# print(data)
