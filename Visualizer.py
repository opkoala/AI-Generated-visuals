import numpy as np
import matplotlib.pyplot as plt
import librosa
import pytube
import sounddevice as sd

# Get the YouTube link from the user
youtube_link = input("Enter YouTube video link: ")

# Download the YouTube video as an audio file
youtube = pytube.YouTube(youtube_link)
audio_stream = youtube.streams.filter(only_audio=True).first()
download_name = audio_stream.download()

# Load the downloaded audio file
audio_data, sample_rate = librosa.load(download_name, sr=None)

CHUNK = 1024  # Number of samples per chunk

plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
x = np.arange(0, CHUNK)  # x-axis for the plot
line, = ax.plot(x, np.zeros(CHUNK))
ax.set_xlim(0, CHUNK)
ax.set_ylim(-1, 1)  # Adjust based on your audio input range

# Start playing the audio
sd.play(audio_data[:CHUNK], sample_rate)

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

sd.stop()  # Stop audio playback

plt.close(fig)
