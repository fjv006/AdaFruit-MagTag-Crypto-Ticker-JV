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
DATA1_LOCATION  = ["RAW", "ETH" , "USD", "PRICE"]
DATA2_LOCATION  = ["RAW", "BTC" , "USD", "PRICE"]
DATA3_LOCATION  = ["RAW", "SOL" , "USD", "PRICE"]
DATA4_LOCATION  = ["RAW", "ALGO", "USD", "PRICE"]
DATA5_LOCATION  = ["RAW", "AVAX", "USD", "PRICE"]
DATA6_LOCATION  = ["RAW", "DOT" , "USD", "PRICE"]
DATA7_LOCATION  = ["RAW", "ETH" , "USD", "CHANGEPCTHOUR"]
DATA8_LOCATION  = ["RAW", "BTC" , "USD", "CHANGEPCTHOUR"]
DATA9_LOCATION  = ["RAW", "SOL" , "USD", "CHANGEPCTHOUR"]
DATA10_LOCATION = ["RAW", "ALGO", "USD", "CHANGEPCTHOUR"]
DATA11_LOCATION = ["RAW", "AVAX", "USD", "CHANGEPCTHOUR"]
DATA12_LOCATION = ["RAW", "DOT" , "USD", "CHANGEPCTHOUR"]

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
    return "$ETH:  $%8.2f" % val
def text_transform2(val):
    return "$BTC:  $%8.2f" % val
def text_transform3(val):
    return "$SOL:  $%8.2f" % val
def text_transform4(val):
    return "$ALGO: $%8.2f" % val
def text_transform5(val):
    return "$AVAX: $%8.2f" % val
def text_transform6(val):
    return "$DOT:  $%8.2f" % val
def text_transform7(val):
    return "%+4.2f%%" % val

#Main
#Set Data

magtag = MagTag(
    url=DATA_SOURCE,
    json_path=(DATA1_LOCATION, DATA7_LOCATION, DATA2_LOCATION, DATA8_LOCATION, DATA3_LOCATION, DATA9_LOCATION, DATA4_LOCATION,DATA10_LOCATION, DATA5_LOCATION,DATA11_LOCATION, DATA6_LOCATION,DATA12_LOCATION),
)

magtag.network.connect()

#ETH 

magtag.add_text(
    text_position=(
        0,
        10,
    ),
    text_scale=2,
    text_transform=text_transform1,
    text_anchor_point=(0, 0.5),
)

magtag.add_text(
    text_position=(
        magtag.graphics.display.width - 90,
        10,
    ),
    text_scale=2,
    text_transform=text_transform7,
    text_anchor_point=(0, 0.5),
)

#BTC

magtag.add_text(
    text_position=(
        0,
        30,
    ),
    text_scale=2,
    text_transform=text_transform2,
    text_anchor_point=(0, 0.5),
)

magtag.add_text(
    text_position=(
        magtag.graphics.display.width - 90,
        30,
    ),
    text_scale=2,
    text_transform=text_transform7,
    text_anchor_point=(0, 0.5),
)

#SOL

magtag.add_text(
    text_position=(
        0,
        50,
    ),
    text_scale=2,
    text_transform=text_transform3,
    text_anchor_point=(0, 0.5),
)

magtag.add_text(
    text_position=(
        magtag.graphics.display.width - 90,
        50,
    ),
    text_scale=2,
    text_transform=text_transform7,
    text_anchor_point=(0, 0.5),
)

#ALGO

magtag.add_text(
    text_position=(
        0,
        70,
    ),
    text_scale=2,
    text_transform=text_transform4,
    text_anchor_point=(0, 0.5),
)

magtag.add_text(
    text_position=(
        magtag.graphics.display.width - 90,
        70,
    ),
    text_scale=2,
    text_transform=text_transform7,
    text_anchor_point=(0, 0.5),
)


#AVAX

magtag.add_text(
    text_position=(
        0,
        90,
    ),
    text_scale=2,
    text_transform=text_transform5,
    text_anchor_point=(0, 0.5),
)

magtag.add_text(
    text_position=(
        magtag.graphics.display.width - 90,
        90,
    ),
    text_scale=2,
    text_transform=text_transform7,
    text_anchor_point=(0, 0.5),
)

#DOT

magtag.add_text(
    text_position=(
        0,
        110,
    ),
    text_scale=2,
    text_transform=text_transform6,
    text_anchor_point=(0, 0.5),
)

magtag.add_text(
    text_position=(
        magtag.graphics.display.width - 90,
        110,
    ),
    text_scale=2,
    text_transform=text_transform7,
    text_anchor_point=(0, 0.5),
)

#Go Get the Info
print("Fetching Data from JSON")

try:
    value = magtag.fetch()

    blink(GREEN, .8)

    print("Response is", value)
except (ValueError, RuntimeError) as e:
    print("Some error occured, retrying! -", e)
magtag.exit_and_deep_sleep(30)
