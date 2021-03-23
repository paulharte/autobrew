import os

## System
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = ''.join(SRC_DIR.rsplit("autobrew", 1)).rstrip('\\/')


#User defined
APP_LOGGING_NAME = "autobrew"

MAX_TEMP_C = 25
MIN_TEMP_C = 23

SAMPLE_INTERVAL_SECONDS = 150

SMELLOSCOPE_OFFSET = 1.55

TWITTER_USER_TO_ALERT = "@paulmharte"
