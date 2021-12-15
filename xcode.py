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
DATA_SOURCE = "https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH,BTC,SOL,ALGO,AVAX,DOT&tsyms=USD"
DATA1_LOCATION = ["ETH", "USD"]
DATA2_LOCATION = ["BTC", "USD"]
DATA3_LOCATION = ["SOL", "USD"]
DATA4_LOCATION = ["ALGO", "USD"]
DATA5_LOCATION = ["AVAX", "USD"]
DATA6_LOCATION = ["DOT", "USD"]

#Set the pin for Battery
analog_in = AnalogIn(board.A1)


#----------------Functions--------------------

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def blink(color, duration):
    magtag.peripherals.neopixel_disable = False
    magtag.peripherals.neopixels.fill(color)
    time.sleep(duration)
    magtag.peripherals.neopixel_disable = True

def text_Current(val):
    return "$%g " % val + STOCK1

def text_High(val):
    return "$%g High" % val

def text_Low(val):
    return "$%g Low" % val

def text_Close(val):
    return "$%g PrvClose" % val

def text_transform1(val):
    return "$ETH: $%g" % val
def text_transform2(val):
    return "$BTC: $%g" % val
def text_transform3(val):
    return "$SOL: $%g" % val
def text_transform4(val):
    return "$ALGO: $%g" % val
def text_transform5(val):
    return "$AVAX: $%g" % val
def text_transform6(val):
    return "$DOT: $%g" % val

#Main
#Set Data

magtag = MagTag(
    url=DATA_SOURCE,
    json_path=(DATA1_LOCATION, DATA2_LOCATION, DATA3_LOCATION, DATA4_LOCATION, DATA5_LOCATION,DATA6_LOCATION),
)

magtag.network.connect()

magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        10,
    ),
    text_scale=2,
    text_transform=text_transform1,
    text_anchor_point=(0.5, 0.5),
)


magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        30,
    ),
    text_scale=2,
    text_transform=text_transform2,
    text_anchor_point=(0.5, 0.5),
)

magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        50,
    ),
    text_scale=2,
    text_transform=text_transform3,
    text_anchor_point=(0.5, 0.5),
)

magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        70,
    ),
    text_scale=2,
    text_transform=text_transform4,
    text_anchor_point=(0.5, 0.5),
)

magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        90,
    ),
    text_scale=2,
    text_transform=text_transform5,
    text_anchor_point=(0.5, 0.5),
)

magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        110,
    ),
    text_scale=2,
    text_transform=text_transform6,
    text_anchor_point=(0.5, 0.5),
)


#Go Get the Info
print("Fetchiing Data from JSON")

try:
    value = magtag.fetch()

    blink(GREEN, .8)

    print("Response is", value)
except (ValueError, RuntimeError) as e:
    print("Some error occured, retrying! -", e)
magtag.exit_and_deep_sleep(60)
