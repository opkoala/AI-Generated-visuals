import numpy as np
import matplotlib.pyplot as plt
import librosa
import pytube
import sounddevice as sd

# Get the YouTube link from the user
youtube_link = input("Enter YouTube link: ")

# Download the YouTube video as an audio file
youtube = pytube.YouTube(youtube_link)
audio_stream = youtube.streams.filter(only_audio=True).first()
download_name = audio_stream.download()

# Load the downloaded audio file
audio_data, sample_rate = librosa.load(download_name)

CHUNK = 1024  # Number of samples per chunk

plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
x = np.arange(0, CHUNK)  # x-axis for the plot
line, = ax.plot(x, np.zeros(CHUNK))
ax.set_xlim(0, CHUNK)
ax.set_ylim(-1, 1)  # Adjust based on your audio input range

# Compute beat frames using librosa
tempo, beat_frames = librosa.beat.beat_track(audio_data, sr=sample_rate, hop_length=CHUNK)

# Normalize beat frames to range [0, 1]
normalized_beat_frames = (beat_frames - beat_frames.min()) / (beat_frames.max() - beat_frames.min())

# Define color map for transitions based on beat frames
color_map = plt.cm.get_cmap('cool')  # Use 'cool' colormap for color transitions

# Start playing the audio
sd.play(audio_data, sample_rate)

while True:
    # Update the plot with the new audio signal and color
    audio_signal = audio_data[:CHUNK]
    line.set_ydata(audio_signal)

    # Get the current beat frame index
    current_frame = len(audio_data) // CHUNK
    
    # Get the current beat frame color
    current_color = color_map(normalized_beat_frames[current_frame])

    # Set the line color
    line.set_color(current_color)
    
    fig.canvas.draw()
    fig.canvas.flush_events()

    # Remove the plotted samples from the audio data
    audio_data = audio_data[CHUNK:]

    if len(audio_data) < CHUNK:
        # End of the audio file
        break

# Stop playing the audio
sd.stop()

plt.close(fig)

