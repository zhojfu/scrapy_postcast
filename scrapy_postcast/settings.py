# Scrapy settings for science project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'scrapy_postcast'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['scrapy_postcast.spiders']
NEWSPIDER_MODULE = 'scrapy_postcast.spiders'
DEFAULT_ITEM_CLASS = 'scrapy_postcast.items.ScrapyPostcastItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
    "scrapy_postcast.pipelines.ScrapyPostcastPipeline",
    "scrapy_postcast.pipelines.MongoDBPipeline",
    ]

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'scrapy_postcast'
MONGODB_COLLECTION = 'postcast'
MONGODB_UNIQ_KEY = '_id'

LOG_FILE = 'scrapy_postcast.logfile'
LOG_LEVEL = 'DEBUG'
