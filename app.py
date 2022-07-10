import time
import requests
import validators
import re
from bs4 import BeautifulSoup


def parse_main(input_link, header):
    html_content = requests.get(input_link, header)
    soup = BeautifulSoup(html_content.content, 'html.parser')
    for link in soup.find_all('a'):
        temp_link = link.get('href')
        print('Link: ', temp_link)
        if not temp_link:
            continue
        if (('government_moscow.tilda.ws' in temp_link) or ('css-mosreg.online' in temp_link))\
                and (temp_link not in url_list) and ('#' not in temp_link):
            url_list.append(temp_link)
        if ('google.com' in temp_link) and (temp_link not in url_list):
            url_list.append(temp_link)
        if ('/' in temp_link) and (temp_link not in url_list) and ('http' not in temp_link):
            # you can add your unique url here, or write new logic
            url_list.append('http://frontside.ru' + temp_link)
        time.sleep(1)
    return print(f'[INFO] -- parse_main -- function result:\n URLS:\n    {url_list}\n Titles:\n    {title_list}')


def prase_urls(urls_list, header):
    for element in urls_list:
        html_content = requests.get(element, header)
        soup = BeautifulSoup(html_content.content, 'html.parser')
        title_list.append(soup.title.text)
    return print(f'[INFO] -- prase_urls -- function result:\nTitles:\n    {title_list}')


def parse_exceptions(exceptions, header):
    html_content = requests.get(exceptions, header)
    soup = BeautifulSoup(html_content.text, 'html.parser')
    for link in soup.find_all('a'):
        temp_link = link.get('href')
        if not temp_link:
            continue
        if 'page' in temp_link:
            url_list.append('https://css-mosreg.online' + temp_link)
    return print(f'[INFO] -- parse_exceptions -- function results:\n    URLS: {url_list}!')



def parse_content(urls, header, file):
    for element in urls:
        html_content = requests.get(element, header)
        soup = BeautifulSoup(html_content.text, 'html.parser')
        for link in soup.find(string=re.compile("rec")):

    return print(f'[INFO] -- parse_content -- function results:\n    !FILE WRITTEN!')


if __name__ == '__main__':
    url_list = []
    title_list = []
    content_text = open('contentText.txt', 'w')
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headsers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0'
    }
    url = input('Enter url for parsing: \n')  # code was written for url's - http://frontside.ru/, https://css-mosreg.online, https://google.com
    if validators.url(url):
        parse_main(url, headers)
        proceed = str(input('Is there any exceptions? (y/n): '))
        if proceed[0].lower() == 'y':
            exception_url = input('Enter url...')
            print('[INFO] Running...')
            parse_exceptions(exception_url, headers)
            prase_urls(url_list, headers)
            parse_content(url_list, headers, content_text)
        else:
            prase_urls(url_list, headers)
            parse_content(url_list, headers, content_text)
            print('[INFO] Running...')
    else:
        print(f'{url} is wrong value\nShutting down... :(')
