#!/usr/bin/env python
# coding: utf-8


try:
    import cPickle as pickle
except ImportError:
    import pickle
import signal
import logging
from twisted.internet import reactor, defer
from scrapy.core.engine import ExecutionEngine
from scrapy.resolver import CachingThreadedResolver
from scrapy.extension import ExtensionManager
from scrapy.signalmanager import SignalManager
from scrapy.utils.ossignal import install_shutdown_handlers, signal_names
from scrapy.utils.misc import load_object
from scrapy.utils.project import get_project_settings
from scrapy import signals
from billiard import Process
logging.basicConfig()


class Crawler(object):

    def __init__(self, settings):
        self.configured = False
        self.settings = settings
        self.signals = SignalManager(self)
        self.stats = load_object(settings['STATS_CLASS'])(self)
        self._start_requests = lambda: ()
        self.crawling = False
        self._spider = None
        lf_cls = load_object(self.settings['LOG_FORMATTER'])
        self.logformatter = lf_cls.from_crawler(self)

    def configure(self):
        if self.configured:
            return
        self.configured = True
        self.extensions = ExtensionManager.from_crawler(self)
        self.engine = ExecutionEngine(self, self._spider_closed)

    def crawl(self, spider, requests=None):
        assert self._spider is None, 'Spider already attached'
        self._spider = spider
        spider.from_crawler(self)
        if requests is None:
            self._start_requests = spider.start_requests
        else:
            self._start_requests = lambda: requests

    def _spider_closed(self, spider=None):
        if not self.engine.open_spiders:
            self.stop()

    @defer.inlineCallbacks
    def start(self):
        yield defer.maybeDeferred(self.configure)
        if self._spider:
            yield self.engine.open_spider(self._spider, self._start_requests())
        yield defer.maybeDeferred(self.engine.start)

    @defer.inlineCallbacks
    def stop(self):
        if self.configured and self.engine.running:
            yield defer.maybeDeferred(self.engine.stop)


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

    def __init__(self, project, debug=True):
        Process.__init__(self)
        self.debug = debug
        self.project = project
        spider = self.create_spider()
        if spider:
            self.name = spider.name
            self.install = True
        else:
            self.install = False

    def _setup(self, spider):
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.configure()
        crawler.signals.connect(self._done_task,
                                signal=signals.spider_closed)
        crawler.crawl(spider)
        crawler.start()
        self.add_crawler()

    def _crawl_next(self, chain):
        spider_next = self.create_spider(chain)
        logging.error(">>>>>>> chain %s" % chain)
        if not spider_next:
            self.remove_crawler()
        else:
            settings = get_project_settings()
            crawler = Crawler(settings)
            crawler.configure()
            crawler.signals.connect(self._done_task,
                                    signal=signals.spider_closed)
            crawler.crawl(spider_next)
            crawler.start()
            self.add_crawler()

    def start(self):
        self._setup(self.spider)
        reactor.run()

    def _done_task(self, spider):
        logging.error(spider.chain_next)
        if spider.chain_next:
            self._crawl_next(spider.chain_next)
        else:
            self.remove_crawler()
