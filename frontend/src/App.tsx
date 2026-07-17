import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  const upload = async () => {
    if (!file) return;

    const data = new FormData();
    data.append("file", file);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/upload",
        data
      );

      setMessage(res.data.message);
    } catch (err) {
      console.error(err);
      setMessage("Upload failed");
    }
  };

  return (
    <div style={{ padding: 40 }}>
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

      <button onClick={upload}>Upload Video</button>

      <h2>{message}</h2>
    </div>
  );
}

export default App;