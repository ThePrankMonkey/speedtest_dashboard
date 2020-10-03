import os
from PIL import Image, ImageDraw, ImageFont
# from .main import epd
from .config import Config

config = Config()
# Height and Width are swapped in Waveshare example...
# HEIGHT = epd.height
# WIDTH = epd.width
HEIGHT = 298  # TODO Replace with derived values
WIDTH = 126  # TODO Replace with derived values
# FONT_NAME = 'Gentium-R.ttf'  # Available on rasppi
FONT_NAME = 'Courier New.ttf'  # Available on macos
font = ImageFont.truetype(FONT_NAME, 10)

data = {
    "up": {
        "arr": [10, 20, 30, 40, 50, 40, 30, 20, 10],
        "max": 120.1234,
        "avg": 100.9999,
        "min": 70.5432,
    },
    "down": {
        "arr": [10, 20, 30, 40, 50, 40, 30, 20, 10],
        "max": 120.1234,
        "avg": 100.9999,
        "min": 70.5432,
    }
}


def add_dash_text(drawblack, data):
    # Text for expected download/upload and min/max
    download_messages = [
        {  # Download Expected
            "xy": (2*HEIGHT/3, 5),
            "text": f"Down: {config.expected_download}",
        },
        {  # Download Max
            "xy": (2*HEIGHT/3+10, 20),
            "text": f"Max: {data['down']['max']:>6.2f}",
        },
        {  # Download Avg
            "xy": (2*HEIGHT/3+10, 35),
            "text": f"Avg: {data['down']['avg']:>6.2f}",
        },
        {  # Download Min
            "xy": (2*HEIGHT/3+10, 50),
            "text": f"Min: {data['down']['min']:>6.2f}",
        },
    ]
    upload_messages = [
        {  # Upload Expected
            "xy": (2*HEIGHT/3, 5),
            "text": f"Up: {config.expected_upload}",
        },
        {  # Upload Max
            "xy": (2*HEIGHT/3+10, 20),
            "text": f"Max: {data['up']['max']:>6.2f}",
        },
        {  # Upload Avg
            "xy": (2*HEIGHT/3+10, 35),
            "text": f"Avg: {data['up']['avg']:>6.2f}",
        },
        {  # Upload Min
            "xy": (2*HEIGHT/3+10, 50),
            "text": f"Min: {data['up']['min']:>6.2f}",
        },
    ]
    for line in download_messages:
        drawblack.text(font=font, fill=0, **line)
    for line in upload_messages:
        drawblack.text(font=font, fill=0, **line)
    return drawblack


def add_dash_graph(drawblack, drawry, data):
    # Graph for archived values
    rect_xy = (
        (5, 5),
        (2*HEIGHT/3-5, WIDTH-5)
    )
    drawblack.rectangle(
        xy=rect_xy,
        outline=0
    )
    bar0 = 0
    bar100 = rect_xy[1][0] - rect_xy[0][0]
    barwid = 5
    return drawblack, drawry


def build_dashboard(data: dict):
    HBlackimage = Image.new('1', (HEIGHT, WIDTH), 255)
    HRYimage = Image.new('1', (HEIGHT, WIDTH), 255)
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)
    drawblack = add_dash_text(drawblack, data)
    drawblack, drawry = add_dash_graph(drawblack, drawry, data)
    return drawblack, drawry


def show():
    HBlackimage.show()


def reset():
    drawblack.rectangle(xy=((0, 0), (HEIGHT, WIDTH)), fill=255)


def run(lines):
    for line in lines:
        drawblack.text(font=font, fill=0, **line)
# Reset Screen
# HBlackimage.show()
# drawblack.rectangle(xy=((0, 0), (HEIGHT, WIDTH)), fill=255)
