#!/usr/bin/env python
# coding=utf-8

from pymongo import MongoClient
import time
from bson.objectid import ObjectId
from .. import settings


class MongodbCursor(object):

    def __init__(self):
        client = MongoClient(settings.MONGODB_URI)
        self._db = client[settings.MONGODB_NAME]
	self._kiread = client['kiread']

    @property
    def db(self):
        return self._db

    @property
    def linkbase(self):
        return self._db['linkbase']

    @property
    def project(self):
        return self._db['project']

    @property
    def rawdata(self):
        return self._kiread["paper"]

    @property
    def sample(self):
        return self._kiread["paper"]

    @property
    def consumer(self):
        return self._db["consumer"]

    @property
    def linkbase(self):
        return self._db['linkbase']

    @property
    def user(self):
        return self._db["user"]

    def set_link_base(self, project, chain, url):
        query = {
            "project": project,
            "url": url,
            "chain": chain
        }
        find = self.linkbase.find_one(query)
        if find:
            return
        else:
            query.update({
                "timestamp": int(time.time()),
                "_id": str(ObjectId()),
                "status": 0
            })
            self.linkbase.insert(query)

    def get_link_base(self, project, chain):
        query = {
            "project": project,
            "chain": chain,
            "status": 0
        }
        ret = self.linkbase.find(query)
        return [i['url'] for i in ret]

    def exp_link_base(self, url):
        find = self.linkbase.find_one({'url': url})
        if find:
            self.linkbase.update({"url": url}, {"$set": {"status": 1}})


conn = MongodbCursor()

__all__ = ["conn"]
