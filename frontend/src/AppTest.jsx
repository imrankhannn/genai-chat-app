import { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";

export default function App() {
  
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hi! Ask me anything about your documents.",
      time: getTime()
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const [sessionId, setSessionId] = useState(() =>
  crypto.randomUUID()
);


  const chatEndRef = useRef(null);

  // auto scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  function getTime() {
    return new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit"
    });
  }

  // typing animation (SAFE)
  const typeAssistantMessage = (text) => {
    let index = 0;

    // add empty assistant bubble first
    setMessages(prev => [
      ...prev,
      { role: "assistant", content: "", time: getTime() }
    ]);

    const interval = setInterval(() => {
      index++;

      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          content: text.slice(0, index)
        };
        return updated;
      });

      if (index >= text.length) {
        clearInterval(interval);
      }
    }, 20);
  };

  const startNewSession = () => {
  setSessionId(crypto.randomUUID());
  setMessages([
    {
      role: "assistant",
      content: "New session started. Ask me anything about your documents.",
      time: getTime()
    }
  ]);
};

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput("");

    // add user message
    setMessages(prev => [
      ...prev,
      { role: "user", content: userMessage, time: getTime() }
    ]);

    setIsLoading(true);

    // allow typing indicator to render
    await new Promise(r => setTimeout(r, 0));

    try {
      const res = await fetch("http://localhost:8000/ask-rag-chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
  question: userMessage,
  session_id: sessionId
})
      });

      const data = await res.json();

      typeAssistantMessage(data.answer || "No response from server");
    } catch {
      typeAssistantMessage("⚠️ Error connecting to server");
    } finally {
      setIsLoading(false);
    }
  };

  return (
  <div style={styles.page}>
    <div style={styles.container}>
      {/* session bar */}
      <div style={styles.sessionBar}>
        <span>Session:</span>
        <code>{sessionId.slice(0, 8)}</code>
        <button onClick={startNewSession}>New Chat</button>
      </div>

      {/* chat box */}
      <div style={styles.chatBox}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              ...styles.message,
              ...(msg.role === "user"
                ? styles.userMessage
                : styles.assistantMessage)
            }}
          >
            <ReactMarkdown>{msg.content}</ReactMarkdown>
            <div style={styles.time}>{msg.time}</div>
          </div>
        ))}

        {isLoading && (
          <div style={styles.typing}>Agent is typing…</div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* input */}
      <div style={styles.inputBox}>
        <input
          style={styles.input}
          value={input}
          disabled={isLoading}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && sendMessage()}
          placeholder="Type your question…"
        />
        <button
          style={styles.sendButton}
          onClick={sendMessage}
          disabled={isLoading}
        >
          Send
        </button>
      </div>
    </div>
  </div>
);

}

const styles = {
  page: {
    height: "100vh",
    background: "#f4f6fb",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontFamily: "Inter, system-ui, Arial"
  },

  container: {
    width: "100%",
    maxWidth: 900,
    height: "90vh",
    background: "#ffffff",
    display: "flex",
    flexDirection: "column",
    borderRadius: 12,
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
    overflow: "hidden"
  },

  sessionBar: {
    padding: "10px 16px",
    borderBottom: "1px solid #eee",
    display: "flex",
    alignItems: "center",
    gap: 10,
    fontSize: "0.85rem",
    background: "#fafafa"
  },

  chatBox: {
    flex: 1,
    padding: 20,
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: 12,
    background: "#f9fafb"
  },

  message: {
    maxWidth: "75%",
    padding: "12px 14px",
    borderRadius: 12,
    fontSize: "0.95rem",
    lineHeight: 1.5,
    wordBreak: "break-word"
  },

  userMessage: {
    alignSelf: "flex-end",
    background: "#4f46e5",
    color: "#ffffff",
    borderBottomRightRadius: 4
  },

  assistantMessage: {
    alignSelf: "flex-start",
    background: "#e5e7eb",
    color: "#111827",
    borderBottomLeftRadius: 4
  },

  time: {
    fontSize: "0.7rem",
    opacity: 0.6,
    marginTop: 6,
    textAlign: "right"
  },

  typing: {
    fontStyle: "italic",
    fontSize: "0.85rem",
    color: "#6b7280",
    marginLeft: 4
  },

  inputBox: {
    display: "flex",
    padding: 14,
    borderTop: "1px solid #eee",
    background: "#ffffff"
  },

  input: {
    flex: 1,
    padding: "10px 12px",
    fontSize: "0.95rem",
    borderRadius: 8,
    border: "1px solid #ddd",
    outline: "none"
  },

  sendButton: {
    marginLeft: 10,
    padding: "10px 16px",
    borderRadius: 8,
    border: "none",
    background: "#4f46e5",
    color: "#fff",
    cursor: "pointer",
    fontSize: "0.9rem"
  }
};

