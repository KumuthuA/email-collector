import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [keyword, setKeyword] = useState("");
  const [numResults, setNumResults] = useState(10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchEmails = async (e) => {
    e.preventDefault();
    setError("");
  
    if (keyword.trim() === "" || numResults <= 0) {
      setError("Please enter a valid keyword and number of results.");
      return;
    }
  
    setLoading(true);
    try {
      const response = await axios.post("/api/emails", {
        keyword,
        num_results: numResults,
      }, { responseType: 'blob' });
  
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${keyword}_emails.csv`);
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      setError("Failed to fetch emails.");
    } finally {
      setLoading(false);
    }
  };  

  return (
    <div className="App">
      <h1>Email Collector</h1>
      <form onSubmit={fetchEmails}>
        <div className="input-group">
          <label htmlFor="Keyword">Enter keywords</label>
          <input
            type="text"
            id="keyword"
            placeholder="Enter keywords"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
          />
        </div>
        <div className="input-group">
          <label htmlFor="numResults">Enter results count</label>
          <input
            type="number"
            id="numResults"
            value={numResults}
            onChange={(e) => setNumResults(Number(e.target.value))}
            placeholder="Number of results"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Fetching..." : "Find Emails"}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;
