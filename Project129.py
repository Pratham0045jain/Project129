from bs4 import BeautifulSoup
""" beautifulsoup is used to see the doc as html file """
import time
import requests 
import pandas as pd
import csv

# first we are extracting the tables and the tr from the brown stars
# and storing it different lists as name, dis, mass, radius
# finally we are creating a df and changing to csv

START_URL1 = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

page = requests.get(START_URL1)

soup = BeautifulSoup(page.text, "html.parser")
star_table = soup.find_all('table')

tr_tags = star_table[3].find_all('tr')

row_list = []
for tr in tr_tags:
    td = tr.find_all('td')
    """ print(td) """
    row = [i.text.rstrip() for i in td]
    """ print(row) """
    row_list.append(row)
    """ print(row_list) """
    
print(row_list)    

name = []
distance = []
mass = []
radius = []

for i in range(1, len(row_list)):
    name.append(row_list[i][0])
    distance.append(row_list[i][5])
    mass.append(row_list[i][8])
    radius.append(row_list[i][9])

# this value was creating trouble in program as it was 1-42 and also had both radius and mass so i cahnged
# it to 1.42

# also only this was givving bug bcoz, this contained both radius and mass which did not dropped out in the below condition 
# of "remove rows which does not have either one of them"
mass[50] = "1.42"

df1 = pd.DataFrame(list(zip(name, distance, mass, radius)), columns=['name','distance','mass','radius'])
""" print(df1) """

df1.to_csv('dwarf_stars.csv')

time.sleep(3)


# we are reading the csv of dwarf stars and then doing the nessary conversions of radius and mass 
# and converting it to csv
df2 = pd.read_csv("dwarf_stars.csv")
df2 = df2.dropna()

df2["radius"] = 0.102763*df2["radius"]

df2['mass'] = df2['mass'].apply(lambda x: x.replace('$', '').replace(',', '')).astype('float')
df2["mass"] = 0.000954588*df2["mass"]

df2.drop(['Unnamed: 0'],axis=1,inplace=True)
df2.reset_index(drop=True,inplace=True)

df2.to_csv("unit_converted_dwarf_stars.csv")

#---------------------------------------------------------------------------------------------------------------
# we are extracting the data of the bright stars here
time.sleep(3)

start_url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars#verify=False"

page = requests.get(start_url)

soup = BeautifulSoup(page.text, "html.parser")
table = soup.find("table")

temp_list = []

tr_tags = table.find_all("tr")

for tr_tag in tr_tags:
    td_tags = tr_tag.find_all("td")
    row = [i.text.rstrip() for i in td_tags]
    temp_list.append(row)

name = []
distance = []
mass = []
radius = []

for i in range(1, len(temp_list)):
    name.append(temp_list[i][1])
    distance.append(temp_list[i][3])
    mass.append(temp_list[i][5])
    radius.append(temp_list[i][6])

df = pd.DataFrame(list(zip(name, distance, mass, radius)), columns=["name", "distance", "mass", "radius"])
df.to_csv("bright_stars.csv")

#------------------------------------------------------------------------------------------------------
# finally i am merging the data of bright stars and unit_converted_dwarf_stars
time.sleep(3)

file_1 = "bright_stars.csv"
file_2 = "unit_converted_dwarf_stars.csv"

dataset_1 = []
dataset_2 = []

with open(file_1, "r", encoding="utf8") as f:
    csv_reader = csv.reader(f)

    for i in csv_reader:
        dataset_1.append(i)

with open(file_2, "r", encoding="utf8") as f:
    csv_reader = csv.reader(f)

    for j in csv_reader:
        dataset_2.append(j)

header_1 = dataset_1[0]
header_2 = dataset_2[0]

data_1 = dataset_1[1:]
data_2 = dataset_2[1:]

header = header_1 + header_2

data = []

for k in data_1:
    data.append(k)

for l in data_2:
    data.append(l)

with open("final_merged.csv", "w", encoding="utf8") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    csv_writer.writerows(data)



