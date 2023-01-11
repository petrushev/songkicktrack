import sys
from random import random
from time import sleep

import requests as rq
from lxml.html import fromstring
from dateutil.parser import parse as dt_parse


def print_city(city):
    page = 0

    while True:
        page = page + 1

        page_results = fetch_page(city, page)
        if len(page_results) == 0:
            break

        print(format_results(page_results))

        sleep(random() * .3 + .3)


def fetch_page(city, page):
    url = f"https://www.songkick.com/en/metro-areas/{city}?page={page}#metro-area-calendar"

    q = rq.get(url)
    doc = fromstring(q.content)
    doc.make_links_absolute(url)

    dates = doc.cssselect('li.event-listings-element')

    results = []

    for date_el in dates:
        date_info = date_el.cssselect('time')[0]
        dt = dt_parse(date_info.attrib['datetime'])

        link = date_el.cssselect('p.artists a.event-link')[0]

        title = link.text_content().strip().replace('\n', ', ')
        while '  ' in title:
            title = title.replace('  ', ' ')
        url = link.attrib['href']

        results.append({
            'title': title,
            'link': link.attrib['href'],
            'dt': dt
        })

    return results


def format_results(results):
    result = u'\n'.join(
        [f"{item['title']}\n    {item['link']}\n    {item['dt']:%Y %b %d}\n"
        for item in results]
    )

    return result


def main():
    city = sys.argv[1]

    results = print_city(city)


if __name__ == '__main__':
    main()
