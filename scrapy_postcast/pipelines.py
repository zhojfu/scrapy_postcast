from scrapy.conf import settings
from scrapy import log
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class ScrapyPostcastPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        #line = json.dumps(dict(item))
        #self.file.write(line)
        return item

class MongoDBPipeline(object):
    def __init__(self):
        import pymongo
        import gridfs
        connection = pymongo.Connection(settings['MONGODB_SERVER'], 
                settings['MONGODB_PORT'])
        self.db = connection[settings['MONGODB_DB']]
        self.fs = gridfs.GridFS(self.db,settings['GridFs_Collection'])
        self.collection = self.db[settings['MONGODB_COLLECTION']]
        if self.__get_uniq_key() is not None:
            self.collection.create_index(self.__get_uniq_key(), unique = True)

    def process_item(self, item, spider):
        postcast_detail = {
            'postcast_name':item.get('_id'),
            'postcast_text':item.get('text'),
            'postcast_url':item.get('url'),
        }
        if self.__get_uniq_key() is None:
            self.collection.inset(postcast_detail)
        else:
            self.collection.update(
                    {self.__get_uniq_key(): item[self.__get_uniq_key()]},
                    postcast_detail,
                    upsert = True)
        with open('postcast.mp3', 'wb') as f:
            f.write(item.get('podtcast'))
            self.fs.put(f.read(), filename = item.get('_id'))

        log.msg("Item wrote to MongoDB database %s %s" %
                (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                level = log.DEBUG, spider = spider)
        return item

    def persist_file(self, key, file_content, filename):
        pass

    def __get_uniq_key(self):
        if not settings['MONGODB_UNIQ_KEY'] or settings['MONGODB_UNIQ_KEY'] == "":
            return None
        return settings['MONGODB_UNIQ_KEY']
