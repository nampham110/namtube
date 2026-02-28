from flask import Flask, request, jsonify, send_from_directory
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/transcript")
def transcript():
    video_id = request.args.get("id")

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Lấy transcript đầu tiên khả dụng
        transcript = transcript_list.find_transcript(
            [t.language_code for t in transcript_list]
        )

        detected_language = transcript.language_code
        transcript_data = transcript.fetch()

        result = []

        for line in transcript_data:
            original = line['text']

            # Nếu không phải tiếng Việt thì dịch sang Việt
            if detected_language != "vi":
                translated = GoogleTranslator(
                    source='auto',
                    target='vi'
                ).translate(original)
            else:
                translated = original

            result.append({
                "original": original,
                "translated": translated,
                "start": line['start'],
                "duration": line['duration']
            })

        return jsonify({
            "language": detected_language,
            "data": result
        })

    except TranscriptsDisabled:
        return jsonify({"error": "Transcript disabled"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
