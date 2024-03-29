"""
Send File Using MQTT
"""
import time
from paho import mqtt
import paho.mqtt.client as paho
import hashlib
broker="81cf89a9dcfd4d4bba3d76caec233fde.s1.eu.hivemq.cloud"#this is provided by broker
#broker="iot.eclipse.org"
#broker="192.168.59.182"
#filename="DSCI0027.jpg"
filename="out.wav" #file to send
topic="encyclopedia/audio"
qos=1
data_block_size=2000
fo=open(filename,"rb")
fout=open("1out.txt","wb") #use a different filename

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# for outfile as I'm rnning sender and receiver together
def process_message(msg):
   """ This is the main receiver code
   """
   if len(msg)==200: #is header or end
      msg_in=msg.decode("utf-8")
      msg_in=msg_in.split(",,")
      if msg_in[0]=="end": #is it really last packet?
         in_hash_final=in_hash_md5.hexdigest()
         if in_hash_final==msg_in[2]:
            print("File copied OK -valid hash  ",in_hash_final)
         else:
            print("Bad file receive   ",in_hash_final)
         return False
      else:
         if msg_in[0]!="header":
            in_hash_md5.update(msg)
            return True
         else:
            return False
   else:
      in_hash_md5.update(msg)
      return True
#define callback
def on_message(client, userdata, message):
   time.sleep(1)
   #print("received message =",str(message.payload.decode("utf-8")))
   if process_message(message.payload):
      fout.write(message.payload)

def on_publish(client, userdata, mid):
    #logging.debug("pub ack "+ str(mid))
    client.mid_value=mid
    client.puback_flag=True  


def wait_for(client,msgType,period=0.25,wait_time=40,running_loop=False):
    client.running_loop=running_loop #if using external loop
    wcount=0  
    while True:
        #print("waiting"+ msgType)
        if msgType=="PUBACK":
            if client.on_publish:        
                if client.puback_flag:
                    return True
     
        if not client.running_loop:
            client.loop(.01)  #check for messages manually
        time.sleep(period)
        #print("loop flag ",client.running_loop)
        wcount+=1
        if wcount>wait_time:
            print("return from wait loop taken too long")
            return False
    return True 

def send_header(filename):
   header="header"+",,"+filename+",,"
   header=bytearray(header,"utf-8")
   header.extend(b','*(200-len(header)))
   print(header)
   c_publish(client,topic,header,qos)

def send_end(filename):
   end="end"+",,"+filename+",,"+out_hash_md5.hexdigest()
   end=bytearray(end,"utf-8")
   end.extend(b','*(200-len(end)))
   print(end)
   c_publish(client,topic,end,qos)

def c_publish(client,topic,out_message,qos):
   res,mid=client.publish(topic,out_message,qos)#publish
   if res==0: #published ok
      if wait_for(client,"PUBACK",running_loop=True):
         if mid==client.mid_value:
            print("match mid ",str(mid))
            client.puback_flag=False #reset flag
         else:
            raise SystemExit("not got correct puback mid so quitting")
         
      else:
         raise SystemExit("not got puback so quitting")
#client= paho.Client("client-001")  #create client object client1.on_publish = on_publish                          #assign function to callback client1.connect(broker,port)                                 #establish connection client1.publish("data/files","on")  
######
client = paho.Client(client_id="clientId-mPCgzR0zxN", userdata=None, protocol=paho.MQTTv5)#client ID is from broker
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("username", "password")
client.on_message=on_message
client.on_publish=on_publish
client.puback_flag=False #use flag in publish ack
client.mid_value=None
#####
print("connecting to broker ",broker)
client.connect(broker,8883)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe(topic)#subscribe
time.sleep(2)
start=time.time()
print("publishing ")
send_header(filename)
Run_flag=True
count=0
##hashes
out_hash_md5 = hashlib.md5()
in_hash_md5 = hashlib.md5()

while Run_flag:
   chunk=fo.read(data_block_size) # change if want smaller or larger data blcoks
   if chunk:
      out_hash_md5.update(chunk)
      out_message=chunk
      #print(" length =",type(out_message))
      c_publish(client,topic,out_message,qos)
         
   else:
      #send hash
      out_message=out_hash_md5.hexdigest()
      send_end(filename)
      #print("out Message ",out_message)
      res,mid=client.publish("data/files",out_message,qos=1)#publish
      Run_flag=False
time_taken=time.time()-start
print("took ",time_taken)
time.sleep(4)
client.disconnect() #disconnect
client.loop_stop() #s
fout.close() #close files
fo.close()
