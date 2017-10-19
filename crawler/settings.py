# RABBIT_MQ

RQ_URL = "amqp://guest:guest@localhost:5672"
MQ_USERNAME = "qfbot-crawler"
MQ_PASSWD = "passwd"
HEARTBEAT = 30

REDIS_URL = "redis://localhost:6379/1"

# MONGODB
MONGODB_URI = "mongodb://localhost:27017/"
MONGODB_NAME = "qfbot"

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ITEM_PIPELINES = {
    'crawler.pipelines.MongoPipeline': 200,
}

DOWNLOAD_DELAY = 3

PROXIES = []

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'crawler.tools.agent.RotateUserAgentMiddleware': 400,
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': True,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
}
