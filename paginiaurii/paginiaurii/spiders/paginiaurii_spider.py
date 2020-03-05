# -*- coding: utf-8 -*-
import re
import logging
import string

import scrapy


def text_to_query(s):
    return s.replace(' ', '+')


def get_start_urls(query, location):
    if query == '' and location == '':
        alphabet = list(string.ascii_uppercase)
        return [f'https://www.paginiaurii.ro/cauta/{i}{k}/' for i in alphabet for k in alphabet]
    if location != '':
        return [f'https://www.paginiaurii.ro/cauta/{text_to_query(query)}%2bnear%2b{text_to_query(location)}/']
    else:
        return [f'https://www.paginiaurii.ro/cauta/{text_to_query(query)}/']


class PaginiauriiSpiderSpider(scrapy.Spider):
    name = 'paginiaurii_spider'

    base_urls = 'https://www.paginiaurii.ro'

    def __init__(self, *a, **kw):
        super(PaginiauriiSpiderSpider, self).__init__(*a, **kw)

        self.start_urls = get_start_urls(self.search_query, self.search_location)

    def parse(self, response):
        logging.error(f'Parsing list: {response.url}')
        urls = response.css('div.result h2.item-heading a::attr(href)').getall()
        urls = [self.base_urls + url for url in urls]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page,
                                 meta={'query': self.search_query, 'location': self.search_location})

        next_page = response.xpath("//a[text()='Următorul']/@href").get()
        if next_page is not None and next_page != '':
            next_page_url = self.base_urls + next_page
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_page(self, response):
        logging.error(f'Parsing page: {response.url}')
        def safe_strip(s: str) -> str:
            try:
                return s.strip()
            except:
                return ''

        def get_timetable():
            timetable = response.xpath("//li[@class='open' or @class='close']/text()").get()
            timetable = safe_strip(timetable)
            return timetable

        def get_company_name():
            company_name_raw = response.css('.type-1 span::text').get()
            company_name = safe_strip(company_name_raw)
            return company_name

        def get_address():
            address_raw = response.css('.address::text').get()
            address = safe_strip(address_raw)
            return address

        def get_phone():
            phone_raw = response.xpath("//a[starts-with(@href,'tel:')]/text()").get()
            phone = safe_strip(phone_raw)
            return phone

        def get_activity():
            activity_raw = response.css('#activity a::text').get()
            activity = safe_strip(activity_raw)
            return activity

        def get_website():
            website_raw = response.xpath("//a[@itemprop='url' and @class='t-c']/@href").get()
            website = safe_strip(website_raw)
            return website

        def get_email():
            email_raw = response.xpath("//a[starts-with(@href,'mailto:') and @class='t-c']/text()").get()
            email = safe_strip(email_raw)
            return email

        def get_description():
            descr_raw = response.css('#description p::text').getall()
            descr_raw = [i.strip() for i in descr_raw]
            descr_raw = ' '.join([i for i in descr_raw if i])
            descr = re.sub(' +', ' ', descr_raw)
            return descr

        def get_payment_method():
            method_raw = response.css('#payment-method p::text').get()
            method = safe_strip(method_raw)
            return method

        yield {
            'company_name': get_company_name(),
            'address': get_address(),
            'phone': get_phone(),
            'timetable': get_timetable(),
            'domain': get_activity(),
            'website': get_website(),
            'email': get_email(),
            'description': get_description(),
            'payment_method': get_payment_method(),
            'search_query': response.meta['query'],
            'location': response.meta['location'],
            'url': response.url
        }
