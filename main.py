# -*- coding: utf-8 -*-
import json
import logging
import os
import time

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from paginiaurii.paginiaurii.spiders.paginiaurii_spider import PaginiauriiSpiderSpider
from export import export


def get_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


def generate_filename():
    timestamp = int(time.time())
    return timestamp


def set_default_setting(settings, config):
    settings.update(
        {
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'LOG_LEVEL': 'WARNING',
            'LOG_FILE': 'log.txt',
            'FEED_EXPORT_ENCODING': 'utf-8',
            'DOWNLOADER_MIDDLEWARES': {
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
            }
        }
    )
    if config['output_file_format'] in ['csv', 'json']:
        filetype = config['output_file_format']
        settings.update(
            {
                'FEED_FORMAT': filetype,
                'FEED_URI': f'data/{generate_filename()}.{filetype}'
            }
        )
    if config['output_file_format'] in ['excel', 'xlsx']:
        settings.update(
            {
                'FEED_FORMAT': 'json',
                'FEED_URI': f'data/{generate_filename()}.json'
            }
        )
    return settings


def export_to_excel(settings):
    filename_raw = settings['FEED_URI']
    filename = filename_raw[0:filename_raw.index('.')]
    export(filename_raw, f'{filename}.xlsx')
    os.remove(filename_raw)


def run():
    logging.error('Getting config settings')
    config = get_config()

    logging.error('Setting up crawler')
    settings = get_project_settings()
    settings = set_default_setting(settings, config)

    process = CrawlerProcess(settings)

    process.crawl(
        PaginiauriiSpiderSpider,
        search_query=config['search_query'],
        search_location=config['search_location']
    )
    logging.error('Starting crawler')
    process.start()

    if config['output_file_format'] in ['excel', 'xlsx']:
        logging.error('Exporting into excel')
        export_to_excel(settings)

    logging.error('Successfully finished.')


if __name__ == '__main__':
    run()
