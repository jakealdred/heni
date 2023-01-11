import pandas as pd
from datetime import datetime
from lxml import html

#get html and tree
html_page_link = 'candidateEvalData/webpage.html'
tree = html.parse(html_page_link)
root = tree.getroot()
# parse artist name
artist_name = root.xpath("//meta[@name='og:title']/@content")[0].split(" (b")[0]
# parse painting name
painting_name = root.xpath("//meta[@name='og:title']/@content")[0].split("\n,")[1].strip()
# parse price GBP
price_gbp = root.xpath("//span[@id='main_center_0_lblPriceRealizedPrimary']//text()")[0].split(" ")[1].replace(",", " ")
# parse price US
price_usd = root.xpath("//div[@id='main_center_0_lblPriceRealizedSecondary']//text()")[0].split(" ")[1].replace(",", " ")
# parse price GBP est
price_gbp_est = root.xpath("//span[@id='main_center_0_lblPriceEstimatedPrimary']//text()")[0].replace("GBP ", "")\
                .replace(",", " ").replace("-", ",")
# parse price US est
price_usd_est = root.xpath("//span[@id='main_center_0_lblPriceEstimatedSecondary']//text()")[0].replace("USD ", "")\
                .replace(",", " ").replace("-", ",").replace("(","").replace(")","")

# image link
image_link = root.xpath("//img[@id='imgLotImage']/@src")[0]

# sale date
sale_date = root.xpath("//span[@id='main_center_0_lblSaleDate']//text()")[0].split(",")[0]
sale_date = datetime.strptime(sale_date, '%d %B %Y').strftime('%Y-%m-%d')

# Creating dataframe output

dataframe_dict = {"The name of the artist (Peter Doig)": artist_name,
                  "The name of the painting (The Architect's Home in the Ravine)": painting_name,
                  "Price realised in GBP (11 282 500)": price_gbp,
                  "Price realised in USD (6 370 908)": price_usd,
                  "Estimates in GBP (10 000 000 , 15 000 000)": price_gbp_est,
                  "Estimate in USD (14 509 999 , 21 764999)": price_usd_est,
                  "The url of the image of the painting": image_link,
                  "Saledate of the painting (2016-02-11)": sale_date}

dataframe_columns = []
for k, v in dataframe_dict.items():
    dataframe_columns.append(k)

df = pd.DataFrame([dataframe_dict], columns=dataframe_columns)
df.to_csv('question_1_ouput.csv', encoding='utf-8', index=False)
