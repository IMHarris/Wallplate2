#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import threading
import socket
import sys
import datetime
import os
import requests
import random
import signal
import getopt

import argparse
import logging
import logging.handlers
import json

#Read in the startup command line args
isdaemon=False
logtofile = False
for arg in sys.argv:
    if arg == '-d':
        isdaemon=True
    if arg == '-l':
        logtofile=True


#### LOGGING SETUP BEGIN
#Send Messages to log file if requested
if logtofile:
    # Defaults
    LOG_FILENAME = "/home/pi/piproj/wallplate/log/wallplate.log"
    LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"
    
    # # Define and parse command line arguments
    # parser = argparse.ArgumentParser(description="My simple Python service")
    # parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")
    # 
    # # If the log file is specified on the command line then override the default
    # args = parser.parse_args()
    # if args.log:
    #         LOG_FILENAME = args.log
    
    # Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
    # Give the logger a unique name (good practice)
    logger = logging.getLogger(__name__)
    # Set the log level to LOG_LEVEL
    logger.setLevel(LOG_LEVEL)
    # Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
    # Format each log message like this
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    # Attach the formatter to the handler
    handler.setFormatter(formatter)
    # Attach the handler to the logger
    logger.addHandler(handler)
    
    # Make a class we can use to capture stdout and sterr in the log
    class MyLogger(object):
            def __init__(self, logger, level):
                    """Needs a logger and a logger level."""
                    self.logger = logger
                    self.level = level
    
            def write(self, message):
                    # Only log if there is a message (not just a new line)
                    if message.rstrip() != "":
                            self.logger.log(self.level, message.rstrip())
    
    # Replace stdout with logging to file at INFO level
    sys.stdout = MyLogger(logger, logging.INFO)
    # Replace stderr with logging to file at ERROR level
    sys.stderr = MyLogger(logger, logging.ERROR)


#### LOGGING SETUP END
print(sys.version_info)

if isdaemon:
    print("Wallplate launched as daemon. Will initiate 10-second delay to allow Apache to load.")
    time.sleep(10)

# import urllib.request
# import urllib.parse
import plivo

def sendSMS():
    
    try:
        auth_id = "MAMDC2YTGZODKZMTQ5OT"
        auth_token = "MWEzMmJhYzlkZGY3MTgzNGYxZWVkYWY3NWNlZDBi"
        print('here')
        p = plivo.RestAPI(auth_id, auth_token)
         
        params = {
            'src': '+18052209196', # Sender's phone number with country code
            'dst' : '+18479519366', # Receiver's phone Number with country code
            'text' : u"Hello, how are you?", # Your SMS Text Message - English
        #   'text' : u"こんにちは、元気ですか？" # Your SMS Text Message - Japanese
        #   'text' : u"Ce est texte généré aléatoirement" # Your SMS Text Message - French
        #   'url' : "http://example.com/report/", # The URL to which with the status of the message is sent
            'method' : 'POST' # The method used to call the url
        }
         
        response = p.send_message(params)
 
        # Prints the complete response
        print (str(response))
#Textbelt 
        #Send text message
#         payload = {'message': 'Garage door activated' , 'number':'8479519366'}
#         r = requests.post('https://api.plivo.com/v1/Account/{auth_id}/',data=payload)
#         #print (r.url)
#         print('Text server response: ', r.text)

#EZTexting code      
#         import pycurl, io, urllib
#         curl = pycurl.Curl()
#         curl.setopt(pycurl.SSL_VERIFYPEER, 1)
#         curl.setopt(pycurl.SSL_VERIFYHOST, 2)
# #         curl.setopt(pycurl.CAINFO, "ca-certificates.crt")
# 
#         params = ""
#         params+= "User=" + uname + "&Password=" + hashCode
#         params+= "&Subject=From Winnie"
#         params+= "&Message=I am a Bear of Very Little Brain, and long words bother me"
#         params+= "&PhoneNumbers[]=8479519366"
#         params+= "&MessageTypeID=1&StampToSend=1305582245"
#  
#         curl.setopt(pycurl.POSTFIELDS, params)
# 
#         curl.setopt(pycurl.URL, "https://app.eztexting.com/sending/messages?format=json")
# 
#         contents = io.BytesIO()
#         curl.setopt(pycurl.WRITEFUNCTION, contents.write)
# 
#         curl.perform()
# 
#         print (contents.getvalue().decode('UTF-8') + "\n==============================\n") #result of API call
# 
#         responseCode = curl.getinfo(pycurl.HTTP_CODE);
#         print ('Response code: ' + str(responseCode))
#         isSuccesResponse = responseCode < 400;
# 
#         pyobj = json.loads(contents.getvalue().decode('UTF-8'))
# 
#         print ('Status: ' + str(pyobj['Response']['Status']))
#         print ('Code: ' + str(pyobj['Response']['Code']))
#         if (isSuccesResponse):
#             print ('Message ID: ' + str(pyobj['Response']['Entry']['ID']))
#             print ('Subject: ' + pyobj['Response']['Entry']['Subject'])
#             print ('Message: ' + pyobj['Response']['Entry']['Message'])
#             print ('Message Type ID: ' + str(pyobj['Response']['Entry']['MessageTypeID']))
#             print ('Total Recipients: ' + str(pyobj['Response']['Entry']['RecipientsCount']))
#             print ('Credits Charged: ' + str(pyobj['Response']['Entry']['Credits']))
#             print ('Time To Send: ' + pyobj['Response']['Entry']['StampToSend'])
#             print ('Phone Numbers: ' + str(pyobj['Response']['Entry']['PhoneNumbers']))
#             try:
#                 print ('Locally Opted Out Numbers: ' + str(pyobj['Response']['Entry']['LocalOptOuts']))
#             except KeyError:
#                 pyobj['Response']['Entry']['LocalOptOuts'] = ''
#             try:
#                 print ('Globally Opted Out Numbers: ' + pyobj['Response']['Entry']['GlobalOptOuts'])
#             except KeyError:
#                 pyobj['Response']['Entry']['GlobalOptOuts'] = ''
#         else:
#             print ('Fail response from SMS server: ' + str(pyobj['Response']['Errors']))
        
        
#Text Local code      
#         data =  urllib.parse.urlencode({'username': uname, 'hash': hashCode, 'numbers': numbers,
#             'message' : message, 'sender': sender})
#         data = data.encode('utf-8')
#         zz = urllib.request.Request("http://api.txtlocal.com/send/?")
#         f = urllib.request.urlopen(zz, data)
#         fr = f.read()
#         return(fr)
    
    except Exception as inst:
        print('Unable to send SMS message')
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)   
    
    

class App:

    class LED:

        class blinkthread(threading.Thread):

            def __init__(self, threadID, pin, iscathode, program, ontime, offtime, duration, delay, brightness = 100, israndom = False):
                threading.Thread.__init__(self)
                self.__threadID = threadID
                self.__pin = pin
                self._isblinking = False
                self.__ontime = ontime
                self.__offtime = offtime
                self.__brightness = brightness
                self.__ledpwm = GPIO.PWM(pin,500)
                 #If duration is set to zero, duration is unlimited
                if duration == 0:
                    self.__duration = 10000000
                else:
                    self.__duration = duration
                self.__delay = delay
                self.__israndom = israndom
                self.__iscathode = iscathode
                self.__stopevent = threading.Event(  )
            
            def run(self):
                try:
                    
                    self._isblinking = True
                    self.__stopevent.wait(self.__delay)
                    
                    timestart = time.time()
                    timeend = timestart + self.__duration - self.__delay
                     
                    if self.__israndom:
                        random.seed()
                        #self.__ledpwm.start(self.__brightness)
                        self.__ledpwm.start(0)
                        self.__stopevent.wait(self.__offtime * random.random())
                            #GPIO.output(self.__pin, self.__iscathode)
                        
                        while not self.__stopevent.isSet(  ) and time.time() < timeend:
                            #Random starts with the LED off, so there is a random wait time before blinking begins
                            #GPIO.output(self.__pin,not self.__iscathode)
                            self.__ledpwm.ChangeDutyCycle(self.__brightness * random.random()**3)
                            
                            #GPIO.output(self.__pin, self.__iscathode)
                            
                            self.__stopevent.wait(self.__ontime * random.random())
                            self.__ledpwm.ChangeDutyCycle(0)
                            self.__stopevent.wait(self.__offtime * random.random())
                            
                    elif self.__offtime > 0:
                        
                        #Blinking light
                        while not self.__stopevent.isSet(  ) and time.time() < timeend:
                            GPIO.output(self.__pin, self.__iscathode)
                            self.__stopevent.wait(self.__ontime)
                            GPIO.output(self.__pin, not self.__iscathode)
                            self.__stopevent.wait(self.__offtime)
                            
                    else:
                        #Light stays on
                        self.__ledpwm.start(99)
                        while not self.__stopevent.isSet(  )and time.time() < timeend:
                            #GPIO.output(self.__pin, self.__iscathode)
                            self.__stopevent.wait(.25)
                            
                finally:
                    #self.__ledpwm.stop()
                    #self.__ledpwm.deinit()
                    GPIO.output(self.__pin, not self.__iscathode)
                    self.__ledpwm.ChangeDutyCycle(100)
                    self.__ledpwm.stop()
#                     self.__ledpwm = None
                    self.__stopevent.clear()
                    print ('thread completed: ' + self.__threadID)
            
            @property
            def ontime(self):
                return self.__ontime
            
            @property
            def offtime(self):
                return self.__offtime
            
            @property
            def duration(self):
                return self.__duration
            
            def stopblink(self):
                self.__stopevent.set(  )
                #print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
                
            @property
            def isblinking(self):
                return self._isblinking
        
        def __init__(self, name, pin, iscathode =True):
            self.__pin = pin
            self._name = name
            self.__iscathode = iscathode
            GPIO.setup(pin,GPIO.OUT)
            'Make sure the starting state is light off'
            GPIO.output(self.__pin, not self.__iscathode)
            self._isblinking = False
            
        def on(self):
            GPIO.output(self.__pin, self.__iscathode)
            
        def off(self):
            GPIO.output(self.__pin, not self.__iscathode)
        
        def blink(self, program, delay1 = 0, delay2 = 0, duration = 0, delay = 0, brightness = 100, israndom = False):
            self.thread1 = self.blinkthread(self._name, self.__pin, self.__iscathode, program, delay1, delay2, duration, delay, brightness, israndom)
            self.thread1.start()
            self._isblinking = True

        def stopblink(self):
            if (self._isblinking):
                if (self.thread1.isAlive()):
                    self.thread1.stopblink()
                    self.thread1.join()
                    self._isblinking = False
       
            if GPIO.input(self.__pin) and self.__iscathode:
                GPIO.output(self.__pin,not self.__iscathode)
            
        @property
        def isblinking(self):
            return self._isblinking
            print ('Blinking ', self._isblinking)

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        self.__led1pin = 18
        self.__led2pin = 17
        
        led0pin =18
        led1pin = 17
        led2pin = 2
        led3pin = 3
        led4pin = 4
        led5pin = 9
        led6pin = 10
        led7pin = 11
        
        #Set up relay trigger pins
        self.__amppowerpin = 21
        self.__ampmutepin = 20
        self.__garagepin = 12
        self.__unallocatedpin = 16
        
        #Set up switch pins
        self.__mainswitchpin = 6
        self.__garagestatuspin = 26
        
        #Set up LEDs
        self.__LEDs = [None] * 8
        self.__LEDs[0] = self.LED('red led', led0pin, True)
        self.__LEDs[1] = self.LED('yellow led', led1pin, True)
        self.__LEDs[2] = self.LED('Tri1 blue led', led2pin, True)
        self.__LEDs[3] = self.LED('Tri1 red led', led3pin, True)
        self.__LEDs[4] = self.LED('Tri1 green led', led4pin, True)
        self.__LEDs[5] = self.LED('Tri2 green led', led5pin, True)
        self.__LEDs[6] = self.LED('Tri2 blue led', led6pin, True)
        self.__LEDs[7] = self.LED('Tri2 red led', led7pin, True)
        
        GPIO.output(led0pin ,False)
        GPIO.output(led1pin ,False)
        GPIO.output(led2pin ,False)
        GPIO.output(led3pin ,False)
        GPIO.output(led4pin ,False)
        GPIO.output(led5pin ,False)
        GPIO.output(led6pin ,False)
        GPIO.output(led7pin ,False) 
        
        #Set up switches
        GPIO.setup(self.__mainswitchpin, GPIO.IN)
        GPIO.setup(self.__garagestatuspin, GPIO.IN)
        
        #Set up amp control pins
        GPIO.setup(self.__amppowerpin, GPIO.OUT)
        GPIO.output(self.__amppowerpin,True)
        GPIO.setup(self.__ampmutepin, GPIO.OUT)
        GPIO.output(self.__ampmutepin,True)
        GPIO.setup(self.__garagepin ,GPIO.OUT)
        GPIO.output(self.__garagepin ,True)
        GPIO.setup(self.__unallocatedpin ,GPIO.OUT)
        GPIO.output(self.__unallocatedpin ,True)
        
    def ampon(self, isOn):
        GPIO.output(self.__amppowerpin, not isOn)
        if isOn:
            print('Amp switched on.')
        else:
            print('Amp switched off.')
        
    def muteon(self, isOn):
        GPIO.output(self.__ampmutepin, isOn)
        
    def RunWebCommands(self,commandlist):
        
        print("executing web commands")
        
        try:
            
            if len(commandlist) > 0:
                commanddict = json.loads(commandlist)
                
                if "door" in commanddict:
                    self.ActivateGarage()
                
                elif "LEDs" in commanddict:
                    #initialize variables
                    self.ontime = [0] * 8
                    self.offtime = [0] * 8
                    self.duration = [0] * 8
                    self.delay = [0] * 8
                    self.random = [False] * 8
                    self.brightness = [100] * 8
                    
                    LEDs = commanddict["LEDs"]
                    print("LEDs: ", LEDs)
                    for k, led in LEDs.items():
                        i = int(led["index"])
                        self.ontime[i] = float(led["on_time"])
                        self.offtime[i] = float(led["off_time"])
                        self.duration[i] = float(led["duration"])
                        self.delay[i] = float(led["delay"])
                        self.random[i] = led["random"]
                        self.brightness[i] = float(led["brightness"])
                     
                    for index in range(len(self.ontime)):
                        #kickoff threads
                        self.LEDBlink(index,self.ontime[index], self.offtime[index], self.duration[index],self.delay[index], self.brightness[index], self.random[index])
                    
        except Exception as inst:
            print('App unable to execute web command string')
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
# ...                          # but may be overridden in exception subclasses
# ...     x, y = inst.args     # unpack args
# ...     print('x =', x)
# ...     print('y =', y)
#             
            
    def LEDBlink (self, ledindex, ontime, offtime, duration,delay, brightness = 100, israndom=False):
        self.__LEDs[ledindex].blink('', ontime, offtime, duration,delay, brightness, israndom)
        
    def SwitchValue(self):
        return GPIO.input(self.__mainswitchpin)
    
    def GarageOpen(self):
        return not GPIO.input(self.__garagestatuspin)
    
    def RunSwitchProgram(self):
        
        self.ampon(True)
        self.muteon(False)
        time.sleep(0.5)
        self.LEDBlink(4, 0.15, 1, 5, 0, 100, True)
        self.LEDBlink(2, 0.15, 1, 5, 0.15, 100,True)
        self.LEDBlink(3, 0.15, 1, 5, 0.3, 100, True)
        self.LEDBlink(5, 0.15, 0.3, 5, 0, 100, True)
        self.LEDBlink(6, 0.15, 0.3, 5, 0.15, 100, True)
        self.LEDBlink(7, 0.15, 0.3, 5, 0.3, 100, True)
        self.LEDBlink(1, 0.15, 1, 5, 0, 100, True)
        self.LEDBlink(0, 0.15, 1, 5, 0, 100, True)
        os.system('aplay /home/pi/piproj/Sounds/electric.wav')
        self.ampon(False)
        self.muteon(True)
        
    def LEDOff(self, ledindex):
        if self.__LEDs[ledindex].isblinking:
            self.__LEDs[ledindex].stopblink()
        self.__LEDs[ledindex].off()
        
    def KillAll(self):
        self.LEDOff(0)
        self.LEDOff(1)
        self.LEDOff(2)
        self.LEDOff(3)
        self.LEDOff(4)
        self.LEDOff(5)
        self.LEDOff(6)
        self.LEDOff(7)
#         self.__LEDs = [None] * 8
    
    def KillLED(self,index):
        self.LEDOff(index)
    
    def cleanup(self):
        self.KillAll()
        GPIO.cleanup()
        print('Cleaning up')

    def ActivateGarage(self):
        print('Activating garage door.')
        GPIO.output(self.__garagepin, False)
        time.sleep(0.45)
        GPIO.output(self.__garagepin, True)
        
        #Send text message
        payload = {'message': 'Garage door activated' , 'number':'8479519366'}
        r = requests.post('http://textbelt.com/text',data=payload)
        #print (r.url)
        print('Text server response: ', r.text)
        
class ListenThread(threading.Thread):

            _sentconnection = False
            __connection = None
            clientconnected = False
            
            def __init__(self, threadID):
                threading.Thread.__init__(self)
                self.__threadID = threadID
                self.__stopevent = threading.Event(  )
                self.__clientconnected = False
            
            def run(self):
                try:            
                    # Wait for a connection 
                    print (sys.stderr, 'New listening thread activated.')
                    self.__connection, self.__client_address = sock.accept()
                    self.__clientconnected = True
                
#                     while not self.__stopevent.isSet(  ):
#                         self.__stopevent.wait(0.1)
                    
#                     self.__connection.shutdown(2) 
#                     self.__connection.close()
                    print('Prior connection thread complete')
                    
                except:
                    print ('Threaded port listner interrupted.')
                    
                    
            def stoplistening(self):
                if self.__clientconnected:
                    print('Setting stop event')
                    self.__stopevent.set()
                    print('Set stop event')
                else:
                    self.__stopevent.set()
                    #raise RuntimeError('killed listener')
                
            @property
            def isclientconnected(self):
                return self.__clientconnected
            
            @property
            def getconnection(self):
                return self.__connection
                self.__stopevent.set()
            
            @property
            def getaddress(self):
                return self.__client_address
                
#Initialize variables
def get_now():
    "get the current date and time as a string"
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

payload = {'message': 'Wallplate service initiated' , 'number':'8479519366'}
r = requests.post('http://textbelt.com/text',data=payload)
#print (r.url)
print('Text server response: ', r.text)
        
app = App()

#Create a TCP/IP socket to listen for commands
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  
# Bind the socket to the port
server_address = ('localhost', 10001)
print(sys.stderr, 'Starting up on %s port %s' % (server_address))
sock.bind(server_address)
  
  
# Listen for incoming connections
sock.listen(1)

#Pick up interruptions
def sigterm_handler(_signo, _stack_frame):
    "When sysvinit sends the TERM signal,  before exiting."
    print("[" + get_now() + "] received signal {}, exiting...".format(_signo))
    app.cleanup()
    sys.exit(0)
    
signal.signal(signal.SIGTERM, sigterm_handler)


try:
    reachedend = False
    mainlastoff = True
    if app.GarageOpen():
        print('Garage is open')
    else:
        print('Garage is closed')
    
    garagelastopen = False
    stringresponse = ''
    
    #Kick off thread to listen to port
    portlistenthread1 = ListenThread("portlistener")
    portlistenthread1.start()
        
    print (sys.stderr, 'Waiting for a connection. ', 'Wall plate armed.')
    
    while True:
        #Main Loop
        #Loop listens for connections on the port and for events from the switches
        
        #Check in on status of main switch
        if app.SwitchValue() == False and mainlastoff:
            print ('Main swtich activated.')
            app.RunSwitchProgram()
            mainlastoff = False
            
        if app.SwitchValue() == True and not mainlastoff:
            #Run actions for switch off
            print('Main switch deactivated')
            app.KillAll()
            mainlastoff = True
        
        if app.GarageOpen() == True and not garagelastopen:
            print ('Garage opened')
            app.LEDBlink(0, 0.15, 0, 0, 0, 100, False)
            garagelastopen = True
            
        if app.GarageOpen() == False and garagelastopen:
            #Run actions for switch off
            print('Garage closed')
            app.KillLED(0)
            garagelastopen = False
        
        #Check in on thread to see if a client has connected
        if portlistenthread1.isclientconnected:
            client_address = portlistenthread1.getaddress
            conn = portlistenthread1.getconnection
      
            try:
                print (sys.stderr, 'connection from', client_address)
                stringresponse = ''
                # Receive the data in small chunks and retransmit it
                while (not reachedend):
                    #print (reachedend)
                    data = conn.recv(1032)
                    chunk = data.decode('UTF-8').strip()
                    stringresponse += chunk
#                     print ('received "%s"' % chunk)
                    
                    
                    if stringresponse[-5:] == '*END*': 
#                         print('got to the end')
                        print("Length of data received: ",str(len(stringresponse)))
#                         print ('Endstring: ', stringresponse)
                        reachedend = True 
                    
                    if reachedend:
#                         print ('no more data from', client_address)
                        returnmessage = u'Got message.  Initiating program*END*'
                        #returnmessage = 'received message: ' + stringresponse + ', Initiating Program*END*'
#                         print ('sending response back to the client: ', returnmessage)
#                         conn.sendall(b'Got message.  Initiating program*END*')                         
#                         conn.sendall(bytes(returnmessage, 'UTF-8'))
                        conn.sendall(bytes(returnmessage, 'UTF-8'))
#                         print("final parameter string: ", stringresponse)
                        parameterstring = stringresponse[:-5]
                        
                        #Wait for the client to close the connection and then close on the server side
                        #Todo  put a timer on this
                        data = None
                        print('waiting for client to close connection')
                        while True:
                            try:
                                data = conn.recv(16)
                            except:
                                break
                            finally:
                                if not data:
                                    break
                    
                        conn.close()
                        print('connection closed')
                
                reachedend = False
                      
            except Exception as inst:
                print("Unexpected Error: ", sys.exc_info()[0])
                print(type(inst))
                print(inst.args)
                print(inst)
            
            finally:
                app.RunWebCommands(parameterstring)
                #print('commands submitted')
                print("finallyyy")
                 
                #sendSMS()
#                 print (resp)
                print("finally")
                
                #start a new listening thread
                portlistenthread1 = ListenThread("portlistener")
                portlistenthread1.start()
        
        time.sleep(0.1)
      
#except KeyboardInterrupt:

finally:
    print('Shutting down')
    #Stop listening
    if portlistenthread1.is_alive():
        portlistenthread1.stoplistening()
        #portlistenthread1.join()
    
    sock.shutdown(2)
    sock.close()
    app.cleanup()
    portlistenthread1 = None
    print('Done with everything')
    conn = None
    sock = None
    app = None
    sys.exit(0)
