import pyaudio
import numpy as np
import wave

#The following code comes from Shivam Sharma as referenced below
sample_format = pyaudio.paInt16
chunk=1024#4096
RATE=48000
amp_factor=40   #amplification factor
channels=1
seconds=15
filename = "output.wav"
p=pyaudio.PyAudio()

#input stream setup
#change input_device_index from 0 to any number these number defines the index number of sound devices available on pi
stream=p.open(format = pyaudio.paInt16,rate=RATE,channels=1, input_device_index = 1, input=True, frames_per_buffer=chunk)
frames = []
#the code below is from the pyAudio library documentation referenced below
#output stream setup
player=p.open(format = pyaudio.paInt16,rate=RATE,channels=1, output=True, frames_per_buffer=chunk)

for i in range(0, int(RATE / chunk * seconds)):#while True:            #Used to continuously stream audio
     data=(np.fromstring(stream.read(chunk,exception_on_overflow = False),dtype=np.int16)) #if deprecated error occurs then np.fromstring=np.frombuffer
     frames.append(data)# data to record in output.wav
     player.write(amp_factor*data,chunk)#data to play on speaker directly
     #print(chunk)
    
#closes streams
stream.stop_stream()
stream.close()
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
p.terminate
