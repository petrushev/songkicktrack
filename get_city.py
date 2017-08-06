import sys
from random import random
from time import sleep

import requests as rq
from lxml.html import fromstring
from dateutil.parser import parse as dt_parse


BASE_URL = 'https://www.songkick.com/metro_areas/'



def fetch_city(city):
    page = 0
    results = []

    while True:
        page = page + 1

        page_results = fetch_page(city, page)
        if len(page_results) == 0:
            break

        results.extend(page_results)

        sleep(random() * .3 + .2)

    return results


def fetch_page(city, page):
    url = '{0}{1}?page={2}'.format(BASE_URL, city, page)
    q = rq.get(url)
    doc = fromstring(q.content)
    doc.make_links_absolute(url)

    items = doc.cssselect('li[title]')

    results = []

    for item in items:
        dt_tag = item.cssselect('time[datetime]')[0]
        dt = dt_parse(dt_tag.attrib['datetime'])

        title_tag = item.cssselect('p.artists.summary')[0]
        title = title_tag.text_content().replace('\n', ' ').strip()
        while ('   ' in title):
            title = title.replace('   ', '  ')

        link_tag = title_tag.cssselect('a[href]')[0]
        link = link_tag.attrib['href']

        result_item = {
            'title': title,
            'link': link,
            'dt': dt}
        results.append(result_item)

    return results


def format_results(results):
    result = u'\n'.join(
        [u'{0}\n    {1}\n    {2}\n'.format(
            item['title'], item['link'], item['dt'].strftime('%Y %b %d'))
        for item in results]
    )

    return result


def main():
    city = sys.argv[1]

    results = fetch_city(city)
    formatted = format_results(results)

    print formatted.encode('utf-8')


if __name__ == '__main__':
    main()
