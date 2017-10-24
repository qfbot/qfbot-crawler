import logging

class MongoPipeline(object):
    """Mongodb pipelines"""
    cursor = conn
    from .tools.db import conn
    from bson.objectid import ObjectId

    def process_item(self, item, spider):
        if spider.debug:
            mongo = self.cursor.sample
        else:
            mongo = self.cursor.rawdata
        if not item:
            return item
        data = {}
        for key in item.keys():
            data.update({key: item[key]})

        find = mongo.find_one({"href": item.get("href")})
        if find:
            mongo.update({"href": item.get("href")},
                         {"$set": data}, upsert=True)

            logging.warn("[-] update data %s" % find['_id'])
            return item
        else:
            data["_id"] = str(ObjectId())
            logging.info("[-] new data %s" % data.get("_id")) 
            mongo.save(data)
            return item


class MySqlPipeline(object):

    def process_item(self, item, spider):
        pass


class JsonFilePipleline(object):
    
    def process_item(self, item, spider):
        pass
