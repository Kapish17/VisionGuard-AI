import { useState } from "react";
import axios from "axios";

const labels: Record<string, string> = {
  person: "👤 Person",
  bicycle: "🚲 Bicycle",
  car: "🚗 Car",
  motorcycle: "🏍 Motorcycle",
  bus: "🚌 Bus",
  truck: "🚚 Truck",
  backpack: "🎒 Backpack",
  handbag: "👜 Handbag",
  suitcase: "🧳 Suitcase",
  laptop: "💻 Laptop",
  "cell phone": "📱 Cell Phone",
};

function App() {
  const [file, setFile] = useState<File | null>(null);

  const [message, setMessage] = useState("");

  const [originalVideo, setOriginalVideo] = useState("");
  const [processedVideo, setProcessedVideo] = useState("");

  const [summary, setSummary] = useState<Record<string, number>>({});

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
      setSummary(res.data.summary || {});
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
        maxWidth: "1100px",
        margin: "40px auto",
        textAlign: "center",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>🛡️ VisionGuard AI</h1>
      <p>Intelligent CCTV Investigation Assistant using AI</p>

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
          padding: "12px 28px",
          cursor: "pointer",
          fontSize: "16px",
          borderRadius: "8px",
        }}
      >
        {loading ? "Processing Video..." : "Upload & Detect"}
      </button>

      <br />
      <br />

      {loading && <h3>🔍 Running YOLOv8 AI Detection...</h3>}

      <h3>{message}</h3>

      {originalVideo && (
        <>
          <hr />

          <h2>📹 Original Video</h2>

          <video width="850" controls style={{ borderRadius: "10px" }}>
            <source src={originalVideo} type="video/mp4" />
          </video>
        </>
      )}

      {processedVideo && (
        <>
          <hr />

          <h2>🤖 AI Detection Result</h2>

          <video width="850" controls style={{ borderRadius: "10px" }}>
            <source src={processedVideo} type="video/mp4" />
          </video>
        </>
      )}

      {Object.keys(summary).length > 0 && (
        <>
          <hr />

          <h2>📊 CCTV Detection Dashboard</h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit,minmax(190px,1fr))",
              gap: "18px",
              marginTop: "25px",
            }}
          >
            {Object.entries(summary).map(([name, count]) => (
              <div
                key={name}
                style={{
                  background: "#ffffff",
                  borderRadius: "15px",
                  padding: "22px",
                  border: "1px solid #ddd",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
                }}
              >
                <h3
                  style={{
                    marginBottom: "12px",
                    color: "#333",
                    fontSize: "18px",
                  }}
                >
                  {labels[name] || name}
                </h3>

                <div
                  style={{
                    fontSize: "38px",
                    fontWeight: "bold",
                    color: count > 0 ? "#007BFF" : "#999",
                  }}
                >
                  {count}
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default App;