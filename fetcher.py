#!/usr/bin/python3
# -*-coding: utf-8 -*-
# vim: sw=4 ts=4 expandtab ai

import hashlib
import logging
import lxml.html
import psycopg2
import ssl
import time
import urllib.parse
import urllib.request
import yaml
from datetime import datetime, timedelta

DB_CONFIG_PATH = 'config/database.yml'
BASE_URL = 'https://parallel.ru/news'
MAX_PAGE_NO = 20

NO_VERIFY_CTX = ssl.create_default_context()
NO_VERIFY_CTX.check_hostname = False
NO_VERIFY_CTX.verify_mode = ssl.CERT_NONE

logging.basicConfig(level=logging.INFO, format='%(asctime)2s %(levelname)-8s %(message)s')


class NewsData(object):
    def __init__(self, html_item):
        content = html_item.find_class('field-content')[0]
        self.title = content.text_content().strip()
        self.link = content.find('.//a').attrib['href'].strip()
        self.date_created = datetime.strptime(
            html_item.find_class('views-field views-field-created')[0].text_content().strip(),
            '%d.%m.%Y'
        ).date()
        type_field = html_item.find_class('field-content newstype-field')
        self.tags = [a.text_content().strip() for a in 
            type_field[0].findall('.//a')
        ] if type_field else []
        self.digest = hashlib.sha1(self.title.encode()).hexdigest()

    def insert_query(self):
        return """
            INSERT INTO newsfeed_imports(title, initial_title, link, date_created, tags, created_at, updated_at)
            SELECT %(title)s, %(digest)s, %(link)s, %(date_created)s, %(tags)s, %(now)s, %(now)s
            WHERE NOT EXISTS (SELECT 1 FROM newsfeed_imports where initial_title = %(digest)s)
            RETURNING id;
            """, dict({'now': datetime.now()}, **vars(self))

def get_page(page_num):
    with urllib.request.urlopen(
        '{}?page={}'.format(BASE_URL, page_num),
         context=NO_VERIFY_CTX
    ) as req:
        return req.read()

while True:
    logging.info('Loading database config from %s...', DB_CONFIG_PATH)
    with open(DB_CONFIG_PATH) as f:
        db_config = yaml.safe_load(f)

    logging.info('Connecting to database...')
    db_conn = psycopg2.connect(
        dbname=db_config['database'],
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host'],
        port=db_config['port']
    )
    cur = db_conn.cursor()

    cur.execute('select max(date_created) from newsfeed_imports;')
    last_imported_date = cur.fetchone()[0]
    logging.info('Last imported news in database are from %s', last_imported_date.strftime('%Y-%m-%d'))

    cur.execute('select cron_schedule, cron_value from newsfeed_settings;')
    time_unit, cron_value = cur.fetchone()
    time_unit += 's'
    time_to_sleep = timedelta(**{time_unit: cron_value})

    logging.info('Starting fetch')
    
    imported_news = []
    for p in range(0, MAX_PAGE_NO + 1):
        page_data = get_page(p)
        logging.info('\nSuccessfully loaded page #%d (response length = %d)', p, len(page_data))

        doc = lxml.html.fromstring(page_data)
        news = doc.find_class('contextual-links-region')
        logging.info('News quantity on page #%d: %d', p, len(news))

        import_candidates = []
        for news_elem in news:
            nd = NewsData(news_elem)
            if nd.date_created >= last_imported_date:
                import_candidates.append(nd)

        logging.info('Found %d candidates to import from page #%d', len(import_candidates), p)
        if len(import_candidates) < 1:
            break
        imported_news.extend(import_candidates)
        time.sleep(1)
    
    imported_news.sort(key=lambda x: x.date_created)
    existing = 0
    imported = 0
    for news_item in imported_news:
        cur.execute(*news_item.insert_query())
        if cur.fetchone():
            imported += 1
        else:
            existing += 1
    logging.info(
        '\nSuccessfully imported %d news, %d news were already existing in database',
        imported,
        existing
    )
    if imported:
        logging.warning('Commiting changes...')
        db_conn.commit()

    cur.close()
    db_conn.close()
    logging.info(
        'Next fetch will be done in %d %s (%d seconds)',
        cron_value,
        time_unit,
        time_to_sleep.total_seconds()
    )
    time.sleep(time_to_sleep.total_seconds())



