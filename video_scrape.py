from bs4 import BeautifulSoup as bs
import sys
import os
import requests
from pytube import YouTube
import logging
import pdb

# Video Scraper for YouTube
# scrapes all videos on front page for a search query
# search given as command line argument

# USAGE
# One url:
# python3 video_scrape.py <url>
# Multiple urls:
# python3 video_scrape.py <url1> <url2> ...
# YouTube search query
# python3 video_scrape.py <search query>

# Program settings
logging.basicConfig(level=logging.INFO)
only_video = False
max_res = 720

# pytube stream object does not have a get resolution function
def get_resolution(stream):
    try:
        s = str(stream)
        logging.debug(s)
        s = s.split('res="')[1]
        s = s.split('p')[0]
        return int(s)
    except:
        return 0

def scrape_from_url(video_url):
    try:
        logging.info('Downloading video:')
        yt = YouTube(video_url)
        if only_video:
            streams = yt.streams.filter(adaptive=True, file_extension = 'mp4').all()
        else:
            streams = yt.streams.filter(progressive=True, file_extension = 'mp4').all()
        high_res = 0
        stream = streams[0]
        # download video with highest res
        for s in streams:
            resolution = get_resolution(s)
            if (resolution > high_res and resolution <= max_res):
                high_res = get_resolution(s)
                stream = s
        logging.info(video_url)
        stream.download()
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)


def scrape_from_search(search_text):
    logging.info('Scraping for query: %s' % search_text)
    url = "https://www.youtube.com/results?search_query=" + search_text.replace(' ', '+')
    response = requests.get(url)
    html = response.content
    soup = bs(html, 'html.parser')
    urls = []
    # creates list of search results
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        end = vid['href']
        # only get urls for videos, not for channels or playlists
        if end[0:6] == '/watch':
            logging.debug(end)
            urls.append('https://www.youtube.com' + end)

    # for each video url, download in current directory
    for video_url in urls:
        scrape_from_url(video_url)


# Given search text, gets list of youtube videos
text = ' '.join(sys.argv[1:])
if text.find('youtube.com'):
    for i in range(1, len(sys.argv)):
        scrape_from_url(sys.argv[i])
else:
    scrape_from_search(text)
