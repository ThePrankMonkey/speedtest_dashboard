# Eink Display Project

I have a WaveShare 2.13V3 eink hat. I want to use it to display speedtest results.

## Eink

### Setup for EInk

1. Enable SPI
   1. Run `sudo raspi-config`
      1. Enable the SPI interface.
   2. Reboot
2. Install the WaveShare EPaper module
   1. `git clone https://github.com/waveshare/e-Paper`
   2. Navigate into the rasppi folder
   3. `sudo python3 setup.py install`

### Using Eink

```python
import time
from PIL import Image
from waveshare_epd import epd2in13b_V3 as epdriver # Different boards need different imports
black = Image.open("2in13bc-b.bmp")
color = Image.open("2in13bc-ry.bmp")
epd = epdriver.EPD()
epd.init()
epd.Clear()
time.sleep(1)
epd.display(epd.getbuffer(black), epd.getbuffer(color))
epd.sleep()
epd.Dev_exit()
```

## Speedtest

### Setup Speedtest

`pip3 install speedtest-cli`

### Using Speedtest

```python
import speedtest
EXPECTED_UP = 100
EXPECTED_DOWN = 100

def get_speedtest() -> tuple:
    test = speedtest.Speedtest()
    test.download()
    test.upload()
    real_up = test.results.upload // 1024**2
    real_down = test.results.download // 1024**2

    percent_up = real_up/EXPECTED_UP
    percent_down = real_down/EXPECTED_DOWN
    return (percent_up, percent_down)
```

## Making Dashboard

### Dashboard Psuedocode

```plain
# Initialize empty dashboard
# Initialize eink
# Initialize records
# Loop
    # Grab current up/down
    # Update dashboard
    # Update eink
    # Wait
```

### Dashboard Mockup

```plain
___________________________________________________
|                                   UP (100 MB/S)  |
|                       o         MAX: 100 MB/s    |
|               o       o o   o   MIN: 100 MB/S    |
|               o o     o o o o     DOWN (100 MB/S)|
|   o   o       o o o   o o o o   MAX: 100 MB/s    |
| o o o o o o o o o o o o o o o   MIN: 100 MB/S    |
|__________________________________________________|
```

We have a graph of every download attempt