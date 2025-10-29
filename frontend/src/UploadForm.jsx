import React, { useState } from "react";
import "./UploadForm.css";

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState("");
  const clientId = Math.random().toString(36).substring(7);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
    setResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select an audio file");
      return;
    }
    
    setLoading(true);
    setError(null);
    setProgress(0);
    setResult(null);
    setProgressMessage("Uploading file...");
    
    try {
      // Simulate progress updates since WebSocket might not work on Render free tier
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) return prev;
          return prev + Math.random() * 10;
        });
      }, 2000);
      
      const form = new FormData();
      form.append("file", file);
      
      setProgressMessage("Processing audio... This may take 5-6 minutes for high quality.");
      
      const resp = await fetch(`https://vocal-removal-app.onrender.com/separate/${clientId}`, {
        method: "POST",
        body: form,
      });
      
      clearInterval(progressInterval);
      
      if (!resp.ok) {
        throw new Error("Failed to process audio file");
      }
      
      const data = await resp.json();
      
      // Check if there's an error in the response
      if (data.error) {
        throw new Error(data.error);
      }
      
      setProgress(100);
      setProgressMessage("Separation complete!");
      setResult(data);
    } catch (err) {
      setError(err.message);
      setProgress(0);
    } finally {
      setLoading(false);
    }
  };

  const downloadFile = (filename, label) => {
    const url = `https://vocal-removal-app.onrender.com/download/${filename}`;
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="upload-container">
      <div className="sith-glow"></div>
      
      <div className="header">
        <h1 className="title">
          <span className="sith-text">DARK SIDE</span>
          <span className="subtitle">Vocal Separation System</span>
        </h1>
        <p className="tagline">"The Force is strong with this one..."</p>
      </div>

      <form onSubmit={handleSubmit} className="upload-form">
        <div className="file-input-wrapper">
          <input 
            type="file" 
            accept="audio/*,audio/mp3,audio/mpeg" 
            onChange={handleFileChange}
            disabled={loading}
            id="file-input"
            className="file-input"
          />
          <label htmlFor="file-input" className="file-label">
            <span className="file-icon">🎵</span>
            <span className="file-text">
              {file ? file.name : "Choose your destiny... (Select Audio File)"}
            </span>
          </label>
        </div>

        <button 
          type="submit" 
          disabled={loading || !file}
          className={`submit-button ${loading ? 'processing' : ''}`}
        >
          <span className="button-text">
            {loading ? "⚔️ EXECUTING..." : "⚔️ INITIATE SEPARATION"}
          </span>
          <span className="button-glow"></span>
        </button>
      </form>

      {loading && (
        <div className="progress-container">
          <div className="progress-label">{progressMessage}</div>
          <div className="progress-bar-wrapper">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${Math.max(0, progress)}%` }}
              >
                <div className="lightsaber-glow"></div>
              </div>
            </div>
            <div className="progress-percentage">{Math.max(0, progress)}%</div>
          </div>
          <div className="loading-text">
            <span className="pulse">●</span> The Dark Side is processing your file...
          </div>
        </div>
      )}
      
      {error && (
        <div className="error-message">
          <div className="error-icon">⚠️</div>
          <div className="error-text">
            <strong>Disturbance in the Force:</strong><br />
            {error}
          </div>
        </div>
      )}
      
      {result && !loading && (
        <div className="results-container">
          <h3 className="results-title">
            <span className="success-icon">✓</span> Separation Complete
          </h3>
          
          <div className="download-grid">
            <div className="download-card vocals">
              <div className="card-header">
                <span className="card-icon">🎤</span>
                <span className="card-title">Vocals</span>
              </div>
              <div className="card-filename">{result.vocals}</div>
              
              {/* Audio Player */}
              <div className="audio-player-wrapper">
                <audio 
                  controls 
                  className="audio-player"
                  src={`https://vocal-removal-app.onrender.com/download/${result.vocals}`}
                >
                  Your browser does not support the audio element.
                </audio>
              </div>
              
              <button 
                onClick={() => downloadFile(result.vocals, "Vocals")}
                className="download-button"
              >
                <span className="download-icon">⬇</span>
                Download Vocals
              </button>
            </div>

            <div className="download-card instrumental">
              <div className="card-header">
                <span className="card-icon">🎸</span>
                <span className="card-title">Instrumental</span>
              </div>
              <div className="card-filename">{result.instrumental}</div>
              
              {/* Audio Player */}
              <div className="audio-player-wrapper">
                <audio 
                  controls 
                  className="audio-player"
                  src={`https://vocal-removal-app.onrender.com/download/${result.instrumental}`}
                >
                  Your browser does not support the audio element.
                </audio>
              </div>
              
              <button 
                onClick={() => downloadFile(result.instrumental, "Instrumental")}
                className="download-button"
              >
                <span className="download-icon">⬇</span>
                Download Instrumental
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="footer">
        <p className="force-quote">"Much to learn, you still have."</p>
      </div>
    </div>
  );
}
