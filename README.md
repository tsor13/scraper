Before first use, run command:
    bash setup.sh

video_scrape.py - to scrape youtube videos
    One url:
        python3 video_scrape.py <url>
    Multiple urls:
        python3 video_scrape.py <url1> <url2>
    YouTube search query:
        python3 video_scrape.py <search query>

live_scrape.py - scrapes live youtube streams
    Must be run in the setup virtual environment. Before use, run:
        source env/bin/activate
    To scrape from url (optional parameter: duration-number of seconds to record, default 60):
        python3 live_scrape.py <url> <duration=60>
