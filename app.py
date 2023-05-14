from flask import Flask, render_template, request, redirect, send_file
import pytube, os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
     # get the YouTube video link from the form
    video_url = request.form['video_url']

    # create a YouTube object and extract the audio stream
    youtube = pytube.YouTube(video_url)
    audio_stream = youtube.streams.filter(only_audio=True).first()

    # set the filename to the video title
    filename = youtube.title + ".mp3"

    # download the audio stream as an MP3 file
    audio_stream.download(output_path=".", filename=filename)

    # return the MP3 file to the user for download
    response = send_file(filename, as_attachment=True)

    # remove the file from the file system
    os.remove(filename)

    return response

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)