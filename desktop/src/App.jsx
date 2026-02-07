import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Brain, Layers, Activity, Send, Minimize, Maximize, X } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

// API Configuration
const API_URL = "http://127.0.0.1:8000";

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Omni System Online. Ready for instructions.' }
  ]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('Idle');
  const [activeBrain, setActiveBrain] = useState('None');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initial Brain Check
  useEffect(() => {
    fetch(`${API_URL}/brains`)
      .then(res => res.json())
      .then(data => {
        // Just logic to update state if we want to show installed brains
        console.log("Brains:", data);
      })
      .catch(err => console.error("API Offline", err));
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setStatus('Processing...');

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.content, brain: activeBrain })
      });
      
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
      setStatus('Idle');
    } catch (error) {
      setMessages(prev => [...prev, { role: 'system', content: `Error: ${error.message}. Is 'omni serve' running?` }]);
      setStatus('Error');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex h-screen bg-omni-dark text-omni-text font-mono overflow-hidden">
      {/* Sidebar */}
      <div className="w-16 flex flex-col items-center py-4 border-r border-omni-dim bg-omni-panel">
        <div className="mb-8 text-omni-accent font-bold text-xl">O</div>
        
        <NavIcon icon={Terminal} label="Chat" active={activeTab === 'chat'} onClick={() => setActiveTab('chat')} />
        <NavIcon icon={Brain} label="Brains" active={activeTab === 'brains'} onClick={() => setActiveTab('brains')} />
        <NavIcon icon={Layers} label="Swarm" active={activeTab === 'swarm'} onClick={() => setActiveTab('swarm')} />
        
        <div className="mt-auto">
          <NavIcon icon={Activity} label="Status" />
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col relative">
        {/* Title Bar (Draggable) */}
        <div className="h-8 flex justify-between items-center px-4 bg-omni-panel border-b border-omni-dim select-none" style={{WebkitAppRegion: 'drag'}}>
          <span className="text-xs text-gray-500">OMNI DESKTOP v0.8.5</span>
          <div className="flex gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500 opacity-50 hover:opacity-100 cursor-pointer"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500 opacity-50 hover:opacity-100 cursor-pointer"></div>
            <div className="w-3 h-3 rounded-full bg-green-500 opacity-50 hover:opacity-100 cursor-pointer"></div>
          </div>
        </div>

        {/* Scanline Effect */}
        <div className="absolute inset-0 pointer-events-none scanline opacity-10"></div>

        {/* Chat Area */}
        {activeTab === 'chat' && (
          <div className="flex-1 flex flex-col overflow-hidden">
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[80%] p-3 rounded-lg ${
                    msg.role === 'user' 
                      ? 'bg-omni-dim border border-gray-700 text-white' 
                      : msg.role === 'system'
                      ? 'text-yellow-500 text-sm'
                      : 'bg-omni-panel border border-omni-accent text-omni-accent'
                  }`}>
                    <ReactMarkdown className="prose prose-invert prose-sm">
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-omni-panel border-t border-omni-dim">
              <div className="flex gap-2 items-center bg-black border border-gray-700 rounded-md p-2 focus-within:border-omni-accent transition-colors">
                <span className="text-omni-accent animate-pulse">{'>'}</span>
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Command the Swarm..."
                  className="flex-1 bg-transparent outline-none text-white placeholder-gray-600"
                  autoFocus
                />
                <button onClick={sendMessage} disabled={loading} className="text-gray-500 hover:text-omni-accent disabled:opacity-50">
                  <Send size={18} />
                </button>
              </div>
              <div className="flex justify-between mt-2 text-[10px] text-gray-500 uppercase tracking-wider">
                <span>Active Brain: {activeBrain}</span>
                <span>Status: {status}</span>
              </div>
            </div>
          </div>
        )}

        {/* Placeholders for other tabs */}
        {activeTab === 'brains' && (
          <div className="flex-1 p-8 flex items-center justify-center text-gray-500">
            Brain Manager Coming Soon
          </div>
        )}
      </div>
    </div>
  )
}

function NavIcon({ icon: Icon, label, active, onClick }) {
  return (
    <div 
      onClick={onClick}
      className={`p-3 mb-2 rounded-lg cursor-pointer transition-all duration-200 group relative ${
        active ? 'bg-omni-accent/10 text-omni-accent' : 'text-gray-500 hover:bg-white/5 hover:text-gray-300'
      }`}
    >
      <Icon size={24} />
      {/* Tooltip */}
      <div className="absolute left-14 top-2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50 pointer-events-none">
        {label}
      </div>
    </div>
  )
}

export default App
