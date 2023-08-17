import React, { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');

  const handleAskQuestion = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question })
      });

      const data = await response.json();
      setResponse(data.response);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chat App</h1>
        <input
          type="text"
          placeholder="Enter your question"
          value={question}
          onChange={e => setQuestion(e.target.value)}
        />
        <button onClick={handleAskQuestion}>Ask</button>
        {response && (
          <div className="response">
            <p>Response:</p>
            <p>{response}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
