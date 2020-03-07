# -*- coding: utf-8 -*-
import json
import os
import time

from export import export


def create_config(search_query, search_location, output_file_format):
    with open('config.json', 'r') as f:
        config = json.load(f)

    config.update(
        {
            'search_query': search_query,
            'search_location': search_location,
            'output_file_format': output_file_format
        }
    )
    return config


def generate_filename():
    timestamp = str(int(time.time()))
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

    excel_filename = f'{filename}.xlsx'
    export(filename_raw, excel_filename)
    os.remove(filename_raw)
    return excel_filename
