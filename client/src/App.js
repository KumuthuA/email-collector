import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  // State variables to manage form input, loading state, and error messages
  const [keyword, setKeyword] = useState("");
  const [numResults, setNumResults] = useState(10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Function to handle form submission and fetch emails from the server
  const fetchEmails = async (e) => {
    e.preventDefault();
    setError("");
  
    // Validate user input
    if (keyword.trim() === "" || numResults <= 0) {
      setError("Please enter a valid keyword and number of results.");
      return;
    }
  
    setLoading(true);
    try {
      // Send a POST request to the server to fetch emails
      const response = await axios.post("/api/emails", {
        keyword,
        num_results: numResults,
      }, { responseType: 'blob' });  // Expecting a CSV file as a blob response
  
      // Create a downloadable link for the CSV file
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${keyword}_emails.csv`);
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      setError("Failed to fetch emails.");  // Handle errors during the fetch
    } finally {
      setLoading(false);  // Ensure loading state is reset
    }
  };

  return (
    <div className="App">
      <h1>Email Collector</h1>
      <form onSubmit={fetchEmails}>
        {/* Input for keyword */}
        <div className="input-group">
          <label htmlFor="keyword">Enter keywords</label>
          <input
            type="text"
            id="keyword"
            placeholder="Enter keywords"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
          />
        </div>
        
        {/* Input for number of results */}
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

        {/* Submit button */}
        <button type="submit" disabled={loading}>
          {loading ? "Fetching..." : "Find Emails"}
        </button>
      </form>
      
      {/* Display error message if any */}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;
