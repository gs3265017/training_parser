import time
import requests
import validators
from bs4 import BeautifulSoup


def parseMain(input_link, header):
    """parsing list of collectetd urls from the main page"""
    html_content = requests.get(input_link, header)
    soup = BeautifulSoup(html_content.content, 'html.parser')
    for link in soup.find_all('a'):
        temp_link = link.get('href')
        print('Link: ', temp_link)
        if not temp_link:
            continue
        # hardcoded logic for websites :)
        if (('government_moscow.tilda.ws' in temp_link) or ('css-mosreg.online' in temp_link)) and (temp_link not in url_list) and ('#' not in temp_link):
            url_list.append(temp_link)
        if ('google.com' in temp_link) and (temp_link not in url_list):
            url_list.append(temp_link)
        if ('/' in temp_link) and (temp_link not in url_list) and ('http' not in temp_link):
            # you can add your unique url here, or write new logic
            url_list.append('http://frontside.ru' + temp_link)
        time.sleep(1)
    return print(f'[INFO] -- parse_main -- function result:\n URLS: \n {url_list}\n Titles: \n {title_list}')


def parseUrls(urls_list, header):
    """parsing list of collectetd urls from the main page"""
    for element in urls_list:
        html_content = requests.get(element, header)
        soup = BeautifulSoup(html_content.content, 'html.parser')
        title_list.append(soup.title.text)
    return print(f'[INFO] -- parse_urls -- function result:\n Titles: \n {title_list}')


def parseExceptions(exceptions, header):
    """parses unique links, that can hold bunch of urls, that was not getted with parseMain()"""
    html_content = requests.get(exceptions, header)
    soup = BeautifulSoup(html_content.text, 'html.parser')
    for link in soup.find_all('a'):
        temp_link = link.get('href')
        if not temp_link:
            continue
        if 'page' in temp_link:
            url_list.append('https://css-mosreg.online' + temp_link)


def parseContent(urls, header):
    """ parses content from all collected links"""
    for element in urls:
        html_content = requests.get(element, header)
        soup = BeautifulSoup(html_content.text, 'html.parser')
        print(soup.get_text())
    return print(f'-- parse_urls -- function result:\n Titles: \n {title_list}')


if __name__ == '__main__':
    url_list = []
    title_list = []
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headsers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0'
    }
    url = input('Enter url for parsing: \n')  # enter your url here, code was written for url's - http://frontside.ru/, https://css-mosreg.online, https://google.com
    if validators.url(url):
        parseMain(url, headers)
        proceed = str(input('Is there any exceptions? (y/n): '))
        if proceed[0].lower() == 'y':
            exception_url = input('Enter url...')
            print('[INFO] Running...')
            parseExceptions(exception_url, headers)
            parseUrls(url_list, headers)
            parseContent(url_list, headers)
        else:
            parseUrls(url_list, headers)
            parseContent(url_list, headers)
            print('[INFO] Running...')
    else:
        print(f'{url} is wrong value\nShutting down... :(')
