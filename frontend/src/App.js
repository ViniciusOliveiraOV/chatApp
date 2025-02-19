import React, { useState, useEffect } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [username, setUsername] = useState("");
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    if (username) {
      const newSocket = new WebSocket(`ws://localhost:8000/ws/${username}`);
      setSocket(newSocket);

      newSocket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        setMessages((prev) => [...prev, message]);
      };

      return() => newSocket.close();
    }
  }, [username]);

  const sendMessage = () => {
    if (socket && input) {
      socket.send(input);
      setInput("");
    }
  };
  return (
    <div>
      <h1>Chat App</h1>
      <input
        type="text"
        placeholder="Enter your username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
    />
    <div>
      {messages.map((msg, index) => (
        <div key={index}>
            <strong>{msg.username}:</strong> {msg.message}
        </div>
      ))}
    </div>
    <input
      type="text"
      value={input}
      onChange={(e) => setInput(e.target.value)}
    />
    <button onClick={sendMessage}>Send</button>
  </div>
  );
}

export default App;
    