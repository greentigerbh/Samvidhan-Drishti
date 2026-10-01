from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

BASE_DIR = os.path.expanduser("~/samvidhan_drishti")

WRITINGS_DIR = os.path.join(BASE_DIR, "writings")
DEBATES_DIR = os.path.join(BASE_DIR, "debates")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
VIDEO_DIR = os.path.join(BASE_DIR, "video")
IMAGES_DIR = os.path.join(BASE_DIR, "images")


def get_files(folder, extensions):

    if not os.path.exists(folder):
        return []

    result = []

    for root, dirs, files in os.walk(folder):

        for filename in files:

            if filename.lower().endswith(extensions):

                full_path = os.path.join(root, filename)

                relative_path = os.path.relpath(
                    full_path,
                    folder
                )

                result.append(relative_path)

    return sorted(result)


@app.route("/")
def home():

    writings = get_files(
        WRITINGS_DIR,
        (".pdf",)
    )

    debates = get_files(
        DEBATES_DIR,
        (".html", ".htm")
    )

    audio = get_files(
        AUDIO_DIR,
        (".mp3", ".wav", ".ogg", ".m4a", ".aac")
    )

    videos = get_files(
        VIDEO_DIR,
        (".mp4", ".mkv", ".avi", ".mov", ".webm")
    )

    images = get_files(
        IMAGES_DIR,
        (".jpg", ".jpeg", ".png", ".webp", ".gif")
    )

    return render_template(
        "index.html",

        writings=writings,

        debates=debates,

        audio=audio,

        videos=videos,

        images=images,

        writings_count=len(writings),

        debates_count=len(debates),

        audio_count=len(audio),

        video_count=len(videos),

        images_count=len(images)
    )


@app.route("/file/writing/<path:filename>")
def serve_writing(filename):

    return send_from_directory(
        WRITINGS_DIR,
        filename
    )


@app.route("/file/debate/<path:filename>")
def serve_debate(filename):

    return send_from_directory(
        DEBATES_DIR,
        filename
    )


@app.route("/file/audio/<path:filename>")
def serve_audio(filename):

    return send_from_directory(
        AUDIO_DIR,
        filename
    )


@app.route("/file/video/<path:filename>")
def serve_video(filename):

    return send_from_directory(
        VIDEO_DIR,
        filename
    )


@app.route("/file/image/<path:filename>")
def serve_image(filename):

    return send_from_directory(
        IMAGES_DIR,
        filename
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
