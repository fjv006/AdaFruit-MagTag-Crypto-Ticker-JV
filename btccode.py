# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import terminalio
import neopixel
import alarm
import board
import json
import math

from adafruit_magtag.magtag import MagTag
from analogio import AnalogIn
from wakeful import store_data, load_data

#NeoPix Colors
RED = 0x880000
GREEN = 0x008800
BLUE = 0x000088
YELLOW = 0x884400
CYAN = 0x0088BB
MAGENTA = 0x9900BB
WHITE = 0x888888

SYNCHRONIZE_CLOCK = True

# Set up where we'll be fetching data from
DATA_SOURCE = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=ETH,BTC,SOL,ALGO,AVAX,DOT&tsyms=USD"
DATA_LOCATION = ["ETH", "USD", "PRICE"]

def text_transform1(val):
    return "$BTC: $%d" % val


magtag = MagTag(
    url=DATA_SOURCE,
    json_path=DATA_LOCATION,
)

magtag.network.connect()

magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        (magtag.graphics.display.height // 4) - 1,
    ),
    text_scale=2,
    text_transform=text_transform1,
    text_anchor_point=(0.5, 0.5),
)

try:
    value = magtag.fetch()
    print("Response is", value)
except (ValueError, RuntimeError) as e:
    print("Some error occured, retrying! -", e)
magtag.exit_and_deep_sleep(60)
