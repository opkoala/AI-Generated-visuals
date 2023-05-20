from flask import Flask, render_template, request, url_for, redirect, send_file, session
from pytube import YouTube
from io import BytesIO
import pydub

app = Flask(__name__)
app.config['SECRET_KEY'] = "654c0fb3968af9d5e6a9b3edcbc7051b"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            return render_template("error.html")
        return render_template("download.html", url=url)
    return render_template("home.html")

@app.route("/download", methods=["GET", "POST"])
def download_audio():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        audio = url.streams.get_audio_only()
        audio.stream_to_buffer(buffer)
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name="/full/path/to/Audio.mp3"
, mimetype="audio/mpeg")
    
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)

