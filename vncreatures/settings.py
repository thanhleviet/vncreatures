# -*- coding: utf-8 -*-

# Scrapy settings for vncreatures project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os

BOT_NAME = 'vncreatures'

SPIDER_MODULES = ['vncreatures.spiders']
NEWSPIDER_MODULE = 'vncreatures.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'google.com (+http://www.google.com)'

BASE_URL = "http://www.vncreatures.net"

# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = "/home/root"

IMAGES = "plant_images"

ITEM_PIPELINES = {
    'vncreatures.pipelines.PlantDescriptionJsonPipeline': 200,
}