import React, { useState } from "react";

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select an audio file");
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const form = new FormData();
      form.append("file", file);
      
      const resp = await fetch("http://localhost:8000/separate/", {
        method: "POST",
        body: form,
      });
      
      if (!resp.ok) {
        throw new Error("Failed to process audio file");
      }
      
      const data = await resp.json();
      
      // Check if there's an error in the response
      if (data.error) {
        throw new Error(data.error);
      }
      
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadFile = (filename, label) => {
    const url = `http://localhost:8000/download/${filename}`;
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
      <h2>Vocal Removal</h2>
      <form onSubmit={handleSubmit}>
        <input 
          type="file" 
          accept="audio/*" 
          onChange={handleFileChange}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !file}>
          {loading ? "Processing..." : "Separate"}
        </button>
      </form>
      
      {error && (
        <div style={{ color: "red", marginTop: "10px" }}>
          Error: {error}
        </div>
      )}
      
      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>Results:</h3>
          <div style={{ marginTop: "10px" }}>
            <button onClick={() => downloadFile(result.vocals, "Vocals")}>
              Download Vocals
            </button>
          </div>
          <div style={{ marginTop: "10px" }}>
            <button onClick={() => downloadFile(result.instrumental, "Instrumental")}>
              Download Instrumental
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
