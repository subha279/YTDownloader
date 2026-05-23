from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

# Create Flask app
app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    url = request.form["url"]
    media_type = request.form["type"]

    video_quality = request.form.get("quality", "720")
    mp3_quality = request.form.get("mp3_quality", "320")

    file_id = str(uuid.uuid4())

    if media_type == "mp3":

        options = {
            "format": "bestaudio",
            "outtmpl": f"{DOWNLOAD_FOLDER}/{file_id}.%(ext)s",

            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": mp3_quality
            }]
        }

        extension = ".mp3"

    else:

        options = {
            "format": f"bestvideo[height<={video_quality}]+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": f"{DOWNLOAD_FOLDER}/{file_id}.%(ext)s"
        }

        extension = ".mp4"

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    files = os.listdir(DOWNLOAD_FOLDER)

    newest = max(
        [os.path.join(DOWNLOAD_FOLDER, f) for f in files],
        key=os.path.getctime
    )

    return send_file(
        newest,
        as_attachment=True,
        download_name=f"download{extension}"
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
