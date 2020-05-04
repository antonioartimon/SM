#we import the RPi.GPIO library with the name of GPIO
import RPi.GPIO as GPIO
#we import the sleep module from the time library
import time
#we import SMTP protocol client
import smtplib
#To control the sensor we are going to use the Adafruit DHT11 Python library
import Adafruit_DHT
#GPIO.BCM option means that you are referring to the pins by the "Broadcom SOC channel" number
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#name the type of sensor used
type=Adafruit_DHT.DHT11
#declare the pin used by the sensor in GPIO form
dht11=25
trig=23
echo=24
#set the trigger pin as OUTPUT and the echo as INPUT
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
#set the sensor as INPUT
GPIO.setup(dht11,GPIO.IN)
#create one SMTP object
server=smtplib.SMTP('smtp.gmail.com',587)
#start the server
server.starttls()
#login data for your account
server.login("username@gmail.com","password")

def calculate_distance():
    #set the trigger to HIGH
	GPIO.output(trig,GPIO.HIGH)
    #sleep 0.00001 s and the set the trigger to LOW
	time.sleep(0.00001)
	GPIO.output(trig,GPIO.LOW)
    #save the start and stop times
	start=time.time()
	stop=time.time()
    #modify the start time to be the last time until the echo become HIGH
	while GPIO.input(echo)==0:
		start=time.time()
    #modify the stop time to be the last time until the echo becomes LOW
	while GPIO.input(echo)==1:
		stop=time.time()
    #get the duration of the echo pin as HIGH
	duration=stop-start
    #calculate the distance
	distance=34300/2*duration
    #return the distance
	return distance
    
#we start a loop that never ends
try:
	while True:
        #make the reading
		humidity, temperature=Adafruit_DHT.read_retry(type,dht11) 
        #we will save the values only if they are not null
		if humidity is not None and temperature is not None:
        #msg is the message that will be sent 
        #msg has temperature and humidity values
            		msg="Temperature = {:.1f} , Humidity = {:.1f}" .format(temperature, humidity)
		if calculate_distance() <50:
        #send the message    
			server.sendmail("username@gmail.com","receiver@gmail.com",msg)
			print("E-mail sent !")
		time.sleep(1)
except KeyboardInterrupt:
	pass
#close the server    
server.quit()
##clean all the used ports
GPIO.cleanup()
