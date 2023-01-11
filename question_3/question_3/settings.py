from datetime import datetime
BOT_NAME = 'question_3'

SPIDER_MODULES = ['question_3.spiders']
NEWSPIDER_MODULE = 'question_3.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 2

DOWNLOAD_DELAY = 0.2

CONCURRENT_REQUESTS_PER_DOMAIN = 2

DOWNLOAD_TIMEOUT = 10

ITEM_PIPELINES = {
   'question_3.pipelines.Question3Pipeline': 300,
}

LOG_LEVEL = 'INFO'
LOG_FILE = '{}_{}.txt'.format(BOT_NAME, datetime.today().strftime('%Y-%m-%d'))
# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
