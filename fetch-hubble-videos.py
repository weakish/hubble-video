#!/usr/bin/env python2.7

# by Jakukyo Friel <weakish@gmail.com>
# under Apache License, Version 2.0, <http://www.apache.org/licenses/LICENSE-2.0.html>


from urllib2 import urlopen
from lxml.html import fromstring


def get_page(url):
  html = urlopen(url).read()
  page = fromstring(html)
  page.make_links_absolute(url)
  return page


def get_index_urls(url):
  index_page = get_page(url)
  links = index_page.cssselect('table.archive_normal a')
  urls = [link.attrib['href'] for link in links]
  return urls


def build_video_page_list():
  base_url = 'http://www.spacetelescope.org/videos/page/'
  video_page_list = []
  for i in range(1,19):
    url = base_url + str(i) + '/'
    urls = get_index_urls(url)
    video_page_list.extend(urls)
  return video_page_list


def get_video_download_url(url):
  video_page = get_page(url)
  links = video_page.cssselect('#rightcolumn div.archive_download span.archive_dl_text a')
  download_urls = [link.attrib['href'] for link in links]
  fullhd_url = [url for url in download_urls if 'hd_1080p25_screen' in url]
  return fullhd_url

def build_video_download_list():
  video_urls = [get_video_download_url(page) for page in build_video_page_list()]
  return video_urls


def main():
  video_urls = build_video_download_list()
  print(video_urls)

if __name__ == '__main__':
  main()
