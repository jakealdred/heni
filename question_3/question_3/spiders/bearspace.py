import scrapy
import json
import logging
import re

from scrapy.utils.response import open_in_browser
from question_3.items import BearspaceItem


class BearspaceSpider(scrapy.Spider):

    name = "bearspace"

    def start_requests(self):

        all_listings_api_url = "https://www.bearspace.co.uk/_api/wix-ecommerce-storefront-web/api?o=getData&s=WixStoresWebClient&q=query,getData($externalId:String!,$compId:String,$mainCollectionId:String,$limit:Int!,$sort:ProductSort,$filters:ProductFilters,$offset:Int,$withOptions:Boolean,=,false,$withPriceRange:Boolean,=,false){appSettings(externalId:$externalId){widgetSettings}catalog{category(compId:$compId,categoryId:$mainCollectionId){id,name,productsWithMetaData(limit:$limit,onlyVisible:true,sort:$sort,filters:$filters,offset:$offset){list{id,description,options{id,key,title,@include(if:$withOptions),optionType,@include(if:$withOptions),selections,@include(if:$withOptions){id,value,description,key,linkedMediaItems{url,fullUrl,thumbnailFullUrl:fullUrl(width:50,height:50),mediaType,width,height,index,title,videoFiles{url,width,height,format,quality}}}}productItems,@include(if:$withOptions){id,optionsSelections,price,formattedPrice,formattedComparePrice,availableForPreOrder,inventory{status,quantity}isVisible,pricePerUnit,formattedPricePerUnit}customTextFields(limit:1){title}productType,ribbon,price,comparePrice,sku,isInStock,urlPart,formattedComparePrice,formattedPrice,pricePerUnit,formattedPricePerUnit,pricePerUnitData{baseQuantity,baseMeasurementUnit}digitalProductFileItems{fileType}name,media{url,index,width,mediaType,altText,title,height}isManageProductItems,productItemsPreOrderAvailability,isTrackingInventory,inventory{status,quantity,availableForPreOrder,preOrderInfoView{limit}}subscriptionPlans{list{id,visible}}priceRange(withSubscriptionPriceRange:true),@include(if:$withPriceRange){fromPriceFormatted}discount{mode,value}}totalCount}}}}&v=%7B%22externalId%22%3A%22%22%2C%22compId%22%3A%22TPASection_isucjep3%22%2C%22limit%22%3A200%2C%22sort%22%3Anull%2C%22filters%22%3Anull%2C%22offset%22%3A0%2C%22withOptions%22%3Afalse%2C%22withPriceRange%22%3Afalse%2C%22mainCollectionId%22%3Anull%7D"

        headers = {'X-XSRF-TOKEN': '1668108556|W4pwG33tL6YX',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                   'Authorization': 'hLPF3HP3Vuw2r7FJIj4-4b3hebWEVXGizTVn9QPMryw.eyJpbnN0YW5jZUlkIjoiOWRiZDIzZjktMzE0YS00NzVjLWI4OTAtYTZhNjQ1ZGNiZTdhIiwiYXBwRGVmSWQiOiIxMzgwYjcwMy1jZTgxLWZmMDUtZjExNS0zOTU3MWQ5NGRmY2QiLCJtZXRhU2l0ZUlkIjoiOGQ3ODQxYzctNmFkMC00MjdkLTg5NWMtMzFkYzE0ODhmYWVlIiwic2lnbkRhdGUiOiIyMDIyLTExLTEwVDE5OjI5OjE2Ljg1MVoiLCJ2ZW5kb3JQcm9kdWN0SWQiOiJQcmVtaXVtMSIsImRlbW9Nb2RlIjpmYWxzZSwib3JpZ2luSW5zdGFuY2VJZCI6ImJjYjk0MjcyLWU2ZWEtNDc1YS05ZThlLWZjYTEwMDI4NzZlYiIsImFpZCI6ImIwODcxMWY4LTUyYTMtNDAyNi1iOTExLTA3Yzc0MjYyOTcyZCIsImJpVG9rZW4iOiIxMGM1NjIzZS01YjlhLTA1MjEtMzFjYy05NzdhNTE1NDQ0OTQiLCJzaXRlT3duZXJJZCI6IjIzYTJlZDE4LWMyYTgtNDNlZi04ZmIzLWZmYTBjMjQzNGYyOCJ9',
                   'Content-Type': 'application/json; charset=utf-8',
                   'Accept': '*/*'}

        yield scrapy.Request(url=all_listings_api_url, headers=headers, callback=self.parse)

    def parse(self, response):

        api_response = json.loads(response.body.decode())

        for listing in api_response['data']['catalog']['category']['productsWithMetaData']['list']:

            if listing['isInStock'] is True:

                item = BearspaceItem()
                listing_url = listing['urlPart']

                item['url'] = 'https://www.bearspace.co.uk/product-page/{}'.format(listing_url)
                item['title'] = listing['name']
                item['price_gbp'] = listing['price']

                # API returns the description as HTML - we split on the p tag and then remove all HTML tags, so we can more
                # easily iterate over the description text to extract media and dimensions
                raw_description = listing['description'].replace('&nbsp;', '')
                description = list(map(lambda x: re.sub(re.compile('<.*?>'), ' ', x), raw_description.split('<p>')))[1:]

                if not description:
                    description = list(map(lambda x: re.sub(re.compile('<.*?>'), ' ', x), raw_description.split('<br>')))

                for desc in description:
                    if ('x' in desc.lower() and 'cm' in desc.lower()) or 'artist:' in desc.lower():
                        pass
                    else:
                        item['media'] = desc
                        break

                description = ' '.join(description)

                try:
                    item['height_cm'] = re.findall('(?:height|x|X)+\s?\d+(?:\.\d+)?\s?(?:x|X|h|H)?', description)[0]
                    item['height_cm'] = item['height_cm'].lower().replace('x', '').replace('height', '').replace('h', '').strip()

                    widths = re.findall('width\s?\d+(?:\.\d+)?|\d+(?:\.\d+)?\s?(?:cm|cms|W|w)?\s?[x|X]', description)
                    item['width_cm'] = widths[0].lower().replace('x', '').replace('cms', '').replace('w', '').replace('cm', '').strip()

                    for width in widths:
                        if 'width' in width:
                            item['width_cm'] = width.split(" ")[-1]

                except IndexError:

                    if 'cm diam' in description:
                        diameter = description.split('cm diam')[0].split(" ")[-1]
                        item['height_cm'] = diameter
                        item['width_cm'] = diameter
                    else:
                        logging.warning("Unable to calculate dimensions for url: {} using: {}".format(item['url'], description))

                yield item
