// frontend/src/components/ChatWindow.js
import React, { useState, useEffect, useRef } from "react";
import "./ChatWindow.css";
import { marked } from "marked";

// Support both Vite and CRA environment variables; defaults to http://127.0.0.1:8000
const API_BASE =
  (typeof import.meta !== "undefined" && import.meta.env && import.meta.env.VITE_API_BASE) ||
  (typeof process !== "undefined" && process.env && process.env.REACT_APP_API_BASE) ||
  "http://127.0.0.1:8000";

function ChatWindow() {
  // Default messages
  const defaultMessage = [
    { role: "assistant", content: "Hi, how can I help you today?" }
  ];

  const [messages, setMessages] = useState(defaultMessage);
  const [input, setInput] = useState("");
  const [provider, setProvider] = useState("openai"); // Model provider
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);

  // Scroll to the bottom
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Call backend API
  const callBackend = async (messageText, providerName) => {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: messageText,
        provider: providerName
      })
    });
    if (!res.ok) {
      return { response: `Server error: ${res.status}` };
    }
    return await res.json();
  };

  // Send a message
  const handleSend = async (inputText) => {
    const text = (inputText || "").trim();
    if (!text || sending) return;

    setSending(true);

    // Add user message first
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setInput("");

    try {
      const data = await callBackend(text, provider);
      const reply = (data && data.response) || "(No response content)";
      setMessages((prev) => [...prev, { role: "assistant", content: reply }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Request failed: ${String(err)}` }
      ]);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="messages-container">
      {/* Toolbar: model selection */}
      <div className="toolbar" style={{ display: "flex", gap: 8, marginBottom: 8 }}>
        <label style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <span>Model:</span>
          <select
            value={provider}
            onChange={(e) => setProvider(e.target.value)}
          >
            <option value="openai">OpenAI</option>
            <option value="deepseek">DeepSeek</option>
          </select>
        </label>
        <span style={{ marginLeft: "auto", opacity: 0.7, fontSize: 12 }}>
          API: {API_BASE}
        </span>
      </div>

      {/* Chat messages */}
      {messages.map((message, index) => (
        <div key={index} className={`${message.role}-message-container`}>
          {message.content && (
            <div className={`message ${message.role}-message`}>
              <div
                dangerouslySetInnerHTML={{
                  __html: marked(message.content).replace(/<p>|<\/p>/g, "")
                }}
              />
            </div>
          )}
        </div>
      ))}
      <div ref={messagesEndRef} />

      {/* Input area */}
      <div className="input-area">
        <input
          type="text"
          value={input}
          disabled={sending}
          onChange={(e) => setInput(e.target.value)}
          placeholder={sending ? "Sending..." : "Type a message..."}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend(input);
            }
          }}
        />
        <button
          className="send-button"
          disabled={sending}
          onClick={() => handleSend(input)}
        >
          {sending ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;
