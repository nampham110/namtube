from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>NamTube is running</h1>"

@app.route("/transcript")
def transcript():
    video_id = request.args.get("id")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    result = []

    for line in transcript:
        translated = GoogleTranslator(
            source='auto',
            target='vi'
        ).translate(line['text'])

        result.append({
            "original": line['text'],
            "translated": translated,
            "start": line['start'],
            "duration": line['duration']
        })

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
