import pyaudio
import wave 
import numpy as np
from matplotlib import pyplot as plt
import csv
from circularBuffer import CircularBuffer

p = pyaudio.PyAudio()

# Get Device Index for M4 Soundcard
for device in range(0, p.get_device_count()):
    if p.get_device_info_by_index(device)['name'] == "M4":
        soundcard_index = device

# Audio Sampling Parameters
CHUNK = 256                     # Number of frames the signal is broken into
FORMAT = pyaudio.paFloat32      # Format of sampling
CHANNELS = 2                    # Channels to be monitored by the pyaudio stream
RATE = 44100                    # Sampling rate of pyaudio stream
RECORD_SECONDS = 1              # Record time for fixed rates

# Open the audio stream from M4 Soundcard
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=soundcard_index,
                frames_per_buffer=CHUNK)

print("* recording")

experiment_data = np.empty((0, 2)) # Preallocate the experiment storage

threshold = 0.002 # Impact threshold

impact_cb = CircularBuffer(2) # Store two samples

# Main loop monitoring for input to be below threshold
while True:
    in_data = stream.read(CHUNK)                               # Read in a full buffer
    interleaved = np.frombuffer(in_data, dtype=np.float32)     # Transform to float from buffer
    result = np.reshape(interleaved, (CHUNK, 2))               # Reshape the numpy array into left and right channels
    
    if (result[:,1] >= threshold).sum() > 20:                  # Trigger if there is presence of a spike in the buffer
        
        impact_cb.update(result[:,1])                          # Add new data to the circular buffer

        after_strike = stream.read(CHUNK)                                     # Read another chunk to complete the pulse
        interleaved_after = np.frombuffer(after_strike, dtype=np.float32)     # Transform to float from buffer
        result_after = np.reshape(interleaved_after, (CHUNK, 2))              # Reshape the numpy array into left and right channels
        
        experiment_data = np.concatenate((impact_cb.content[1],impact_cb.content[0],result_after[:,1]))   # Concatenate all results into a experiement data object
        
        break
    
    impact_cb.update(result[:,1]) # Keep adding impact data to circular buffer

print("* done")

# Plot data
plt.plot(experiment_data)
plt.show()

# Stop the audio stream and terminate the pyaudio instance
stream.stop_stream()    
stream.close()

p.terminate()
