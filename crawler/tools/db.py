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
        return self._kiread["rawdata"]


    @property
    def consumer(self):
        return self._db["consumer"]

    @property
    def linkbase(self):
        return self._db['linkbase']

    @property
    def user(self):
        return self._db["user"]


conn = MongodbCursor()

__all__ = ["conn"]
