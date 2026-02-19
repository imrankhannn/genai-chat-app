import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";

export default function App() {
  const [mode, setMode] = useState("llm"); // llm | doc | web
  const [sessionId, setSessionId] = useState(crypto.randomUUID());
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hi! Ask me anything." }
  ]);
  const [input, setInput] = useState("");
  const [docUploaded, setDocUploaded] = useState(false);
  const [webLoaded, setWebLoaded] = useState(false);
  const [websiteUrl, setWebsiteUrl] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const chatEndRef = useRef(null);
  const API_BASE = import.meta.env.VITE_API_BASE_URL;

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const typeReply = (fullText) => {
    let index = 0;

    setMessages(prev => [...prev, { role: "assistant", content: "" }]);

    const interval = setInterval(() => {
      index++;

      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          content: fullText.slice(0, index)
        };
        return updated;
      });

      if (index >= fullText.length) {
        clearInterval(interval);
        setIsTyping(false);
      }
    }, 20);
  };

  const sendMessage = async () => {
    if (isTyping) return;
    if (!input.trim()) return;

    if (mode === "doc" && !docUploaded) return;
    if (mode === "web" && !webLoaded) return;

    const userMessage = input;
    setInput("");

    setMessages(prev => [...prev, { role: "user", content: userMessage }]);

    let endpoint = "ask-llm";
    if (mode === "doc") endpoint = "ask-doc-chat";
    if (mode === "web") endpoint = "ask-web-chat";

    setIsTyping(true);

    const res = await fetch(`${API_BASE}/${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: userMessage,
        session_id: sessionId
      })
    });

    const data = await res.json();

    if (mode === "llm") {
      typeReply(data.answer);
    } else {
      setMessages(prev => [
        ...prev,
        { role: "assistant", content: data.answer }
      ]);
      setIsTyping(false);
    }
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    await fetch(`${API_BASE}/upload?session_id=${sessionId}`, {
      method: "POST",
      body: formData
    });

    setDocUploaded(true);
    setMessages(prev => [
      ...prev,
      { role: "assistant", content: "Document uploaded successfully." }
    ]);
  };

  const loadWebsite = async () => {
    if (!websiteUrl) return;

    await fetch(`${API_BASE}/load-website`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: websiteUrl,
        session_id: sessionId
      })
    });

    setWebLoaded(true);
    setMessages(prev => [
      ...prev,
      { role: "assistant", content: "Website loaded successfully." }
    ]);
  };

  const newChat = () => {
    setSessionId(crypto.randomUUID());
    setMessages([{ role: "assistant", content: "New chat started." }]);
    setDocUploaded(false);
    setWebLoaded(false);
    setWebsiteUrl("");
    setMode("llm");
  };

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <h2>Multi-Level GenAI</h2>

        <div style={styles.modeBar}>
          <button
            style={mode === "llm" ? styles.active : styles.button}
            onClick={() => setMode("llm")}
          >
            LLM
          </button>

          <button
            style={mode === "doc" ? styles.active : styles.button}
            onClick={() => setMode("doc")}
          >
            Document
          </button>

          <button
            style={mode === "web" ? styles.active : styles.button}
            onClick={() => setMode("web")}
          >
            Website
          </button>

          <button onClick={newChat} style={styles.button}>
            New Chat
          </button>
        </div>

        {mode === "doc" && (
          <div style={styles.upload}>
            <input type="file" accept=".pdf,.txt,.docx" onChange={handleUpload} />
            {!docUploaded && <small>Please upload a document</small>}
          </div>
        )}

        {mode === "web" && (
          <div style={styles.upload}>
            <input
              style={styles.input}
              placeholder="Enter website URL..."
              value={websiteUrl}
              onChange={(e) => setWebsiteUrl(e.target.value)}
            />
            <button style={styles.button} onClick={loadWebsite}>
              Load Website
            </button>
            {!webLoaded && <small>Please load a website</small>}
          </div>
        )}

        <div style={styles.chat}>
          {messages.map((m, i) => (
            <div
              key={i}
              style={m.role === "user" ? styles.userMsg : styles.botMsg}
            >
              <ReactMarkdown>{m.content}</ReactMarkdown>
            </div>
          ))}

          {isTyping && <div style={styles.botMsg}>Assistant is typing…</div>}

          <div ref={chatEndRef} />
        </div>

        <div style={styles.inputBar}>
          <input
            style={styles.input}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") sendMessage();
            }}
            placeholder="Type your question..."
          />

          <button
            style={
              (mode === "doc" && !docUploaded) ||
              (mode === "web" && !webLoaded)
                ? styles.disabledBtn
                : styles.button
            }
            onClick={sendMessage}
            disabled={
              (mode === "doc" && !docUploaded) ||
              (mode === "web" && !webLoaded)
            }
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
    alignItems: "center"
  },

  container: {
    width: "100%",
    maxWidth: 900,
    height: "90vh",
    background: "#fff",
    borderRadius: 12,
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
    display: "flex",
    flexDirection: "column",
    padding: 16,
    fontFamily: "Inter, system-ui, Arial"
  },

  modeBar: {
    display: "flex",
    gap: 10,
    marginBottom: 10
  },

  upload: {
    marginBottom: 10
  },

  chat: {
    flex: 1,
    overflowY: "auto",
    padding: 12,
    display: "flex",
    flexDirection: "column",
    gap: 10,
    background: "#f9fafb",
    borderRadius: 8
  },

  userMsg: {
    alignSelf: "flex-end",
    background: "#4f46e5",
    color: "#fff",
    padding: "10px 14px",
    borderRadius: 12,
    maxWidth: "70%"
  },

  botMsg: {
    alignSelf: "flex-start",
    background: "#e5e7eb",
    color: "#111827",
    padding: "10px 14px",
    borderRadius: 12,
    maxWidth: "70%"
  },

  inputBar: {
    display: "flex",
    gap: 10,
    marginTop: 10
  },

  input: {
    flex: 1,
    padding: 10,
    borderRadius: 8,
    border: "1px solid #ddd"
  },

  button: {
    padding: "8px 14px",
    borderRadius: 8,
    border: "none",
    background: "#4f46e5",
    color: "#fff",
    cursor: "pointer"
  },

  disabledBtn: {
    padding: "8px 14px",
    borderRadius: 8,
    border: "none",
    background: "#a5b4fc",
    color: "#fff"
  },

  active: {
    padding: "8px 14px",
    borderRadius: 8,
    background: "#111827",
    color: "#fff"
  }
};

