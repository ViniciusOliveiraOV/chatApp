import React, { useState, useEffect, useCallback } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [username, setUsername] = useState("");
  const [socket, setSocket] = useState(null);
	
  const closeSocket = useCallback(() => { 
    if (socket) { 
      console.log("Closing webSocket connection");
      socket.close();
    }
  }, [socket]);



  useEffect(() => {
    if (username) {
      console.log(`Establishing WebSocket connection for ${username}`);
      const newSocket = new WebSocket(`ws://localhost:8000/ws/${username}`);
      setSocket(newSocket);

      newSocket.onopen = () => { 
        console.log("WebSocket connection established");
      }; 

      newSocket.onmessage = (event) => {
        try { 
          const message = JSON.parse(event.data);
          console.log("Received message:", message);
          setMessages((prev) => [...prev, message])
        } catch (error) { 
          console.error("Error parsing message:", error);
        }
      };

      newSocket.onerror = (error) => { 
        console.error("WebSocket error:", error);
      };

      newSocket.onclose = () => { 
        console.log("WebSocket connection closed");
      }; 
      
      setSocket(newSocket);
      
      return() => { 
        closeSocket();
      };
    }
  }, [username, closeSocket]);
	

  const sendMessage = () => {
    if (socket && socket.readyState === WebSocket.OPEN && input) {
      console.log("Sending message:", input);
      socket.send(input);
      setInput("");
    } else { 
      console.warn("Cannot send message, WebSocket is not open or input is empty");
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
    
