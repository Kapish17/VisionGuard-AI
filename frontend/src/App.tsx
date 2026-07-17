import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [videoUrl, setVideoUrl] = useState("");
  const [message, setMessage] = useState("");

  const uploadVideo = async () => {
    if (!file) {
      alert("Please select a video.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      setMessage(res.data.message);
      setVideoUrl(res.data.video_url);
    } catch (err) {
      console.error(err);
      alert("Upload failed.");
    }
  };

  return (
    <div
      style={{
        maxWidth: "800px",
        margin: "40px auto",
        textAlign: "center",
      }}
    >
      <h1>VisionGuard AI</h1>

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

      <button onClick={uploadVideo}>Upload Video</button>

      <p>{message}</p>

      {videoUrl && (
        <video
          width="700"
          controls
          style={{ marginTop: "20px", borderRadius: "10px" }}
        >
          <source src={videoUrl} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      )}
    </div>
  );
}

export default App;