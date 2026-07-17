import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState<File | null>(null);

  const [message, setMessage] = useState("");

  const [originalVideo, setOriginalVideo] = useState("");
  const [processedVideo, setProcessedVideo] = useState("");

  const [loading, setLoading] = useState(false);

  const uploadVideo = async () => {
    if (!file) {
      alert("Please select a video.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setMessage("");

      const res = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      setMessage(res.data.message);

      setOriginalVideo(res.data.original_video);
      setProcessedVideo(res.data.processed_video);
    } catch (err) {
      console.error(err);
      alert("Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "900px",
        margin: "40px auto",
        textAlign: "center",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>🛡️ VisionGuard AI</h1>

      <p>
        Intelligent CCTV Investigation Assistant using AI
      </p>

      <input
        type="file"
        accept="video/*"
        onChange={(e) => {
          if (e.target.files) {
            setFile(e.target.files[0]);
          }
        }}
      />

      <br />
      <br />

      <button
        onClick={uploadVideo}
        disabled={loading}
        style={{
          padding: "10px 25px",
          cursor: "pointer",
          fontSize: "16px",
        }}
      >
        {loading ? "Processing Video..." : "Upload & Detect"}
      </button>

      <br />
      <br />

      {loading && (
        <h3>🔍 Running YOLO Object Detection...</h3>
      )}

      <h3>{message}</h3>

      {originalVideo && (
        <>
          <hr />

          <h2>📹 Original Video</h2>

          <video
            width="800"
            controls
            style={{
              borderRadius: "10px",
            }}
          >
            <source src={originalVideo} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </>
      )}

      {processedVideo && (
        <>
          <hr />

          <h2>🤖 AI Detection Result</h2>

          <video
            width="800"
            controls
            style={{
              borderRadius: "10px",
            }}
          >
            <source src={processedVideo} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </>
      )}
    </div>
  );
}

export default App;