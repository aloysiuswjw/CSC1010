import subprocess
import sys
import random
import time
import re
from paho.mqtt import client as mqtt_client
from sense_hat import SenseHat

broker = '172.20.10.10'
port = 1883
topic = "room2"  
client_id = f"python-mqtt-{random.randint(0, 1000)}" 

sense = SenseHat()
arr=[]
count = 0
temp = 0
humidity = 0

def getDisBTMACAddresses():
	cmd = "hcitool scan"
	#run command in terminal 
	output= subprocess.getstatusoutput(cmd)
	#convert to string
	output=''.join(map(str,output))
	print(output)
	#regex to check for MAC address format 
	pattern =re.compile(r'(?:[0-9a-fA-F]:?){12}')
	#print in list
	macAddressList = re.findall(pattern,output) 
	#store in array
	global arr,count
	for x in macAddressList:
		arr.append(x)
	count=len(arr)
	
	arr = []

	
def showCapacity():
	number = [
	   # zero
	   0, 1, 1, 1,
	   0, 1, 0, 1,
	   0, 1, 0, 1,
	   0, 1, 1, 1,
	   # one
	   0, 0, 1, 0,
	   0, 1, 1, 0,
	   0, 0, 1, 0,
	   0, 1, 1, 1,
	   # two
	   0, 1, 1, 1,
	   0, 0, 0, 1,
	   0, 0, 1, 0,
	   0, 1, 1, 1,
	   # three
	   0, 1, 1, 1,
	   0, 0, 0, 1,
	   0, 0, 1, 1,
	   0, 1, 1, 1,
	   # four
	   0, 1, 0, 1,
	   0, 1, 0, 1,
	   0, 1, 1, 1,
	   0, 0, 0, 1,
	   # five
	   0, 1, 1, 1,
	   0, 1, 0, 0,
	   0, 0, 1, 1,
	   0, 1, 1, 1,
	   # six
	   0, 1, 0, 0,
	   0, 1, 1, 1,
	   0, 1, 0, 1,
	   0, 1, 1, 1,
	   # seven
	   0, 1, 1, 1,
	   0, 0, 0, 1,
	   0, 0, 1, 0,
	   0, 1, 0, 0,
	   # eight
	   0, 1, 1, 1,
	   0, 1, 1, 1,
	   0, 1, 1, 1,
	   0, 1, 1, 1,
	   # nine
	   0, 1, 1, 1,
	   0, 1, 0, 1,
	   0, 1, 1, 1,
	   0, 0, 0, 1
	]
	
	# color
	red = [255, 0, 0]
	black = [0, 0, 0]
	darkblue=[0,0,139]
	
	full = [
	   # FL
	   0, 1, 1, 0,
	   0, 1, 0, 0,
	   0, 1, 1, 0,
	   0, 1, 0, 0,
	   
	   0, 1, 0, 0,
	   0, 1, 0, 0,
	   0, 1, 0, 0,
	   0, 1, 1, 0,
	   
	   0, 1, 0, 0,
	   0, 1, 0, 0,
	   0, 1, 0, 0,
	   0, 1, 1, 0,
	   
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   0, 0, 0, 0,
	   ]
	  
	clock_image = [
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0
	]
	
	client =connect_mqtt()
	client.loop_start()
	timer =10
	sumPublishTime=0
	sumRotationTime=0
	
	while True:
		start_time=time.time()
		global count
		getDisBTMACAddresses()
		if count <5:
			pixel_offset = 0
			index = 0
			for index_loop in range(0, 4):
				for counter_loop in range(0, 4):
					clock_image[index+4] = number[int(count%10)*16+pixel_offset]
					pixel_offset = pixel_offset + 1
					index = index + 1
				index = index + 4
			
			for index in range(0, 64):
				if (clock_image[index]):
					if index<32:
						clock_image[index] = red
				else:
					clock_image[index] = black
			
			sense.set_pixels(clock_image)
		else:
			pixel_offset = 0
			index = 0
			for index_loop in range(0, 4):
				for counter_loop in range(0, 4):
					if (count >= 10):
						clock_image[index] = number[int(count/10)*16+pixel_offset]
					clock_image[index+4] = number[int(count%10)*16+pixel_offset]
					clock_image[index+32] = full[int(count/10)*16+pixel_offset]
					clock_image[index+36] = full[int(count/10)*16+pixel_offset]
					pixel_offset = pixel_offset + 1
					index = index + 1
				index = index + 4
			
			for index in range(0, 64):
				if (clock_image[index]):
					if index<32:
						clock_image[index] = red
					else:
						clock_image[index] = darkblue
				else:
					clock_image[index] = black
			
			sense.set_pixels(clock_image)
			
		seconds= time.time()-start_time
		sumPublishTime+=seconds
		sumRotationTime+=seconds
		
		if 10<=sumRotationTime<=20:
			showClock()
		elif 20<=sumRotationTime<=30:
			showTempAndHumidity()
		elif sumRotationTime>30: 
			sumRotationTime=0
		if sumPublishTime>timer:
			publish(client)
			sumPublishTime=0
			
def connect_mqtt():
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
		    print("Connected to MQTT Broker!")
		else:
		    print("Failed to connect, return code %d\n", rc)

	client = mqtt_client.Client(client_id)
	# client.username_pw_set(username, password)
	client.on_connect = on_connect
	client.connect(broker, port)
	
	return client


def publish(client):
	global count,temp,humidity 
	msg = f"messages: {count,temp,humidity}"
	result = client.publish(topic, msg)
	status = result[0]
	if status == 0:
	    print(f"Send `{msg}` to topic `{topic}`")
	else:
	    print(f"Failed to send message to topic {topic}")
	    	
def showClock():
	number = [
	   # zero
	   0, 1, 1, 1,
	   0, 1, 0, 1,
	   0, 1, 0, 1,
	   0, 1, 1, 1,
	   # one
	   0, 0, 1, 0,
	   0, 1, 1, 0,
	   0, 0, 1, 0,
	   0, 1, 1, 1,
	   # two
	   0, 1, 1, 1,
	   0, 0, 0, 1,
	   0, 0, 1, 0,
	   0, 1, 1, 1,
	   # three
	   0, 1, 1, 1,
	   0, 0, 0, 1,
	   0, 0, 1, 1,
	   0, 1, 1, 1,
	   # four
	   0, 1, 0, 1,
	   0, 1, 0, 1,
	   0, 1, 1, 1,
	   0, 0, 0, 1,
	   # five
	   0, 1, 1, 1,
	   0, 1, 0, 0,
	   0, 0, 1, 1,
	   0, 1, 1, 1,
	   # six
	   0, 1, 0, 0,
	   0, 1, 1, 1,
	   0, 1, 0, 1,
	   0, 1, 1, 1,
	   # seven
	   0, 1, 1, 1,
	   0, 0, 0, 1,
	   0, 0, 1, 0,
	   0, 1, 0, 0,
	   # eight
	   0, 1, 1, 1,
	   0, 1, 1, 1,
	   0, 1, 1, 1,
	   0, 1, 1, 1,
	   # nine
	   0, 1, 1, 1,
	   0, 1, 0, 1,
	   0, 1, 1, 1,
	   0, 0, 0, 1
	] 
	#hour-red, min-blue  
	hour_color = [255, 0, 0]
	minute_color = [0, 0, 139]
	black = [0, 0, 0]
	  
	clock_image = [
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0,
	   0, 0, 0, 0, 0, 0, 0, 0
	]
	hour = time.localtime().tm_hour
	minute = time.localtime().tm_min
	pixel_offset = 0
	index = 0
	for index_loop in range(0, 4):
		for counter_loop in range(0, 4):
			if (hour >= 10):
				clock_image[index] = number[int(hour/10)*16+pixel_offset]
			clock_image[index+4] = number[int(hour%10)*16+pixel_offset]
			clock_image[index+32] = number[int(minute/10)*16+pixel_offset]
			clock_image[index+36] = number[int(minute%10)*16+pixel_offset]
			pixel_offset = pixel_offset + 1
			index = index + 1
		index = index + 4
  
	for index in range(0, 64):
		if (clock_image[index]):
			if index < 32:
				clock_image[index] = hour_color
			else:
				clock_image[index] = minute_color
		else:
			clock_image[index] = black
  
	sense.set_pixels(clock_image)
		
def showTempAndHumidity():
	def digit_b(color):
	  X = color
	  O = [0, 0, 0]
	  return [
		O,O,O,O,
		O,O,O,O,
		O,O,O,O,
		O,O,O,O    
	  ]

	def digit_1(color):
	  X = color
	  O = [0, 0, 0]
	  return [
		O,X,X,X,
		O,O,X,X,
		O,O,X,X,
		O,O,X,X 
	  ]

	def digit_2(color):
	  X = color
	  O = [0, 0, 0]
	  return [
		O,X,X,X,
		O,O,X,X,
		O,X,X,O,
		O,X,X,X    
	  ]

	def digit_3(color):
	  X = color
	  O = [0, 0, 0]
	  return [
		O,X,X,X,
		O,O,X,X,
		O,O,O,X,
		O,X,X,X  
	  ]

	def digit_4(color):
	  X = color
	  O = [0, 0, 0]
	  return [
		O,X,O,X,
		O,X,O,X,
		O,X,X,X,
		O,O,O,X    
	  ]

	def digit_5(color):
	  X = color
	  O = [0, 0, 0]
	  return [
		O,X,X,X,
		O,X,X,O,
		O,O,X,X,
		O,X,X,X    
	  ]

	def digit_6(color):
	  X = color
	  O = [0, 0, 0]
	  return [
		O,X,O,O,
		O,X,X,X,
		O,X,O,X,
		O,X,X,X    
	  ]

	def digit_7(color):
	  X = color
	  O = [0, 0, 0,]
	  return [
		O,X,X,X,
		O,O,O,X,
		O,O,X,O,
		O,O,X,O    
	  ]

	def digit_8(color):
	  X = color
	  O = [0, 0, 0,]
	  return [
		O,X,X,O,
		O,X,X,X,
		O,X,O,X,
		O,X,X,X    
	  ]

	def digit_9(color):
	  X = color
	  O = [0, 0, 0,]
	  return [
		O,X,X,X,
		O,X,O,X,
		O,X,X,X,
		O,O,O,X    
	  ]

	def digit_0(color):
	  X = color
	  O = [0, 0, 0,]
	  return [
		O,O,X,O,
		O,X,O,X,
		O,X,O,X,
		O,O,X,O    
	  ]

	def get_digit_map(digit, color):
		if digit == 0:
			return digit_0(color)
		elif digit == 1:
			return digit_1(color)
		elif digit == 2:
			return digit_2(color)
		elif digit == 3:
			return digit_3(color)
		elif digit == 4:
			return digit_4(color)
		elif digit == 5:
			return digit_5(color)
		elif digit == 6:
			return digit_6(color)
		elif digit == 7:
			return digit_7(color)
		elif digit == 8:
			return digit_8(color)
		elif digit == 9:
			return digit_9(color)
		else:
			return digit_b(color)

	# compose an image of 2 upper digits and 2 lower digits
	def compose_image(U1, U2, L1, L2):
	  image = []
	  image[0:7] = U1[0:4] + U2[0:4]
	  image[8:15] = U1[4:8] + U2[4:8]
	  image[16:23] = U1[8:12] + U2[8:12]
	  image[24:31] = U1[12:16] + U2[12:16]
	  
	  image[32:39] = L1[0:4] + L2[0:4]
	  image[40:47] = L1[4:8] + L2[4:8]
	  image[48:55] = L1[8:12] + L2[8:12]
	  image[56:63] = L1[12:16] + L2[12:16]
	  return image

	def display_thermostat(temp, humidity):
	  upper_color = [255, 0, 0]
	  lower_color = [0, 0, 139]

	  U1 = get_digit_map(temp // 10, upper_color)
	  U2 = get_digit_map(temp % 10, upper_color)
	  L1 = get_digit_map(humidity // 10, lower_color)
	  L2 = get_digit_map(humidity % 10, lower_color)
	  sense.set_pixels(compose_image(U1, U2, L1, L2))

	def get_amb_temp():
	  avg_sensor_temp = (sense.get_temperature_from_humidity() + sense.get_temperature_from_pressure()) / 2
	  amb_temp = 0.0071*avg_sensor_temp*avg_sensor_temp + 0.86*avg_sensor_temp - 10.0 - 3
	  return amb_temp

	def get_amb_humidity():
	  sensor_humidity = sense.get_humidity()
	  sensor_temp = sense.get_temperature_from_humidity()
	  amb_humidity = sensor_humidity * (2.5 - (0.029 * sensor_temp))
	  return amb_humidity
	
	# show two lines of 2 digit 4x4 numbers will update constantly
	def thermometer():
		global temp,humidity
		temp = int(get_amb_temp())
		humidity = int(get_amb_humidity())
		display_thermostat(temp, humidity)
	thermometer()

	
def main():
	showCapacity()
	
if __name__ =='__main__':
	main()


	







































