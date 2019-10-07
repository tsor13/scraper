import sys
import os
from vidgear.vidgear.gears import CamGear
import time
import cv2
import logging
import pdb

# Video Scraper for Live YouTube
# search given as command line argument
# optional parameter - duration

# USAGE
# One url:
# python3 video_scrape.py <url> <seconds to record>

# Program settings
# MP4 TYPE
output = 'video.mp4'
codec = 'mp4v'
# AVI TYPE
# output = 'video.avi'
# codec = 'MJPG'
fps = 40


def scrape_live(url, duration=60, show=False):
    stream = CamGear(source=url, y_tube=True, time_delay=1, logging=True).start()
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output, fourcc, fps, (1920, 1080))

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

# Given search text, gets list of youtube videos
url = sys.argv[1]
duration = 60
if len(sys.argv) > 2:
    duration = int(sys.argv[2])
scrape_live(url, duration)
