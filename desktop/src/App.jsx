import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Brain, Layers, Activity, Send, Mic, Headphones, Image as ImageIcon, X } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

// API Configuration
const API_URL = "http://127.0.0.1:8000";

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Omni System Online. Ready.' }
  ]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('Idle');
  const [activeBrain, setActiveBrain] = useState('None');
  const [isLiveMode, setIsLiveMode] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  
  const messagesEndRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

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
        console.log("Brains:", data);
        if (data.installed.length > 0) setActiveBrain(data.installed[0]);
      })
      .catch(err => console.error("API Offline", err));
  }, []);

  const sendMessage = async (textOverride = null) => {
    const textToSend = textOverride || input;
    if (!textToSend.trim()) return;

    if (!textOverride) {
      setMessages(prev => [...prev, { role: 'user', content: textToSend }]);
      setInput('');
    }
    
    setLoading(true);
    setStatus('Thinking...');

    try {
      // 1. Get Text Response
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: textToSend, brain: activeBrain })
      });
      const data = await res.json();
      const aiResponse = data.response;

      setMessages(prev => [...prev, { role: 'assistant', content: aiResponse }]);
      
      // 2. If Live Mode, Speak it
      if (isLiveMode) {
        setStatus('Speaking...');
        const speakRes = await fetch(`${API_URL}/speak`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: aiResponse })
        });
        const blob = await speakRes.blob();
        const audioUrl = URL.createObjectURL(blob);
        const audio = new Audio(audioUrl);
        audio.play();
        audio.onended = () => {
            setStatus('Listening...');
            startRecording(); // Loop back to listening!
        };
      } else {
          setStatus('Idle');
      }

    } catch (error) {
      setMessages(prev => [...prev, { role: 'system', content: `Error: ${error.message}` }]);
      setStatus('Error');
    } finally {
      setLoading(false);
    }
  };

  // -- VOICE LOGIC --

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        await processAudio(audioBlob);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setStatus('Listening...');
    } catch (err) {
      console.error("Mic Error:", err);
      setIsLiveMode(false);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setStatus('Processing Audio...');
    }
  };

  const processAudio = async (audioBlob) => {
    const formData = new FormData();
    formData.append('file', audioBlob, 'input.wav');

    try {
      const res = await fetch(`${API_URL}/voice`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (data.transcription && data.transcription.trim()) {
        setMessages(prev => [...prev, { role: 'user', content: data.transcription }]);
        await sendMessage(data.transcription);
      } else {
          // Silence detected, maybe listen again?
          if (isLiveMode) startRecording(); 
      }
    } catch (err) {
      console.error("Transcription failed", err);
    }
  };

  const toggleLiveMode = () => {
    if (isLiveMode) {
      setIsLiveMode(false);
      stopRecording();
      setStatus('Idle');
    } else {
      setIsLiveMode(true);
      startRecording();
    }
  };

  // -- VISION LOGIC --
  const handleImageUpload = async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('file', file);
      formData.append('prompt', "Describe this image for me.");
      
      setMessages(prev => [...prev, { role: 'user', content: `[Sent Image: ${file.name}]` }]);
      setLoading(true);
      setStatus('Viewing...');

      try {
          const res = await fetch(`${API_URL}/vision`, { method: 'POST', body: formData });
          const data = await res.json();
          setMessages(prev => [...prev, { role: 'assistant', content: data.description }]);
      } catch (err) {
          console.error(err);
      } finally {
          setLoading(false);
          setStatus('Idle');
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
      <div className="w-16 flex flex-col items-center py-4 border-r border-omni-dim bg-omni-panel z-10">
        <div className="mb-8 text-omni-accent font-bold text-xl">O</div>
        
        <NavIcon icon={Terminal} label="Chat" active={activeTab === 'chat'} onClick={() => setActiveTab('chat')} />
        <NavIcon icon={Brain} label="Brains" active={activeTab === 'brains'} onClick={() => setActiveTab('brains')} />
        <NavIcon icon={Layers} label="Swarm" active={activeTab === 'swarm'} onClick={() => setActiveTab('swarm')} />
        
        <div className="mt-auto flex flex-col gap-4 mb-4">
           {/* Live Mode Toggle */}
            <div 
                onClick={toggleLiveMode}
                className={`p-3 rounded-full cursor-pointer transition-all duration-300 ${
                    isLiveMode 
                    ? 'bg-red-500/20 text-red-500 animate-pulse shadow-[0_0_15px_rgba(239,68,68,0.5)]' 
                    : 'text-gray-500 hover:text-omni-accent'
                }`}
                title="Omni Live (Voice Mode)"
            >
                <Headphones size={20} />
            </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col relative">
        {/* Title Bar */}
        <div className="h-8 flex justify-between items-center px-4 bg-omni-panel border-b border-omni-dim select-none" style={{WebkitAppRegion: 'drag'}}>
          <span className="text-xs text-gray-500">OMNI DESKTOP v0.9.1</span>
           <span className="text-xs text-omni-accent">{status}</span>
        </div>

        {/* Scanline Effect */}
        <div className="absolute inset-0 pointer-events-none scanline opacity-5"></div>

        {/* Chat Area */}
        {activeTab === 'chat' && (
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Live Mode Overlay */}
            {isLiveMode && (
                <div className="absolute inset-0 bg-black/80 backdrop-blur-sm z-20 flex flex-col items-center justify-center">
                    <div className="w-32 h-32 rounded-full border-4 border-omni-accent flex items-center justify-center animate-pulse shadow-[0_0_30px_#00ff9d]">
                        <Mic size={48} className="text-omni-accent" />
                    </div>
                    <h2 className="mt-8 text-2xl font-bold text-omni-accent tracking-widest">OMNI LIVE</h2>
                    <p className="mt-2 text-gray-400">{status}</p>
                    <button 
                        onClick={toggleLiveMode}
                        className="mt-12 px-6 py-2 border border-red-500 text-red-500 rounded hover:bg-red-500/10 transition-colors"
                    >
                        END SESSION
                    </button>
                </div>
            )}

            <div className="flex-1 overflow-y-auto p-4 space-y-4 pb-20">
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
                
                {/* Image Upload */}
                <label className="cursor-pointer text-gray-500 hover:text-omni-accent transition-colors">
                    <ImageIcon size={18} />
                    <input type="file" accept="image/*" className="hidden" onChange={handleImageUpload} />
                </label>

                <span className="text-omni-accent">{'>'}</span>
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Command the Swarm..."
                  className="flex-1 bg-transparent outline-none text-white placeholder-gray-600"
                  autoFocus
                />
                
                {/* Send Button */}
                <button onClick={() => sendMessage()} disabled={loading} className="text-gray-500 hover:text-omni-accent disabled:opacity-50">
                  <Send size={18} />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Placeholders */}
        {activeTab === 'brains' && (
          <div className="flex-1 p-8 flex items-center justify-center text-gray-500">
            Brain Manager (16GB+ RAM Auto-Detect Active)
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
      <div className="absolute left-14 top-2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50 pointer-events-none">
        {label}
      </div>
    </div>
  )
}

export default App
