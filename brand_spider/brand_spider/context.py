from OpenSSL import SSL
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory

class CustomContextFactory(ScrapyClientContextFactory):
    def __init__(self):
        self.method = SSL.SSLv23_METHOD