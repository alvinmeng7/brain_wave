import socket
import sys
import time
import argparse
import signal
import struct
import os
import json
import pyaudio
import sounddevice as sd
import numpy as np
from datetime import datetime

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 1500

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                output=True)

# Print received message to console
def print_message(*args):
    try:
        print(args[0]) #added to see raw data 
        obj = json.loads(args[0].decode())
        print(obj.get('data'))
    except BaseException as e:
        print(e)
 #  print("(%s) RECEIVED MESSAGE: " % time.time() +
 # ''.join(str(struct.unpack('>%df' % int(length), args[0]))))

# Clean exit from print mode
def exit_print(signal, frame):
    print("Closing listener")
    sys.exit(0)

# Record received message in text file
def record_to_file(*args):
    textfile.write(str(time.time()) + ",")
    textfile.write(''.join(str(struct.unpack('>%df' % length,args[0]))))
    textfile.write("\n")

# Save recording, clean exit from record mode
def close_file(*args):
    print("\nFILE SAVED")
    textfile.close()
    sys.exit(0)

def fetch_message(*args):
    try:
        #print(args[0]) #added to see raw data
        obj = json.loads(args[0].decode())
        return obj.get('data')
        #print(obj.get('data'))
    except BaseException as e:
        print(e)
    return None

def map_to_0_to_256_int(decoded_data):
    #amplify = 0.1
    arr_num = 0
    channel_data = [0] * len(decoded_data[0])
    for array in decoded_data:
        arr_num += 1
    for idx in range(len(array)):
        channel_data[idx] += array[idx]

    for idx in range(len(channel_data)):
        channel_data[idx] = int(channel_data[idx] / arr_num)

    _min = min(channel_data)
    if _min < 0:
        for idx in range(len(channel_data)):
            channel_data[idx] -= _min

    _min = min(channel_data)
    _max = max(channel_data)
    width  = (_max - _min)/255
    for idx in range(len(channel_data)):
        diff = channel_data[idx] - _min
        channel_data[idx] = int(diff / width)
    return channel_data

def map_to_int(decoded_data):
    #amplify = 0.1
    arr_num = 0
    channel_data = [0.0] * len(decoded_data[0])
    for array in decoded_data:
        arr_num += 1
        for idx in range(len(array)):
            channel_data[idx] += array[idx]

    for idx in range(len(channel_data)):
        channel_data[idx] = channel_data[idx] / arr_num

    for idx in range(len(channel_data)):
        channel_data[idx] = 10 * channel_data[idx]
    '''
    _min = min(channel_data)
    if _min < 0:
        for idx in range(len(channel_data)):
            channel_data[idx] -= _min
    '''
    return channel_data

if __name__ == "__main__":
  # Collect command line arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=12345, help="The port to listen on")
  parser.add_argument("--address",default="/openbci", help="address to listen to")
  parser.add_argument("--option",default="record",help="Debugger option")
  parser.add_argument("--len",default=8,help="Debugger option")
  args = parser.parse_args()

  # Set up necessary parameters from command line
  length = args.len
  if args.option=="print":
      signal.signal(signal.SIGINT, exit_print)
  elif args.option=="record":
      i = 0
      while os.path.exists("udp_test%s.txt" % i):
        i += 1
      filename = "udp_test%i.txt" % i
      textfile = open(filename, "w")
      textfile.write("time,address,messages\n")
      textfile.write("-------------------------\n")
      print("Recording to %s" % filename)
      signal.signal(signal.SIGINT, close_file)

  # Connect to socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_address = (args.ip, args.port)
  sock.bind(server_address)

  # Display socket attributes
  print('--------------------')
  print("-- UDP LISTENER -- ")
  print('--------------------')
  print("IP:", args.ip)
  print("PORT:", args.port)
  print('--------------------')
  print("%s option selected" % args.option)

  # Receive messages
  print("Listening...")
  start = time.time()
  numSamples = 0
  duration = 10
  #while time.time() <= start + duration:
  while True:
    data, addr = sock.recvfrom(32) # buffer size is 20000 bytes
    if args.option=="print":
      #print_message(data)

      decoded_data = fetch_message(data)

      #channel_data = map_to_0_to_256_int(decoded_data)
      channel_data = map_to_int(decoded_data)
      print(datetime.now())

      channel_data = np.repeat(channel_data, RATE/250)

      sd.play(channel_data, RATE)  # 播放
      time.sleep(len(channel_data)/RATE)

      #stream.write(bytes(channel_data))
      numSamples += 1
    elif args.option=="record":
      record_to_file(data)
      print(data)

print( "Samples == {}".format(numSamples) )
print( "Duration == {}".format(duration) )
print( "Avg Sampling Rate == {}".format(numSamples / duration) )
