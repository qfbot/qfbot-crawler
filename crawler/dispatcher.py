#!/usr/bin/env python
# coding: utf-8
# vim: set et sw=4 ts=4 sts=4 fenc=utf-8
# Author: YuanLin

try:
    import cPickle as pickle
except ImportError:
    import pickle

from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.crawler import Crawler

from scrapy import log, signals
import logging
from billiard import Process
logging.basicConfig()


reactor.suggestThreadPoolSize(20)


class Boot(Process):
    _crawl_running = 0
    _done = False

    def add_crawler(self):
        self._crawl_running += 1

    def remove_crawler(self):
        self._crawl_running -= 1
        if self._crawl_running == 0:
            self._done = True
            reactor.stop()

    def __init__(self, spider):
        Process.__init__(self)
        self.spider = spider
        self.name = spider.name

    def _setup(self, spider):
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.configure()
        crawler.signals.connect(self._done_task,
                                signal=signals.spider_closed)
        crawler.crawl(spider)
        crawler.start()
        self.add_crawler()

    def _crawl_next(self, spider):
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.configure()
        crawler.signals.connect(self._done_task,
                                signal=signals.spider_closed)
        crawler.crawl(spider)
        crawler.start()

    def run(self):
        self._setup(self.spider)
        log.start()
        reactor.run()

    def _done_task(self, spider):
        logging.error(spider.chain_next)
        if spider.chain_next:
            self._crawl_next(spider.name, spider.chain_next, spider.debug)
        else:
            self.remove_crawler()
