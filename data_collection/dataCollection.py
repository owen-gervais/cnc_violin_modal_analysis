import pyaudio
import numpy as np
from matplotlib import pyplot as plt



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

stream = p.open(format=FORMAT,                                      # Open the audio stream from M4 Soundcard
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=soundcard_index,
                frames_per_buffer=CHUNK)

threshold_data = np.empty((10*CHUNK,))                              # Preallocate the experiment storage

print("Starting Threshold Monitoring..... (DO NOT TOUCH THE SENSORS!)")

for i in range(0, 10):
    in_data = stream.read(CHUNK)
    interleaved_data = np.frombuffer(in_data, dtype=np.float32)     # Transform to float from buffer
    separated_data = np.reshape(interleaved_data, (CHUNK, 2))       # Reshape the numpy array into left and right channels
    threshold_data[(i*CHUNK):((i+1)*CHUNK)] = separated_data[:,1]

baseline_threshold = np.amax(threshold_data)                        # Get the maximum value in the readings in order establish a baseline (SINUSOID)

print("Baseline Threshold Captured! Baseline Reading: {} V".format(baseline_threshold))

impact_offset = 0.01                                                # Impact offset to fight off false readings
impact_threshold = baseline_threshold + impact_offset               # Create the impact threshold

hammer_data = np.empty((3*CHUNK,))                                  # Array preallocation to collect the whole hammer data
accelerometer_data = np.empty((3*CHUNK,))                           # Array preallocation to collect the whole accelorometer data

prev_hammer_data = np.empty((CHUNK,))                               # Array preallocation to store the previous hammer data reading
prev_accelerometer_data = np.empty((CHUNK,))                        # Array preallocation to store the previous accelerometer data reading

print("Starting data acquisition.....")

testNum = 1                                                      # Start counter for first test

try:
    while True:
        in_data = stream.read(CHUNK)                                    # Read in a new full buffer
        interleaved_data = np.frombuffer(in_data, dtype=np.float32)     # Transform to float from buffer
        separated_data = np.reshape(interleaved_data, (CHUNK, 2))       # Reshape the numpy array into left and right channels
        if np.amax(separated_data[:,1]) > impact_threshold: 
            
            post_impact_data = stream.read(CHUNK)                                         # Read in a new buffer after impact
            post_interleaved_data = np.frombuffer(post_impact_data, dtype=np.float32)     # Transform to float from buffer
            post_separated_data = np.reshape(post_interleaved_data, (CHUNK, 2))           # Reshape the numpy array into left and right channels
            
            print("Formatting the experiment data...")

            # Concatenate and direct assign both data points into the preallocated memory space

            accelerometer_data[0:CHUNK] = prev_accelerometer_data
            accelerometer_data[CHUNK:2*CHUNK]  = separated_data[:,0]
            accelerometer_data[2*CHUNK:3*CHUNK] = post_separated_data[:,0]

            hammer_data[0:CHUNK] = prev_hammer_data
            hammer_data[CHUNK:2*CHUNK] = separated_data[:,1]
            hammer_data[2*CHUNK:3*CHUNK] = post_separated_data[:,1]

            csv_formatted_data = np.concatenate((hammer_data, accelerometer_data), axis=1)

            fileName = "experiment_data/experiment_data_{}.csv".format(testNum)

            with open(fileName, 'w') as f:
                f.write("Accelerometer {0:d}, Force Sensor {0:d},\n".format(testNum))
                for i in range(0,3*CHUNK):
                    f.write("{0:4.3f}, {1:4.3f},\n".format(csv_formatted_data[i][0], csv_formatted_data[i][1]))

            testNum += 1

        prev_accelerometer_data[0:CHUNK] = separated_data[:,0]          # Assign current reading to the previous accelerometer for collection
        prev_hammer_data[0:CHUNK] = separated_data[:,1]                 # Assign current reading ot the previous hammer for collection

except KeyboardInterrupt:
    print('\n')
    pass

print("Data acquistion completed!")

print("Displaying the latest impact data.....")

# Plot data
plt.figure(1)
plt.subplot(211)
plt.plot(hammer_data)
plt.xlabel("Hammer Readings")

plt.subplot(212)
plt.plot(accelerometer_data)
plt.xlabel("Accelerometer Readings")
plt.show()

stream.stop_stream()                                                # Stop the audio stream and terminate the pyaudio instance
stream.close()                                                      # Close the audio stream

p.terminate()