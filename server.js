const express = require("express");
const { YoutubeTranscript } = require("youtube-transcript");

const app = express();

app.use(express.static("public"));

app.get("/api/transcript/:id", async (req, res) => {
  try {
    const transcript = await YoutubeTranscript.fetchTranscript(req.params.id);

    const formatted = transcript.map(item => ({
      start: item.offset / 1000,
      end: (item.offset + item.duration) / 1000,
      text: item.text
    }));

    res.json(formatted);
  } catch (err) {
    res.status(500).json({ error: "No transcript available." });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Server running on port", PORT));
