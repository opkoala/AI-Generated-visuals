import numpy as np
import matplotlib.pyplot as plt
import librosa

# Load the audio file
download_name = "/full/path/to/Audio.mp3"
audio_data, sample_rate = librosa.load(download_name)

CHUNK = 1024  # Number of samples per chunk

plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
x = np.arange(0, CHUNK)  # x-axis for the plot
line, = ax.plot(x, np.zeros(CHUNK))
ax.set_xlim(0, CHUNK)
ax.set_ylim(-1, 1)  # Adjust based on your audio input range

# Start playing the audio
# Add your audio playback code here

while True:
    # Update the plot with the new audio signal
    audio_signal = audio_data[:CHUNK]
    line.set_ydata(audio_signal)
    fig.canvas.draw()
    fig.canvas.flush_events()

    # Remove the plotted samples from the audio data
    audio_data = audio_data[CHUNK:]

    if len(audio_data) < CHUNK:
        # End of the audio file
        break

# Stop playing the audio
# Add your audio stop code here

plt.close(fig)
