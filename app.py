from flask import Flask, request, jsonify, send_from_directory
from youtube_transcript_api import YouTubeTranscriptApi
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/transcript")
def transcript():
    video_id = request.args.get("id")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    result = []
    for line in transcript[:30]:
        original = line['text']
        translated = GoogleTranslator(source='auto', target='vi').translate(original)
        result.append({
            "original": original,
            "translated": translated
        })

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
