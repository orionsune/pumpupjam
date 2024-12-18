import time
import mpv
import board
import threading
import neopixel
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import simpleaudio as sa
from rpi_ws281x import *
import argparse

# Create a sound object
# wave_object = sa.WaveObject.from_wave_file("/home/pi/sample.wav")
# Init the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
# Init an ADS1115 object
ads = ADS.ADS1115(i2c)
# Init the analog sensor input channel
channel0 = AnalogIn(ads, ADS.P0)
# Init the neopixel matrix panel.
pixels1 = neopixel.NeoPixel(board.D12, 256, brightness=0.5, auto_write=False)
# defines the media player to use mpv
player = mpv.MPV()
# Init some variables
pressure = 0
playidle = True
speed = 1

LED_COUNT = 256  # how many LEDs are in the panel
LED_PIN = 12  # which pin on the raspberry pi to use
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 165  # Set to 0 for darkest and 255 for brightest
LED_INVERT = True  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
strip = Adafruit_NeoPixel(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
)
strip.begin()

# defines a framebuffer neopixel object for use with displaying text on the panel
from adafruit_pixel_framebuf import PixelFramebuffer

pixel_pin = board.D12
pixel_width = 32
pixel_height = 8
pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height,
    brightness=0.5,
    auto_write=False,
)
pixel_framebuf = PixelFramebuffer(pixels, 32, 8, orientation=0, rotation=0)


# generate colors based on position for progress bar rainbow.
# Generates rainbow colors in tuples based on a column's position in the matrix panel
# The tuples represent (R, G, B) with values from 0 to 255.
def wheel(pos):
    if pos < 85:  # hereisone
        return (pos * 3, 255 - pos * 3, 0)  # Generate a red-yellow color
    elif pos < 170:  # hereisone
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)  # Generate a yellow-green color
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)  # Generate a green-blue color


# generate colors for the theaterchase animation
def wheelchase(pos):
    if pos < 85:  # hereisone
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:  # hereisone
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


# turn LED columns on or off
def col(position, color1, color2, color3):
    for i in range(8):
        pixels1[position] = (color1, color2, color3)
        position += 1
    pixels1.show()


# pressure checking for each LED column
# fills up the strip column by column based on "pressure" readings
def pressurecheck():
    if pressure >= 10:
        color = wheel(0)
        col(0, color[0], color[1], color[2])
    elif pressure < 10:
        col(0, 0, 0, 0)

    if pressure <= 10 and pressure >= 0:
        if playidle == False:
            player.speed = 0.3

    if pressure >= 20:
        color = wheel(8)
        col(8, color[0], color[1], color[2])
    elif pressure < 20:
        col(8, 0, 0, 0)

    if pressure <= 20 and pressure >= 10:
        if playidle == False:
            player.speed = 0.4

    if pressure >= 30:
        color = wheel(16)
        col(16, color[0], color[1], color[2])
    elif pressure < 30:
        col(16, 0, 0, 0)

    if pressure <= 30 and pressure >= 20:
        if playidle == False:
            player.speed = 0.4

    if pressure >= 40:
        color = wheel(24)
        col(24, color[0], color[1], color[2])
    elif pressure < 40:
        col(24, 0, 0, 0)

    if pressure <= 40 and pressure >= 30:
        if playidle == False:
            player.speed = 0.5

    if pressure >= 50:
        color = wheel(32)
        col(32, color[0], color[1], color[2])
    elif pressure < 50:
        col(32, 0, 0, 0)

    if pressure <= 50 and pressure >= 40:
        if playidle == False:
            player.speed = 0.5

    if pressure >= 60:
        color = wheel(40)
        col(40, color[0], color[1], color[2])
    elif pressure < 60:
        col(40, 0, 0, 0)

    if pressure <= 60 and pressure >= 50:
        if playidle == False:
            player.speed = 0.5

    if pressure >= 70:
        color = wheel(48)
        col(48, color[0], color[1], color[2])
    elif pressure < 70:
        col(48, 0, 0, 0)

    if pressure <= 70 and pressure >= 60:
        if playidle == False:
            player.speed = 0.6

    if pressure >= 80:
        color = wheel(56)
        col(56, color[0], color[1], color[2])
    elif pressure < 80:
        col(56, 0, 0, 0)

    if pressure <= 10 and pressure >= 0:
        if playidle == False:
            player.speed = 0.5

    if pressure >= 90:
        color = wheel(64)
        col(64, color[0], color[1], color[2])
    elif pressure < 90:
        col(64, 0, 0, 0)

    if pressure <= 90 and pressure >= 80:
        if playidle == False:
            player.speed = 0.55

    if pressure >= 100:
        color = wheel(72)
        col(72, color[0], color[1], color[2])
    elif pressure < 100:
        col(72, 0, 0, 0)

    if pressure <= 100 and pressure >= 90:
        if playidle == False:
            player.speed = 0.55

    if pressure >= 110:
        color = wheel(80)
        col(80, color[0], color[1], color[2])
    elif pressure < 110:
        col(80, 0, 0, 0)

    if pressure <= 110 and pressure >= 100:
        if playidle == False:
            player.speed = 0.58

    if pressure >= 120:
        color = wheel(88)
        col(88, color[0], color[1], color[2])
    elif pressure < 120:
        col(88, 0, 0, 0)

    if pressure <= 120 and pressure >= 110:
        if playidle == False:
            player.speed = 0.58

    if pressure >= 130:
        color = wheel(96)
        col(96, color[0], color[1], color[2])
    elif pressure < 130:
        col(96, 0, 0, 0)

    if pressure <= 130 and pressure >= 120:
        if playidle == False:
            player.speed = 0.58

    if pressure >= 140:
        color = wheel(104)
        col(104, color[0], color[1], color[2])
    elif pressure < 140:
        col(104, 0, 0, 0)

    if pressure <= 140 and pressure >= 130:
        if playidle == False:
            player.speed = 0.61

    if pressure >= 150:
        color = wheel(112)
        col(112, color[0], color[1], color[2])
    elif pressure < 150:
        col(112, 0, 0, 0)

    if pressure <= 150 and pressure >= 140:
        if playidle == False:
            player.speed = 0.61

    if pressure >= 160:
        color = wheel(120)
        col(120, color[0], color[1], color[2])
    elif pressure < 160:
        col(120, 0, 0, 0)

    if pressure <= 160 and pressure >= 150:
        if playidle == False:
            player.speed = 0.61

    if pressure >= 170:
        color = wheel(128)
        col(128, color[0], color[1], color[2])
    elif pressure < 170:
        col(128, 0, 0, 0)

    if pressure <= 170 and pressure >= 160:
        if playidle == False:
            player.speed = 0.64

    if pressure >= 180:
        color = wheel(136)
        col(136, color[0], color[1], color[2])
    elif pressure < 180:
        col(136, 0, 0, 0)

    if pressure <= 180 and pressure >= 170:
        if playidle == False:
            player.speed = 0.64

    if pressure >= 190:
        color = wheel(144)
        col(144, color[0], color[1], color[2])
    elif pressure < 190:
        col(144, 0, 0, 0)

    if pressure <= 190 and pressure >= 180:
        if playidle == False:
            player.speed = 0.64

    if pressure >= 200:
        color = wheel(152)
        col(152, color[0], color[1], color[2])
    elif pressure < 200:
        col(152, 0, 0, 0)

    if pressure <= 200 and pressure >= 190:
        if playidle == False:
            player.speed = 0.67

    if pressure >= 210:
        color = wheel(160)
        col(160, color[0], color[1], color[2])
    elif pressure < 210:
        col(160, 0, 0, 0)

    if pressure <= 210 and pressure >= 200:
        if playidle == False:
            player.speed = 0.7

    if pressure >= 220:
        color = wheel(168)
        col(168, color[0], color[1], color[2])
    elif pressure < 220:
        col(168, 0, 0, 0)

    if pressure <= 220 and pressure >= 210:
        if playidle == False:
            player.speed = 0.73

    if pressure >= 230:
        color = wheel(176)
        col(176, color[0], color[1], color[2])
    elif pressure < 230:
        col(176, 0, 0, 0)

    if pressure <= 230 and pressure >= 220:
        if playidle == False:
            player.speed = 0.76

    if pressure >= 240:
        color = wheel(184)
        col(184, color[0], color[1], color[2])
    elif pressure < 240:
        col(184, 0, 0, 0)

    if pressure <= 240 and pressure >= 230:
        if playidle == False:
            player.speed = 0.79

    if pressure >= 250:
        color = wheel(192)
        col(192, color[0], color[1], color[2])
    elif pressure < 250:
        col(192, 0, 0, 0)

    if pressure <= 250 and pressure >= 240:
        if playidle == False:
            player.speed = 0.82

    if pressure >= 260:
        color = wheel(200)
        col(200, color[0], color[1], color[2])
    elif pressure < 260:
        col(200, 0, 0, 0)

    if pressure <= 260 and pressure >= 250:
        if playidle == False:
            player.speed = 0.85

    if pressure >= 270:
        color = wheel(208)
        col(208, color[0], color[1], color[2])
    elif pressure < 270:
        col(208, 0, 0, 0)

    if pressure <= 270 and pressure >= 260:
        if playidle == False:
            player.speed = 0.88

    if pressure >= 280:
        color = wheel(216)
        col(216, color[0], color[1], color[2])
    elif pressure < 280:
        col(216, 0, 0, 0)

    if pressure <= 280 and pressure >= 270:
        if playidle == False:
            player.speed = 0.91

    if pressure >= 290:
        color = wheel(224)
        col(224, color[0], color[1], color[2])
    elif pressure < 290:
        col(224, 0, 0, 0)

    if pressure <= 290 and pressure >= 280:
        if playidle == False:
            player.speed = 0.94

    if pressure >= 300:
        color = wheel(232)
        col(232, color[0], color[1], color[2])
    elif pressure < 300:
        col(232, 0, 0, 0)

    if pressure <= 300 and pressure >= 290:
        if playidle == False:
            player.speed = 0.97

    if pressure >= 310:
        color = wheel(240)
        col(240, color[0], color[1], color[2])
    elif pressure < 310:
        col(240, 0, 0, 0)

    if pressure <= 310 and pressure >= 300:
        if playidle == False:
            player.speed = 1

    if pressure >= 320:
        color = wheel(248)
        col(248, color[0], color[1], color[2])
    elif pressure < 320:
        col(248, 0, 0, 0)

    if pressure >= 320:
        if playidle == False:
            player.speed = 1


# display Pump! on the LED panel
def precheck():
    pixel_framebuf.text("Pump!", 3, 0, 0x00FF00)
    pixel_framebuf.display()


# gets the idle property from the player
# detects if the player is idle (True) or playing a track (False)
def getprop(playidle):
    @player.property_observer("idle-active")
    def playcheck(property_name, isplaying):
        # print(isplaying)
        global playidle
        playidle = isplaying


# plays the track
def playsong():
    player.play("/home/pi/pumpupjamshort.mp3")
    # player.wait_for_playback()


# make theaterchase animation while track plays and pressure is above threshold
def rainbowchase():
    while True:
        getprop(playidle)
        if playidle == False and pressure > 320:
            theaterChaseRainbow(strip)


# stolen demo code generates rainbow flashing patterns
def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(16):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheelchase((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


# starting the track animoation monitor thread
rainbowthread = threading.Thread(target=rainbowchase)
rainbowthread.start()


# my attempt at integrating all the functions together
while True:
    getprop(playidle)
    print(playidle)
    pressure = int(input("Simulated Pressure [0-321]: "))
    if pressure < 10 and playidle == False:
        player.stop()
        player.speed = 1  # reset speed to 1 for next play
    if pressure < 10 and playidle == True:
        precheck()  # display Pump! on the LED display
    if pressure > 10 and playidle == True:
        pressurecheck()  # run the pressure check function
    if pressure > 320 and playidle == True:
        playsong()  # play song when full
    if pressure <= 320 and playidle == False:
        pressurecheck()  # run the progress bar decrease function
    if pressure >= 320 and playidle == False:
        player.speed = 1
