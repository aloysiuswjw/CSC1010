import cv2
import sys
import random
import time
from sense_hat import SenseHat
from paho.mqtt import client as mqtt_client

# connect to mqtt broker
broker = '192.168.1.14'
port = 1883
topic = "room1"  
client_id = f'python-mqtt-{random.randint(0, 1000)}'

sense = SenseHat()
count=0
temp=0
humidity=0

def opencvdetection():
	cascPath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)
	# open webcam
	video_capture = cv2.VideoCapture(0)
	client =connect_mqtt()
	client.loop_start()
	#publish every 10 sec
	timer =10
	sumPublishTime=0
	sumRotationTime=0
	
	while True:
		# calculate start time
		start_time=time.time()
		# capture frame-by-frame
		ret, frame = video_capture.read()
		# resizing for faster detection
		frame = cv2.resize(frame, (640, 480))
		# using a greyscale picture, also for faster detection
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#attr to detect face
		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.2,
			minNeighbors=5,
			minSize=(30, 30),       
		)
		
		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	
		#count number of faces and store as string in global count var
		global count
		count1= str(len(faces))
		count=int(count1)
		
		seconds= time.time()-start_time
		#seperate timer for publish and rotation time
		sumPublishTime+=seconds
		sumRotationTime+=seconds
		#first 10 sec
		if sumRotationTime<timer:
			showCapacity()
		#10-20 sec
		elif 10<=sumRotationTime<=20:
			showClock()
		#20-30 sec
		elif  20<=sumRotationTime<=30:
			showTempAndHumidity()
		#when above 30 reset clock timer
		elif sumRotationTime>30: 
			sumRotationTime=0
		#when detect people return to showcapacity interface
		if count>0:
			showCapacity()
		#publish to broker after 10sec
		if sumPublishTime>timer:
			publish(client)
			sumPublishTime=0
			
		#display the resulting frame
		cv2.imshow('Video', frame)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	client.loop_stop()
	#when everything is done, release the capture
	video_capture.release()
	cv2.destroyAllWindows()

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
	
	# create letter F
	full = [
	   #letter F 
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
	global count
	#print on sensehat matrix using indexes
	if count <5:
		pixel_offset = 0
		index = 0
		for index_loop in range(0, 4):
			for counter_loop in range(0, 4):
				#only top right of 4x4 is used
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
				#display on 4x4 on top left, top right, bottom left, bottom right
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
		
#connect to broker
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

#publich count, temp and humidity
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
	
	#get hour, min
	hour = time.localtime().tm_hour
	minute = time.localtime().tm_min
	pixel_offset = 0
	index = 0
	#same as showcapcity
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
	
	def thermometer():
		global temp,humidity
		temp = int(get_amb_temp())
		humidity = int(get_amb_humidity())
		display_thermostat(temp, humidity)

	thermometer()
	
def main():
	opencvdetection()
	
if __name__ =='__main__':
	main()
