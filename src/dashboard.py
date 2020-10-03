"""
Builds dashboard images for eink display
"""

from PIL import Image, ImageDraw, ImageFont
# from .main import epd
from .config import Config

config = Config()

# data = {
#     "up": {
#         "arr": [10, 20, 30, 40, 50, 40, 30, 20, 10],
#         "max": 120.1234,
#         "avg": 100.9999,
#         "min": 70.5432,
#     },
#     "down": {
#         "arr": [10, 20, 30, 40, 50, 40, 30, 20, 10],
#         "max": 120.1234,
#         "avg": 100.9999,
#         "min": 70.5432,
#     }
# }


class Dashboard():
    """
    Handles creating the images for the display.
    """
    # FONT_NAME = 'Gentium-R.ttf'  # Available on rasppi
    FONT_NAME = 'Courier New.ttf'  # Available on macos

    def __init__(self, epd=None):
        self.height = 298  # epd.height
        self.width = 126  # epd.width
        self.font = ImageFont.truetype(self.FONT_NAME, 10)
        self.HBlackimage = Image.new('1', (self.height, self.width), 255)
        self.HRYimage = Image.new('1', (self.height, self.width), 255)
        self.drawblack = ImageDraw.Draw(self.HBlackimage)
        self.drawry = ImageDraw.Draw(self.HRYimage)

    def __add_dash_text(self, data: dict):
        """
        Text for expected download/upload and min/max
        """
        height_offset1 = 2*self.height/3
        height_offset2 = 2*self.height/3 + 10
        download_messages = [
            {  # Download Expected
                "xy": (height_offset1, 5),
                "text": f"Down: {config.expected_download}",
            },
            {  # Download Max
                "xy": (height_offset2, 20),
                "text": f"Max: {data['down']['max']:>6.2f}",
            },
            {  # Download Avg
                "xy": (height_offset2, 35),
                "text": f"Avg: {data['down']['avg']:>6.2f}",
            },
            {  # Download Min
                "xy": (height_offset2, 50),
                "text": f"Min: {data['down']['min']:>6.2f}",
            },
        ]
        upload_messages = [
            {  # Upload Expected
                "xy": (height_offset1, 70),
                "text": f"Up: {config.expected_upload}",
            },
            {  # Upload Max
                "xy": (height_offset2, 85),
                "text": f"Max: {data['up']['max']:>6.2f}",
            },
            {  # Upload Avg
                "xy": (height_offset2, 100),
                "text": f"Avg: {data['up']['avg']:>6.2f}",
            },
            {  # Upload Min
                "xy": (height_offset2, 115),
                "text": f"Min: {data['up']['min']:>6.2f}",
            },
        ]
        for line in download_messages:
            self.drawblack.text(font=self.font, fill=0, **line)
        for line in upload_messages:
            self.drawblack.text(font=self.font, fill=0, **line)

    def __add_dash_graph(self, data: dict):
        """
        Graph for archived values
        """
        rect_xy = (
            (5, 5),
            (2*self.height/3-5, self.width-5)
        )
        self.drawblack.rectangle(
            xy=rect_xy,
            outline=0
        )
        # bar0 = 0
        # bar100 = rect_xy[1][0] - rect_xy[0][0]
        # barwid = 5

    def build_dashboard(self, data: dict):
        """
        Builds and exports the images
        """
        self.clear()
        self.__add_dash_text(data)
        self.__add_dash_graph(data)
        return self.HBlackimage, self.HRYimage

    def show(self):
        """
        Shows the images, for testing purposes
        """
        self.HBlackimage.show()
        self.HRYimage.show()

    def clear(self):
        """
        Resets the screen to white
        """
        for image in [self.drawblack, self.drawry]:
            image.rectangle(
                xy=((0, 0), (self.height, self.width)),
                fill=255
            )

# Reset Screen
# HBlackimage.show()
# drawblack.rectangle(xy=((0, 0), (HEIGHT, WIDTH)), fill=255)
