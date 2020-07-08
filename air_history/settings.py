# -*- coding: utf-8 -*-

# Scrapy settings for air_history project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'air_history'

SPIDER_MODULES = ['air_history.spiders']
NEWSPIDER_MODULE = 'air_history.spiders'
# USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
DOWNLOADER_MIDDLEWARES = {
   'air_history.middlewares.AreaSpiderMiddleware': 543,
}

ITEM_PIPELINES = {
   'air_history.pipelines.AirHistoryPipeline': 300,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'air_history (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16
DOWNLOAD_DELAY=0.5
CONCURRENT_REQUESTS = 16
DOWNLOAD_TIMEOUT = 15

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
         'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
         'Accept-Language': "zh-CN,zh;q=0.9",
         'Cache-Control': "no-cache",
         'Connection': "keep-alive",
         'Cookie': "SESSIONID=aDgLRCsraVNl9s9bLWTlNdiNyJrVVgcMldv9R1gSxEg; osd=V1sVA0pDvKBq4UN3DkaeuOMEoy4aKNiWMa4DRz8o8sUyoyQJZlVwdTHjRnQPiqUwfDy4AA7XL46XlprniqvmTXI=; JOID=UlEQC0xGtqVi50Z9C06YvekBqygfIt2eN6sJQjcu9883qyIMbFB4czTpQ3wJj681dDq9CgvfKYudk5Lhj6HjRXQ=; _zap=ff292406-6427-4d68-867d-ea4cf2c7564e; d_c0='AMDTgSXAJRGPTnnTg56ojDbwppfNd36jUBY=|1587371174'; _ga=GA1.2.1010108192.1587371199; tshl=; _xsrf=9diq8J2UzOcnb6gYdd9numJa4TU41KWX; tst=r; q_c1=3a96c6d96a6f4489a69d2be2efddd064|1590384154000|1587545082000; __utma=51854390.1010108192.1587371199.1590385825.1590385825.1; __utmz=51854390.1590385825.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100--|2=registration_date=20170711=1^3=entry_date=20170711=1; _gid=GA1.2.709288183.1590974713; SESSIONID=mg6ZKF31oHfXCcxkZLK08eNgtodEbPZr6AKt3xdI2P1; osd=WlgXBEM0rqp3viVVezumcs4kWAZgUcuZIvVrZE9b7s4q8kYlEsXxdCa2L1JxbmlcVmNIef5moYSja_ArJggcjXs=; JOID=U1wRAUo9qqxytyxRfT6ve8oiXQ9pVc2cK_xvYkpS58os908sFsP0fS-yKVd4Z21aU2pBffhjqI2nbfUiLwwaiHI=; l_n_c=1; l_cap_id='ODRkMWRjODEwNzQ1NGI5NDkzNjMyNTU1YjAyZDBiMjk=|1590981736|f61cb01fb2e67da594f87572af48b835d6567156'; r_cap_id='MGQwZGQxY2M3ZThiNDhlOTk3NWU1ODgzZDE4MDVjM2Q=|1590981736|42f961fca45b737822f58d01bb2a0878644e8f74'; cap_id='MzUyN2RjZTE4MWFlNGIxY2FlNGQ2MGZiMDI4ZWVjMjc=|1590981736|6baac0da0b30d6c1b56dfdbb6d5a0b864ce59c59'; n_c=1; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1590974723,1590988240,1590988278,1590994396; capsion_ticket='2|1:0|10:1590996927|14:capsion_ticket|44:NGNkZDE1ODJjOTE4NGYzMjkyYjdhMDgyYTAwYjQ1NTI=|af6a46353ac5aedf6c2bdfc3fca46fcc78dff55e4d8c7bc517ad83b2e08e7f75'; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1591004970; KLBRSID=53650870f91603bc3193342a80cf198c|1591005106|1591002841",
         'Host': "www.zhihu.com",
         'Pragma': "no-cache",
         'Sec-Fetch-Dest': "document",
         'Sec-Fetch-Mode': "navigate",
         'Sec-Fetch-Site':"none",
         'Sec-Fetch-User': "?1",
         'Upgrade-Insecure-Requests': "1",
         'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}
USER_AGENT_LIST = [
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
      "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
      "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'air_history.middlewares.AirHistorySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'air_history.middlewares.AirHistoryDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'air_history.pipelines.AirHistoryPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# 连接数据MySQL
# 数据库地址
MYSQL_HOST = 'localhost'
# 数据库用户名:
MYSQL_USER = 'root'
# 数据库密码
MYSQL_PASSWORD = '123456'
# 数据库端口
MYSQL_PORT = 3306
# 数据库名称
MYSQL_DBNAME = 'zhihu'
# 数据库编码
MYSQL_CHARSET = 'utf8'