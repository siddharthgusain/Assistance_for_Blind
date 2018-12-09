import sys
import Adafruit_DHT
import time
import urllib
import RPi.GPIO as GPIO                    
import time
import httplib
import serial
import threading




#led setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
led=2
GPIO.setup(led,GPIO.OUT)


#ultrasonic setup
TRIG = 23                                
ECHO = 24    
GPIO.setup(TRIG,GPIO.OUT)                  
GPIO.setup(ECHO,GPIO.IN) 
min=120                           #setting minimum distance equals to 120m


#gps setup  
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)


def temp_and_humidity():
	while True:

    	humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    	data=urllib.urlopen("https://api.thingspeak.com/update?api_key=NIQN90JVJSNUJR9E&field1="+str(temperature)+"&field2="+str(humidity))
    	print data

    	print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
    	time.sleep(1)
    	if(temperature>25):
        	GPIO.output(led,True)
    	else:
        	GPIO.output(led,False)



def ultrasonic():
	print "Distance measurement in progress"
	while True:

  		GPIO.output(TRIG, False)                 
  		print "Waitng For Sensor To Settle"
  		time.sleep(2)                           

  		GPIO.output(TRIG, True)                 
  		time.sleep(0.00001)                      
  		GPIO.output(TRIG, False)                

  	while GPIO.input(ECHO)==0:             
    		pulse_start = time.time()            

  	while GPIO.input(ECHO)==1:              
    		pulse_end = time.time()                

  	pulse_duration = pulse_end - pulse_start 

  	distance = pulse_duration * 17150        
  	distance = round(distance, 2)
  
  	print "distance="+str(distance)         
  
                         
  	if(distance<min):                                             
    		GPIO.output(led,True)
  	else:
    		GPIO.output(led,False)


def gps():
	ser= serial.Serial(port='/dev/ttyS0',baudrate=9600,parity=serial.PARITY_NONE,timeout=1)
	time.sleep(1)
	print "welcome"

	sleep = 60 # how many seconds to sleep between posts to the channel

	key = 'SYO11KL0WAKC8POW'  # Thingspeak channel to update

	while (True):
    		data=[]
    		a=''
    		data.append(ser.read().decode('UTF-8'))
    		for i in range(len(data)):
      		a+=data[i]
      		print a
    		time.sleep(1)

    		params = urllib.urlencode({'Latitude':lat , 'Longitude':lon,'key':key}) 

    		headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}

    		conn = httplib.HTTPConnection("api.thingspeak.com:80")

    		try:
      			conn.request("POST", "/update", params, headers)

      			response = conn.getresponse()

      			print temp

      			print response.status, response.reason

      			data = response.read()

      			conn.close()

   	       except:

      			print "connection failed"

      			break



if __name__ == "__main__":
		t1=threading.Thread(target=temp_and_humidity)
		t2=threading.Thread(target=ultrasonic)
		t3=threading.Thread(target=gps)
		t1.start()
		t2.start()
		t3.start()
		t1.join()
 		t2.join()
		t3.join()		



    

