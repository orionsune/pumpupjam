import time
import mpv
import board
import threading
import neopixel
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# import simpleaudio as sa
from rpi_ws281x import *
import argparse
import RPi.GPIO as GPIO

# import time
# import adafruit_hcsr04

# TRIG_PIN = 11  # Raspberry Pi GPIO pin connected to TRIG pin of ultrasonic sensor
# ECHO_PIN = 12  # Raspberry Pi GPIO pin connected to ECHO pin of ultrasonic sensor
# sonar = adafruit_hcsr 4.HCSR04(trigger_pin=board.D11, echo_pin=board.D12)  # Adjust pins
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(TRIG_PIN, GPIO.OUT)
# GPIO.setup(ECHO_PIN, GPIO.IN)

# Create a sound object
# wave_object = sa.WaveObject.from_wave_file("/home/pi/sample.wav")
# Init the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
# Init an ADS1115 object
ads = ADS.ADS1115(i2c)
# ads.gain = 0.6666666666666666
ads.gain = 2
# Init the analog sensor input channel
channel0 = AnalogIn(ads, ADS.P0)
# Init the neopixel matrix panel.
pixels1 = neopixel.NeoPixel(board.D18, 256, brightness=0.75, auto_write=False)
# defines the media player to use mpv
player = mpv.MPV()
# Init some variables
pressure = 0
playidle = True
speed = 1

LED_COUNT = 256  # how many LEDs are in the panel
LED_PIN = 18  # which pin on the raspberry pi to use
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 192  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
strip = Adafruit_NeoPixel(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
)
strip.begin()

# defines a framebuffer neopixel object for use with displaying text on the panel
from adafruit_pixel_framebuf import PixelFramebuffer

pixel_pin = board.D18
pixel_width = 32
pixel_height = 8
pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height,
    brightness=0.75,
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
    if pressure >= 9200:  # column 1
        color = wheel(0)
        col(0, color[0], color[1], color[2])
    elif pressure < 9200:
        col(0, 0, 0, 0)

    if pressure <= 9200 and pressure >= 0:
        player.speed = 0.3

    if pressure >= 9344:  # column 2
        color = wheel(8)
        col(8, color[0], color[1], color[2])
    elif pressure < 9344:
        col(8, 0, 0, 0)

    if pressure <= 9344 and pressure >= 9200:
        player.speed = 0.4

    if pressure >= 9688:  # column 3
        color = wheel(16)
        col(16, color[0], color[1], color[2])
    elif pressure < 9688:
        col(16, 0, 0, 0)

    if pressure <= 9688 and pressure >= 9344:
        player.speed = 0.4

    if pressure >= 10032:  # column 4
        color = wheel(24)
        col(24, color[0], color[1], color[2])
    elif pressure < 10032:
        col(24, 0, 0, 0)

    if pressure <= 10032 and pressure >= 9688:
        player.speed = 0.5

    if pressure >= 10376:  # column 5
        color = wheel(32)
        col(32, color[0], color[1], color[2])
    elif pressure < 10376:
        col(32, 0, 0, 0)

    if pressure <= 10376 and pressure >= 10032:
        player.speed = 0.5

    if pressure >= 10720:  # column 6
        color = wheel(40)
        col(40, color[0], color[1], color[2])
    elif pressure < 10720:
        col(40, 0, 0, 0)

    if pressure <= 10720 and pressure >= 10376:
        player.speed = 0.5

    if pressure >= 11064:  # column 7
        color = wheel(48)
        col(48, color[0], color[1], color[2])
    elif pressure < 11064:
        col(48, 0, 0, 0)

    if pressure <= 11064 and pressure >= 10720:
        player.speed = 0.5

    if pressure >= 11408:  # column 8
        color = wheel(56)
        col(56, color[0], color[1], color[2])
    elif pressure < 11408:
        col(56, 0, 0, 0)

    if pressure <= 11408 and pressure >= 11064:
        player.speed = 0.5

    if pressure >= 11752:  # column 9
        color = wheel(64)
        col(64, color[0], color[1], color[2])
    elif pressure < 11752:
        col(64, 0, 0, 0)

    if pressure <= 11752 and pressure >= 11408:
        player.speed = 0.55

    if pressure >= 12096:  # column 10
        color = wheel(72)
        col(72, color[0], color[1], color[2])
    elif pressure < 12096:
        col(72, 0, 0, 0)

    if pressure <= 12096 and pressure >= 11752:
        player.speed = 0.55

    if pressure >= 12440:  # column 11
        color = wheel(80)
        col(80, color[0], color[1], color[2])
    elif pressure < 12440:
        col(80, 0, 0, 0)

    if pressure <= 12440 and pressure >= 12096:
        player.speed = 0.58

    if pressure >= 12784:  # column 12
        color = wheel(88)
        col(88, color[0], color[1], color[2])
    elif pressure < 12784:
        col(88, 0, 0, 0)

    if pressure <= 12784 and pressure >= 12440:
        player.speed = 0.58

    if pressure >= 13128:  # column 13
        color = wheel(96)
        col(96, color[0], color[1], color[2])
    elif pressure < 13128:
        col(96, 0, 0, 0)

    if pressure <= 13128 and pressure >= 12784:
        player.speed = 0.58

    if pressure >= 13472:  # column 14
        color = wheel(104)
        col(104, color[0], color[1], color[2])
    elif pressure < 13472:
        col(104, 0, 0, 0)

    if pressure <= 13472 and pressure >= 13128:
        player.speed = 0.61

    if pressure >= 13816:  # column 15
        color = wheel(112)
        col(112, color[0], color[1], color[2])
    elif pressure < 13816:
        col(112, 0, 0, 0)

    if pressure <= 13816 and pressure >= 13472:
        player.speed = 0.61

    if pressure >= 14160:  # column 16
        color = wheel(120)
        col(120, color[0], color[1], color[2])
    elif pressure < 14160:
        col(120, 0, 0, 0)

    if pressure <= 14160 and pressure >= 13816:
        player.speed = 0.61

    if pressure >= 14504:  # column 17
        color = wheel(128)
        col(128, color[0], color[1], color[2])
    elif pressure < 14504:
        col(128, 0, 0, 0)

    if pressure <= 14504 and pressure >= 14160:
        player.speed = 0.64

    if pressure >= 14848:  # column 18
        color = wheel(136)
        col(136, color[0], color[1], color[2])
    elif pressure < 14848:
        col(136, 0, 0, 0)

    if pressure <= 14848 and pressure >= 14504:
        player.speed = 0.64

    if pressure >= 15192:  # column 19
        color = wheel(144)
        col(144, color[0], color[1], color[2])
    elif pressure < 15192:
        col(144, 0, 0, 0)

    if pressure <= 15192 and pressure >= 14848:
        player.speed = 0.64

    if pressure >= 15536:  # column 20
        color = wheel(152)
        col(152, color[0], color[1], color[2])
    elif pressure < 15536:
        col(152, 0, 0, 0)

    if pressure <= 15536 and pressure >= 15192:
        player.speed = 0.67

    if pressure >= 15880:  # column 21
        color = wheel(160)
        col(160, color[0], color[1], color[2])
    elif pressure < 15880:
        col(160, 0, 0, 0)

    if pressure <= 15880 and pressure >= 15536:
        player.speed = 0.7

    if pressure >= 16224:  # column 22
        color = wheel(168)
        col(168, color[0], color[1], color[2])
    elif pressure < 16224:
        col(168, 0, 0, 0)

    if pressure <= 16224 and pressure >= 15880:
        player.speed = 0.73

    if pressure >= 16568:  # column 23
        color = wheel(176)
        col(176, color[0], color[1], color[2])
    elif pressure < 16568:
        col(176, 0, 0, 0)

    if pressure <= 16568 and pressure >= 16224:
        player.speed = 0.76

    if pressure >= 16912:  # column 24
        color = wheel(184)
        col(184, color[0], color[1], color[2])
    elif pressure < 16912:
        col(184, 0, 0, 0)

    if pressure <= 16912 and pressure >= 16568:
        player.speed = 0.79

    if pressure >= 17256:  # column 25
        color = wheel(192)
        col(192, color[0], color[1], color[2])
    elif pressure < 17256:
        col(192, 0, 0, 0)

    if pressure <= 17256 and pressure >= 16912:
        player.speed = 0.82

    if pressure >= 17600:  # column 26
        color = wheel(200)
        col(200, color[0], color[1], color[2])
    elif pressure < 17600:
        col(200, 0, 0, 0)

    if pressure <= 17600 and pressure >= 17256:
        player.speed = 0.85

    if pressure >= 17944:  # column 27
        color = wheel(208)
        col(208, color[0], color[1], color[2])
    elif pressure < 17944:
        col(208, 0, 0, 0)

    if pressure <= 17944 and pressure >= 17600:
        player.speed = 0.88

    if pressure >= 18288:  # column 28
        color = wheel(216)
        col(216, color[0], color[1], color[2])
    elif pressure < 18288:
        col(216, 0, 0, 0)

    if pressure <= 18288 and pressure >= 17944:
        player.speed = 0.91

    if pressure >= 18632:  # column 29
        color = wheel(224)
        col(224, color[0], color[1], color[2])
    elif pressure < 18632:
        col(224, 0, 0, 0)

    if pressure <= 18632 and pressure >= 18288:
        player.speed = 0.94

    if pressure >= 18976:  # column 30
        color = wheel(232)
        col(232, color[0], color[1], color[2])
    elif pressure < 18976:
        col(232, 0, 0, 0)

    if pressure <= 18976 and pressure >= 18632:
        player.speed = 0.97

    if pressure >= 19320:  # column 31
        color = wheel(240)
        col(240, color[0], color[1], color[2])
    elif pressure < 19320:
        col(240, 0, 0, 0)

    if pressure <= 19320 and pressure >= 18976:
        player.speed = 1

    if pressure >= 19664:  # column 32
        color = wheel(248)
        col(248, color[0], color[1], color[2])
    elif pressure < 19664:
        col(248, 0, 0, 0)

    if pressure >= 19664:
        player.speed = 1


# display Pump! on the LED panel
def precheck():
    pixel_framebuf.text("Pump!", 3, 0, 0xCC00FF)
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
        if playidle == False and pressure > 19664:
            theaterChaseRainbow(strip)


# stolen demo code generates rainbow flashing patterns
def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(8):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheelchase((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


# starting the track animation monitor thread
rainbowthread = threading.Thread(target=rainbowchase)
rainbowthread.start()


def get_pressure():
    filter_array = []
    num_samples = 10

    # Taking multiple measurements and store in an array
    for _ in range(num_samples):
        filter_array.append(channel0.value)
        # time.sleep(0.03)  # To avoid ultrasonic interference (30 milliseconds delay)

    # Sorting the array in ascending order
    filter_array.sort()

    # Filtering noise
    # Discard the five smallest and five largest samples
    # filtered_samples = filter_array[6:-6]
    filtered_samples = filter_array[1:-5]
    # Calculate the average of the remaining samples
    pressure = int(sum(filtered_samples) / len(filtered_samples))

    return pressure


# my attempt at integrating all the functions together
while True:
    try:
        getprop(playidle)
        # pressure = channel0.value
        pressure = get_pressure() - 1100
        # print("Idle:", playidle)
        # print(pressure)
        # pressure = int(input("Simulated Pressure [0-321]: "))
        if pressure < 9199 and playidle == False:
            player.stop()
            # player.terminate()
            player.speed = 1  # reset speed to 1 for next play
        if pressure < 9199 and playidle == True:
            precheck()  # display Pump! on the LED display
        if pressure > 9199 and playidle == True:
            pressurecheck()  # run the pressure check function
        if pressure > 19664 and playidle == True:
            playsong()  # play song when full
        if pressure <= 19664 and playidle == False:
            pressurecheck()  # run the progress bar decrease function
        if pressure >= 19664 and playidle == False:
            player.speed = 1
    except RuntimeError:
        print("Retrying")
