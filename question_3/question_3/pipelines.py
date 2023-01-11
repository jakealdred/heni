# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class Question3Pipeline:

    def __init__(self):
        self.dataframe = pd.DataFrame()

    def process_item(self, item, spider):

        dataframe_columns = []
        for k, v in item.items():
            dataframe_columns.append(k)

        df = pd.DataFrame([item], columns=dataframe_columns)
        df = df[['url', 'title', 'media', 'height_cm', 'width_cm', 'price_gbp']]
        self.dataframe = pd.concat([self.dataframe, df])

        return item

    def close_spider(self, spider):
        print(self.dataframe)
        return self.dataframe
