from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import psutil
import RPi.GPIO as GPIO
import time
from multiprocessing import Process


# import Adafruit_DHT


app = Flask(__name__)
    
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)


class Sensor(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    temperature = db.Column(db.String(100)) 
    humidity = db.Column(db.String(100)) 
    pressure = db.Column(db.String(100)) 
    light = db.Column(db.String(100))

def __init__(self, date, temperature, humidity, pressure, light):
   self.date = date
   self.temperature = temperature
   self.humidity = humidity
   self.pressure = pressure
   self.light = light


####SENSOR#####


import os
import socket
import RPi.GPIO as GPIO
import neopixel
import _rpi_ws281x as ws
from Tkinter import *
from lib_oled96 import ssd1306
from smbus2 import SMBus
i2cbus = SMBus(1)        # 1 = Raspberry Pi but NOT early REV1 board
oled = ssd1306(i2cbus)   # create oled object, nominating the correct I2C bus, default address
draw = oled.canvas
from PIL import ImageFont, ImageDraw, Image
font = ImageFont.load_default()

import smbus2
import Tkinter
import time
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte

# # settings for HTML webpage generation
# from mako.template import Template
# piftemplate = Template(filename='/var/www/html/template.txt')
# pifhtmlpage = '/var/www/html/cc.html'
# webtmpcolor = 'gray'

import datetime

DEVICE     = 0x23 # Default device I2C address Lightsensor
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
ONE_TIME_HIGH_RES_MODE = 0x20

bus = smbus2.SMBus(1)  # Rev 2 Pi uses 1
Seite=6
S1="offen"

file=("Wetterdaten_"+(time.strftime("%Y%m%d_%H%M%S",  time.localtime())))
Messzaeler =1

def getCPUtemperature():
	res = os.popen('vcgencmd measure_temp').readline()
	return(res.replace("temp=","").replace("'C\n",""))

def Volts():
	res = os.popen('vcgencmd measure_volts').readline()
	return(res.replace("volt=","").replace("V\n","")) 


def convertToNumber(data):
	# Simple function to convert 2 bytes of data
	# into a decimal number
	return ((data[1] + (256 * data[0])) / 1.2)

def readLight(addr=0x23):
	data = bus.read_i2c_block_data(addr, 0x20, 16)#ONE_TIME_HIGH_RES_MODE)
	return convertToNumber(data)
    


	
LED_COUNT = 4      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10       # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT =  False #True
LED_CHANNEL    = 0
LED_STRIP      =ws.WS2811_STRIP_RGB
strip = neopixel.Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()
# strip.setPixelColor(0, Color(0, 2, 0))
# strip.setPixelColor(1, Color(0, 2, 0))
# strip.setPixelColor(2, Color(0, 2, 0))
# strip.setPixelColor(3, Color(0, 2, 0))
strip.setPixelColorRGB(0, 100, 0, 0, 255)
strip.setPixelColorRGB(1, 0, 100, 0, 255)
strip.setPixelColorRGB(2, 0, 2, 100, 255)
strip.setPixelColorRGB(3, 100, 100, 100, 255)
strip.show()

	

DEVICE = 0x76 # Default device I2C address
bus = smbus2.SMBus(1) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
					# Rev 1 Pi uses bus
font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 15)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN,pull_up_down=GPIO.PUD_UP)

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# doesn't even have to be reachable
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	except:
		IP = '127.0.0.1'
	finally:
		s.close()   
	return IP     


def getShort(data, index):
	# return two bytes from data as a signed 16-bit value
	return c_short((data[index+1] << 8) + data[index]).value

def getUShort(data, index):
	# return two bytes from data as an unsigned 16-bit value
	return (data[index+1] << 8) + data[index]

def getChar(data,index):
	# return one byte from data as a signed char
	result = data[index]
	if result > 127:
		result -= 256
	return result

def getUChar(data,index):
	# return one byte from data as an unsigned char
	result =  data[index] & 0xFF
	return result

def readBME280ID(addr=DEVICE):
	# Chip ID Register Address
	REG_ID     = 0xD0
	(chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
	return (chip_id, chip_version)

def readBME280All(addr=DEVICE):
	# Register Addresses
	REG_DATA = 0xF7
	REG_CONTROL = 0xF4
	REG_CONFIG  = 0xF5

	REG_CONTROL_HUM = 0xF2
	REG_HUM_MSB = 0xFD
	REG_HUM_LSB = 0xFE

	# Oversample setting - page 27
	OVERSAMPLE_TEMP = 2
	OVERSAMPLE_PRES = 2
	MODE = 1

	# Oversample setting for humidity register - page 26
	OVERSAMPLE_HUM = 2
	bus.write_byte_data(addr, REG_CONTROL_HUM, OVERSAMPLE_HUM)

	control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
	bus.write_byte_data(addr, REG_CONTROL, control)

	# Read blocks of calibration data from EEPROM
	# See Page 22 data sheet
	cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
	cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
	cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)

	# Convert byte data to word values
	dig_T1 = getUShort(cal1, 0)
	dig_T2 = getShort(cal1, 2)
	dig_T3 = getShort(cal1, 4)

	dig_P1 = getUShort(cal1, 6)
	dig_P2 = getShort(cal1, 8)
	dig_P3 = getShort(cal1, 10)
	dig_P4 = getShort(cal1, 12)
	dig_P5 = getShort(cal1, 14)
	dig_P6 = getShort(cal1, 16)
	dig_P7 = getShort(cal1, 18)
	dig_P8 = getShort(cal1, 20)
	dig_P9 = getShort(cal1, 22)

	dig_H1 = getUChar(cal2, 0)
	dig_H2 = getShort(cal3, 0)
	dig_H3 = getUChar(cal3, 2)

	dig_H4 = getChar(cal3, 3)
	dig_H4 = (dig_H4 << 24) >> 20
	dig_H4 = dig_H4 | (getChar(cal3, 4) & 0x0F)

	dig_H5 = getChar(cal3, 5)
	dig_H5 = (dig_H5 << 24) >> 20
	dig_H5 = dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)

	dig_H6 = getChar(cal3, 6)

	# Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
	wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
	time.sleep(wait_time/1000)  # Wait the required time  

	# Read temperature/pressure/humidity
	data = bus.read_i2c_block_data(addr, REG_DATA, 8)
	pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
	temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
	hum_raw = (data[6] << 8) | data[7]

	#Refine temperature
	var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
	var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
	t_fine = var1+var2
	temperature = float(((t_fine * 5) + 128) >> 8);

	# Refine pressure and adjust for temperature
	var1 = t_fine / 2.0 - 64000.0
	var2 = var1 * var1 * dig_P6 / 32768.0
	var2 = var2 + var1 * dig_P5 * 2.0
	var2 = var2 / 4.0 + dig_P4 * 65536.0
	var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
	var1 = (1.0 + var1 / 32768.0) * dig_P1
	if var1 == 0:
		pressure=0
	else:
		pressure = 1048576.0 - pres_raw
		pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
		var1 = dig_P9 * pressure * pressure / 2147483648.0
		var2 = pressure * dig_P8 / 32768.0
		pressure = pressure + (var1 + var2 + dig_P7) / 16.0

	# Refine humidity
	humidity = t_fine - 76800.0
	humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
	humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
	if humidity > 100:
		humidity = 100
	elif humidity < 0:
		humidity = 0

	return temperature/100.0,pressure/100.0,humidity

def Standard1():
	TEM_MA.set(25),TEM_MI.set(3)
def Standard2():
	FT_MA.set(64),FT_MI.set(42)
def Standard3():
	LD_MA.set(1033),LD_MI.set(934)    
def Standard4():
	HL_TN.set(30)



def Taster():
	global Seite,S1
	if (GPIO.input(26) == False) and S1=="offen":
		Seite=Seite+1
		if Seite>8:
			Seite=1
		S1="gedrueckt"
	
	
	if (GPIO.input(26) == True):
		S1="offen"
	

	fenster.after(1, Taster) 

(chip_id, chip_version) = readBME280ID()
temperature,pressure,humidity = readBME280All()
lichtstaerke = readLight()


def main():
	global Seite,Messzaeler
	(chip_id, chip_version) = readBME280ID()
	temperature,pressure,humidity = readBME280All()
	lichtstaerke = readLight()
	Temperatur = ("Temperatur: %4.1f C" % (temperature))
	Feuchte = ("Rel.Feuchte: %4.1f" % (humidity)+" %")
	Luftdruck = ("Luftdruck:%6.1f hPa" % (pressure)) 
	Lichtstaerke = ("Lichtst.: %6.1f" % (lichtstaerke)+" lux")


	if Seite==1: # Uebersicht
		draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)
		font = ImageFont.load_default()
		draw.text((5, 5), Temperatur , font=font, fill=1)
		draw.text((5, 20), Feuchte, font=font, fill=1)
		draw.text((5, 35), Luftdruck, font=font, fill=1)
		draw.text((5, 50), Lichtstaerke, font=font, fill=1)
		
	if Seite==2:   # Temperatur
		draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)
		font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 18)
		draw.text((16, 0), 'Temperatur' , font=font, fill=1)
		draw.text((40, 30),("%4.1f C" % (temperature)),font=font, fill=1)    
		
	if Seite==3:  # Feuchte 
		draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)
		font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 18)
		draw.text((16, 0), 'Rel.Feuchte' , font=font, fill=1)
		draw.text((30, 30), ("%4.1f" % (humidity)+" %") ,font=font, fill=1)
		
	if Seite==4:   # Luftdruck
		draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)
		font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 18)
		draw.text((18, 0), 'Luftdruck' , font=font, fill=1)
		draw.text((10, 30), ("%6.1f hPa" % (pressure)) ,font=font, fill=1)    
		
	if Seite==5:  # Helligkeit 
		draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)
		font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 14)
		draw.text((13, 0), 'Lichtstaerke' , font=font, fill=1)
		draw.text((12, 30), ("%6.1f" % (lichtstaerke)+" lux") ,font=font, fill=1)         
		
	if Seite==6:   # IP-Adresse
		IP=get_ip()
		draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)
		font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 12)
		draw.text((22, 3), 'IP-Adresse' , font=font, fill=1)
		draw.text((6, 30), IP, font=font, fill=1)
		oled.display()   

	if Seite==7:       # Logo LGK 
		draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)
		logo = Image.open('/home/pi/Desktop/RaspiMacedoPIF/logoltam.png')
		draw.bitmap((1, 0), logo, fill=1)
		
	if Seite==8:    # Projektdaten  
		draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)
		font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 12)
		font1 = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 14)
		draw.text((23, 4), 'LAM-Macedo' , font=font, fill=1)
		draw.text((11, 20), 'DAP PIF 2020-21' , font=font, fill=1)
		draw.text((8, 36), 'Wetterstation' , font=font1, fill=1)
	
	

	oled.display()   

	TemperaturWert.config(text="%.2f" % temperature+" C")
	LuftdruckWert.config(text="%.1f" % pressure+" hPa")
	FeuchteWert.config(text="%.1f" % humidity+" %")
	HellWert.config(text="%.1f" % lichtstaerke + " lux")

# with open((file)+".txt", "a") as f:
#         mytimestamp=datetime.datetime.now()
#         f.write(mytimestamp.strftime("%Y%m%d_%H%M%S"+"   "))
#         f.write("%5.0f" % Messzaeler+"   ")
#         f.write("%.2f" % temperature+"C   ")
#         f.write("%.1f" % humidity+"%  ")
#         f.write("%.1f" % pressure+"hPa   ")
#         #f.write("%.1f" % lichtstaerke + "lux\n")  
	Messzaeler=Messzaeler+1

#CPU_t.config(text="CPU %.2f" % (float(getCPUtemperature())) + " C / "+"%.1f" % (float(Volts())) + " v")

	Helligkeit=LED.get()


	if temperature > (TEM_MA.get()) or temperature < (TEM_MI.get()):
		strip.setPixelColorRGB(0, Helligkeit, 0, 0, 255)
		# strip.setPixelColor(0, Color(Helligkeit, 0, 0))
		LED1.config(bg='red')
		# webtmpcolor="red" # configure color for webdisplay
	else:
		strip.setPixelColorRGB(0, 0, Helligkeit, 0, 255)
		# strip.setPixelColor(0, Color(0, Helligkeit, 0))
		LED1.config(bg='green')
		# webtmpcolor="green" # configure color for webdisplay

	if humidity > (FT_MA.get()) or humidity < (FT_MI.get()):
		strip.setPixelColorRGB(1, Helligkeit, 0, 0, 255)
		# strip.setPixelColor(1, Color(Helligkeit, 0, 0))
		LED2.config(bg='red')
		# webhumicolor="red" # configure color for webdisplay
	else:
		strip.setPixelColorRGB(1, 0, Helligkeit, 0, 255)
		# strip.setPixelColor(1, Color(0, Helligkeit, 0))
		LED2.config(bg='green')
		# webhumicolor="green" # configure color for webdisplay
		
	if pressure > (LD_MA.get()) or pressure < (LD_MI.get()):
		strip.setPixelColorRGB(2, Helligkeit, 0, 0, 255)
		# strip.setPixelColor(2, Color(Helligkeit, 0, 0))
		LED3.config(bg='red')
		# webpressurecolor="red" # configure color for webdisplay
	else:
		strip.setPixelColorRGB(2, 0, Helligkeit, 0, 255)
		# strip.setPixelColor(2, Color(0, Helligkeit, 0))
		LED3.config(bg='green')     
		# webpressurecolor="green" # configure color for webdisplay
		
		
	if lichtstaerke > (HL_TN.get()):
		strip.setPixelColorRGB(3, Helligkeit, Helligkeit, 0, 255) 
		# strip.setPixelColor(3, Color(Helligkeit, Helligkeit, 0))
		LED4.config(bg='Yellow')
		# weblightcolor="yellow" # configure color for webdisplay
		Tag.config(text="Tag")
	else:
		strip.setPixelColorRGB(3, 0, 0, Helligkeit, 255)
		# strip.setPixelColor(3, Color(0, 0, Helligkeit))
		LED4.config(bg='blue') 
		# weblightcolor="blue" # configure color for webdisplay
		Tag.config(text="Nacht")
		# weblightcolor = "red"

# create webpage from template using mako
#FilledTemplate=piftemplate.render(temper="%.2f" % temperature, humid = "%.1f" % humidity, press="%.1f" % pressure, light="%.1f" % lichtstaerke, tmpcol=web_tmp_color)
# FilledTemplate=piftemplate.render(temper="%.1f" % temperature, humid = "%.1f" % humidity, press="%.1f" % pressure, light="%.1f" % lichtstaerke, tmpcol=webtmpcolor, humcol=webhumicolor, pressurecol=webpressurecolor, lightcol=weblightcolor)
# print(FilledTemplate)
# htmlpage=open(pifhtmlpage,"w+")
# htmlpage.write(FilledTemplate)
# htmlpage.close()
# end creating webpage
	
	strip.show()




	fenster.after(500, main) 

# def Quit(): 

# # htmlpage=open(pifhtmlpage,"w+")
# # htmlpage.write(time.strftime("%Y%m%d_%H%M%S",  time.localtime())) 
# # htmlpage.write(" - Webserver running; PIF python app not running")
# # htmlpage.close()

# 	draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=255, fill=1)
# 	oled.display()
# 	# logo = Image.open('lgk-6.png')
# 	# draw.bitmap((2, 0), logo, fill=0)
# 	oled.display()

# # strip.setPixelColor(0, Color(0, 0, 0))
# # strip.setPixelColor(1, Color(0, 0, 0))
# # strip.setPixelColor(2, Color(0, 0, 0))
# # strip.setPixelColor(3, Color(0, 0, 0))
# 	strip.show()

# 	fenster.destroy()

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

fenster = Tk(className=" LGK-BECWE LAM-MACEDO  PIF DAP 2020-21")
fenster.geometry("830x320")
titel = Label(master=fenster, text='Klimadaten', font=('Arial',16))
titel.config(fg='blue', bg='yellow',padx=10,pady=10 )

rahmen_TE1 = Frame(fenster, relief=RIDGE, bd=4,)
rahmen_LD1 = Frame(fenster, relief=RIDGE, bd=4,)
rahmen_FT1 = Frame(fenster, relief=RIDGE, bd=4,)
rahmen_HL1 = Frame(fenster, relief=RIDGE, bd=4,)

Temperaturt = Label(rahmen_TE1, text='  Temperatur  ')
Feuchtet = Label(rahmen_FT1, text='  Rel. Luftfeuchte  ')
Luftdruckt = Label(rahmen_LD1, text='  Luftdruck  ')
Hellt = Label(rahmen_HL1, text='  Lichtstaerke  ')


TemperaturWert= Label(rahmen_TE1, text='----',font=('Arial',16))
FeuchteWert= Label(rahmen_FT1, text='----',font=('Arial',16))
LuftdruckWert= Label(rahmen_LD1, text='----',font=('Arial',16))
HellWert= Label(rahmen_HL1, text='----',font=('Arial',16))


# Quit = Button(fenster, text='Exit', command=Quit,)

titel.place(x=250,y=30,width=320, height=25)

rahmen_TE1.place(x=70,y=90,width=140, height=70)
Temperaturt.place(x=5,y=5,width=120, height=25)
rahmen_FT1.place(x=250,y=90,width=140, height=70)
Feuchtet.place(x=5,y=5,width=120, height=25)
rahmen_LD1.place(x=430,y=90,width=140, height=70)
Luftdruckt.place(x=5,y=5,width=120, height=25)
rahmen_HL1.place(x=610,y=90,width=140, height=70)
Hellt.place(x=5,y=5,width=120, height=25)



TemperaturWert.place(x=5,y=30,width=120, height=25)
FeuchteWert.place(x=5,y=30,width=120, height=25)
LuftdruckWert.place(x=5,y=30,width=120, height=25)
HellWert.place(x=5,y=30,width=120, height=25)

Max = Label(fenster, text='Max')
Max.place(x=30,y=180,width=50, height=25)
Min = Label(fenster, text='Min')
Min.place(x=30,y=235,width=50, height=25)

TEM_MA = Scale(fenster, from_=-15, to=45,length=140,tickinterval=20,orient=HORIZONTAL)
TEM_MA.place(x=70,y=160)
TEM_MI = Scale(fenster, from_=-15, to=45,length=140,tickinterval=20,orient=HORIZONTAL)
TEM_MI.place(x=70,y=215)
TEM_MA.set(25),TEM_MI.set(3)


Name = Label(fenster, text='W. Becker & S. Macedo')
Name.place(x=648,y=305,width=190, height=15)


FT_MA = Scale(fenster, from_=2, to=98,length=140,tickinterval=24,orient=HORIZONTAL)
FT_MA.place(x=250,y=160)
FT_MI = Scale(fenster, from_=2, to=98,length=140,tickinterval=24,orient=HORIZONTAL)
FT_MI.place(x=250,y=215)
FT_MA.set(64),FT_MI.set(42)

LD_MA = Scale(fenster, from_=800, to=1100,length=140,tickinterval=150,orient=HORIZONTAL)
LD_MA.place(x=430,y=160)
LD_MI = Scale(fenster, from_=800, to=1100,length=140,tickinterval=150,orient=HORIZONTAL)
LD_MI.place(x=430,y=215)
LD_MA.set(1033),LD_MI.set(934)



Tag = Label(fenster, text='Tag')
Tag.place(x=635,y=255,width=90, height=25)

HL_TN = Scale(fenster, from_=0, to=100,length=140,tickinterval=50,orient=HORIZONTAL)
HL_TN.place(x=610,y=188)
HL_TN.set(30)

#CPU_t = Label(fenster, text='---')
#CPU_t.place(x=700,y=2,width=130, height=25)

LEDl = Label(fenster, text='LED')
LEDl.place(x=3,y=30,width=25, height=25)
LED = Scale(fenster, from_=1, to=255,length=70,orient=HORIZONTAL)
LED.place(x=30,y=10)
LED.set(1)


LED1 = Button(fenster, text='',font=('Arial',12),command=Standard1)
LED1.place(x=128,y=280,width=24, height=24)

LED2 = Button(fenster, text='',font=('Arial',12),command=Standard2)
LED2.place(x=308,y=280,width=24, height=24)

LED3 = Button(fenster, text='',font=('Arial',12),command=Standard3)
LED3.place(x=488,y=280,width=24, height=24)

LED4 = Button(fenster, text='',font=('Arial',12),command=Standard4)
LED4.place(x=668,y=280,width=24, height=24)

# Quit.place(x=1,y=1,width=28, height=25)
# fenster.mainloop()

def updateDb(Sensor=Sensor, db=db):
	while True:
		(chip_id, chip_version) = readBME280ID()
		temperature,pressure,humidity = readBME280All()
		lichtstaerke = readLight()
		now = datetime.datetime.now()
		datedb = now.strftime("%d-%m-%Y %H:%M")
		temperaturedb = ("Temperatur: %4.1f C" % (temperature))
		humiditydb = ("Rel.Feuchte: %4.1f" % (humidity)+" %")
		pressuredb = ("Luftdruck:%6.1f hPa" % (pressure)) 
		lightdb = ("Lichtst.: %6.1f" % (lichtstaerke)+" lux")
		new_sensors = Sensor(date=datedb, temperature=temperaturedb, humidity=humiditydb, pressure=pressuredb, light=lightdb)
		db.session.add(new_sensors)
		db.session.commit()
		print("New DATA added to dB")
		time.sleep(5*60)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/aboutus')
def aboutus():
	return render_template('aboutus.html')


@app.route('/system')
def system():
	cpu = psutil.cpu_percent()
	ram = psutil.virtual_memory().percent
	freespace = psutil.disk_usage('/').percent
	ip = get_ip()
	return render_template('system.html', ram=ram, cpu=cpu, freespace=freespace, ip=ip)

@app.route('/sensor')
def sensor():
	(chip_id, chip_version) = readBME280ID()
	temperature,pressure,humidity = readBME280All()
	lichtstaerke = readLight()
	Temperatur = ("Temperatur: %4.1f C" % (temperature))
	Feuchte = ("Rel.Feuchte: %4.1f" % (humidity)+" %")
	Luftdruck = ("Luftdruck:%6.1f hPa" % (pressure)) 
	Lichtstaerke = ("Lichtst.: %6.1f" % (lichtstaerke)+" lux")
	return render_template('sensor.html', Temperatur=Temperatur, Feuchte=Feuchte, Luftdruck=Luftdruck, Lichtstaerke=Lichtstaerke)

@app.route('/history')
def history():
	return render_template('history.html', sensors = Sensor.query.all())


if __name__ == "__main__":
	Taster()
	main()
	db.create_all()
	processSensor3 = Process(target=fenster.mainloop)
	processSensor3.start()
	processSensor2 = Process(target=updateDb)
	processSensor2.start()
	app.run(host='0.0.0.0',port=80, threaded=True, debug=True)
