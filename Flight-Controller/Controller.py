'''
Author:	Sean R Hamilton
QA:	
Date:	07/27/2016
References: PID introduction by George Gillard (https://www.dropbox.com/s/yg25rtawb0sboxw/PID%20Guide.pdf)
Description: receives sensor readings and calculates raw motor percentage to reach predefined setpoint.
'''

class Controller:
	# storage variables
	__base = 0	#sensor value when vehicle is on the ground
	__maxThrottle = 0	#maximum motor duty cycle
	__minThrottle = 0	#mininum motor duty cycle
	__throttleRange = 0	#motor duty cycle range
	__setPoint = 0	#destination value
	__position = 0	#current sensor value
	__maxInputValue = 0	#maximum sensor value
	__minInputValue = 0	#minimum sensor value
	__inputValueRange = 0	#usable sensor value range
	__integral = 0	#running sum of error values in getThrottlePercent
	__integralThreshold = 0	#maximum value of __integral
	__prevError = 0	#error from previous PID iteration in getThrottlePercent
	__kP = 0	#proportional constant
	__kI = 0	#integral constant
	__kD = 0	#derivative constant
	
	# initialize storage variables
	def __init__(self, initialSensorValue, maxThrottle, minThrottle, setPoint, integralThreshold, kP, kI, kD):
		__base = initialSensorValue,
		__maxThrottle = maxThrottle
		__minThrottle = minThrottle
		__throttleRange = abs(__maxThrottle - __minThrottle)
		__setPoint = setPoint + __base
		__position = __base
		__integralThreshold = integralThreshold
		__kP = kP
		__kI = kI
		__kD = kD
	
	# update position variable during flight
	def __updatePosition(self, sensorValue):
		__position = sensorValue
		
	# assign controller's destination value mid-flight
	def setSetPoint(self, setPoint):
		__setPoint = setPoint + __base
	
	# returns throttle value used to reach setPoint
	def getThrottlePercent(self, sensorValue):
		__updatePosition(sensorValue)
		
		#return (((((__position - __minInputValue) * __throttleRange) / __inputValueRange) + __minThrottle) * 100) / throttleRange #calculates directly proportional throttle value. The lazy solution
		
		error = __setPoint - __position #calculate new error value
		
		#calculate new integral value
		if ( abs(__integral) > abs(__integralThreshold) ):
			__integral = 0
		else:
			__integral = __integral + error
		
		derivative = error - __prevError #calculate new derivative value
		__prevError = error #update previous error storage
		
		adjustedOutput = (kP * error) + (kI * __integral) + (kD * derivative) #calculate motor compensation
		adjustedOutput = (adjustedOutput * 100) / throttleRange #convert output to percentage
		
		#restrict output to expected range
		if (adjustedOutput < __minThrottle):
			return __minThrottle
		elif (adjustedOutput > __maxThrottle):
			return __maxThrottle
		else:
			return adjustedOutput 
		
	# safely return the vehicle to the base position. Will cause vehicle to plummet to the ground in current configuration.
	def land(self):
		setSetPoint(__base)
			