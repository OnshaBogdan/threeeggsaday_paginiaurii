# -*- coding: utf-8 -*-
import asyncio
import logging

from quart import Quart, jsonify, request
from crochet import setup

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from main import *
from send_email import send_email
from paginiaurii.paginiaurii.spiders.paginiaurii_spider import PaginiauriiSpiderSpider
setup()
app = Quart(__name__)

process = CrawlerRunner()


def export_result(settings, config):
    logging.warning('Exporting...')
    filename = settings['FEED_URI']
    if config['output_file_format'] in ['excel', 'xlsx']:
        filename = export_to_excel(settings)

    logging.warning('Sending an email...')
    send_email(config['sender_email'], config['sender_password'], config['receiver_email'], filename)

    logging.warning('Successfully finished.')


async def io_background_task(search_query, search_location, output_file_format):
    logging.warning('Getting config settings...')
    config = create_config(search_query, search_location, output_file_format)

    logging.warning('Setting up crawler...')
    settings = set_default_setting(get_project_settings(), config)

    process = CrawlerRunner(settings)
    process.crawl(
        PaginiauriiSpiderSpider,
        search_query=config['search_query'],
        search_location=config['search_location'],
        output_file_format=output_file_format,
        config=config,
        settings=settings
    )
    logging.warning('Starting crawler')


@app.route('/', methods=['POST'])
async def add_scraping_task():
    required_keys = ['search_query', 'search_location', 'output_file_format']
    request_data = await request.json
    search_query = request_data['search_query']
    search_location = request_data['search_location']
    output_file_format = request_data['output_file_format']

    if all(key in request_data for key in required_keys):
        asyncio.ensure_future(io_background_task(search_query, search_location, output_file_format))
        return jsonify({'message': 'Task Added'}), 200
    return jsonify({'message': 'Failed'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

