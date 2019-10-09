import sys
import os
import time
import cv2
import logging
import pdb
import pafy
from datetime import datetime
try:
    from vidgear.gears import CamGear
except:
    from vidgear.vidgear.gears import CamGear
# URL with setup directions:
# https://github.com/abhiTronix/vidgear/issues/16#issuecomment-495456217

# Video Scraper for Live YouTube
# search given as command line argument
# optional parameter - duration

# USAGE
# One url:
# python3 video_scrape.py <url> <seconds to record>

# Program settings
folder = 'videos/'

# ENCODING PARAMS
file_type = 'mp4'
codec = 'mp4v'
# AVI TYPE
# file_type = 'avi'
# codec = 'MJPG'

# FRAMES PER SECOND
fps = 40


def scrape_live(url, duration=60, show=False):
    # create pafy object. Just used to extract name of YouTube video
    pafy_vid = pafy.new(url)
    title = folder
    title += pafy_vid.title
    # cleanup title so nicer for video_naming
    title = title.replace(' ','-')
    title = title.replace('.', '')
    # get time
    now = datetime.now()
    # add time stamp
    title += now.strftime("-%m_%d_%Y-%H_%M_%S")
    file_name = title + '.' + file_type

    stream = CamGear(source=url, y_tube=True, time_delay=1, logging=True).start()
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(file_name, fourcc, fps, (1920, 1080))

    start = time.time()
    frames = 0
    while time.time() - start < duration:
        frame = stream.read()
        frames += 1
        out.write(frame)

        if frame is None:
            break

        if show:
            cv2.imshow('Output Frame', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    print(frames / (time.time() - start))
    if show:
        cv2.destroyAllWindows()
    stream.stop()
    out.release()

url = sys.argv[1]
duration = 60
if len(sys.argv) > 2:
    duration = int(sys.argv[2])
scrape_live(url, duration)
