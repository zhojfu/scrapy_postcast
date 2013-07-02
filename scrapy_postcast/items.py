# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ScrapyPostcastItem(Item):
    # define the fields for your item here like:
    # name = Field()
    _id = Field()
    url = Field()
    desc = Field()
    text = Field()
    podcast = Field()
